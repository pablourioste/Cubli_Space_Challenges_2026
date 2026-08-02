#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <atomic>
#include <chrono>
#include <cstdint>
#include <cstring>
#include <deque>
#include <functional>
#include <iostream>
#include <limits>
#include <string>
#include <thread>

// ---- Adjustable test parameters ----
constexpr float kRpm = 12.0f;  // negate this to spin the other direction
constexpr auto kMaxDuration = std::chrono::milliseconds(600000);  // 10 min hard safety cap; Ctrl+C stops sooner -- raise this for a longer continuous run
constexpr auto kCommandPeriod = std::chrono::milliseconds(20);    // well under moteus's 100ms watchdog

constexpr char kPort[] = R"(\\.\COM7)";
const std::string kMoteusId = "8001";  // same target that worked for the status query

// ---- Adapter/serial plumbing: identical to the earlier working programs ----

struct ScopedHandle {
    HANDLE h;
    explicit ScopedHandle(HANDLE handle) : h(handle) {}
    ~ScopedHandle() { if (h != INVALID_HANDLE_VALUE) CloseHandle(h); }
    operator HANDLE() const { return h; }
    bool IsValid() const { return h != INVALID_HANDLE_VALUE; }
};

HANDLE OpenCanAdapter() {
    HANDLE port = CreateFileA(
        kPort, GENERIC_READ | GENERIC_WRITE, 0, nullptr, OPEN_EXISTING, 0, nullptr);
    if (port == INVALID_HANDLE_VALUE) {
        std::cerr << "Cannot open " << kPort << ". Check Device Manager and update kPort if needed.\n";
        return INVALID_HANDLE_VALUE;
    }

    DCB settings{};
    settings.DCBlength = sizeof(settings);
    if (!GetCommState(port, &settings)) {
        std::cerr << "GetCommState failed.\n";
        CloseHandle(port);
        return INVALID_HANDLE_VALUE;
    }

    settings.BaudRate = CBR_115200;
    settings.ByteSize = 8;
    settings.Parity = NOPARITY;
    settings.StopBits = ONESTOPBIT;
    settings.fBinary = TRUE;
    settings.fDtrControl = DTR_CONTROL_ENABLE;
    settings.fRtsControl = RTS_CONTROL_ENABLE;
    settings.fOutxCtsFlow = FALSE;
    settings.fOutxDsrFlow = FALSE;
    settings.fDsrSensitivity = FALSE;
    settings.fOutX = FALSE;
    settings.fInX = FALSE;
    settings.fAbortOnError = FALSE;

    if (!SetCommState(port, &settings)) {
        std::cerr << "SetCommState failed.\n";
        CloseHandle(port);
        return INVALID_HANDLE_VALUE;
    }

    COMMTIMEOUTS timeouts{};
    timeouts.ReadIntervalTimeout = MAXDWORD;
    timeouts.ReadTotalTimeoutMultiplier = 0;
    timeouts.ReadTotalTimeoutConstant = 0;
    timeouts.WriteTotalTimeoutConstant = 1000;
    SetCommTimeouts(port, &timeouts);

    PurgeComm(port, PURGE_RXCLEAR | PURGE_TXCLEAR);
    return port;
}

bool SendLine(HANDLE port, const std::string& line) {
    DWORD bytes_written = 0;
    if (!WriteFile(port, line.data(), static_cast<DWORD>(line.size()), &bytes_written, nullptr) ||
        bytes_written != static_cast<DWORD>(line.size())) {
        std::cerr << "Write failed for: " << line;
        return false;
    }
    return true;
}

class LineReader {
public:
    explicit LineReader(HANDLE port) : port_(port) {}

    std::string Wait(std::chrono::steady_clock::time_point deadline,
        const std::function<bool(const std::string&)>& predicate) {
        for (;;) {
            for (auto it = queue_.begin(); it != queue_.end(); ++it) {
                if (predicate(*it)) {
                    std::string result = std::move(*it);
                    queue_.erase(it);
                    return result;
                }
            }
            if (std::chrono::steady_clock::now() >= deadline) return {};
            Pump();
        }
    }

private:
    void Pump() {
        char buf[256];
        DWORD n = 0;
        if (!ReadFile(port_, buf, sizeof(buf), &n, nullptr) || n == 0) {
            std::this_thread::sleep_for(std::chrono::milliseconds(1));
            return;
        }
        partial_.append(buf, n);
        size_t pos;
        while ((pos = partial_.find('\n')) != std::string::npos) {
            std::string line = partial_.substr(0, pos);
            partial_.erase(0, pos + 1);
            if (!line.empty() && line.back() == '\r') line.pop_back();
            if (line.empty()) continue;
            if (line.rfind("ERR", 0) == 0) std::cerr << "Adapter: " << line << '\n';
            queue_.push_back(std::move(line));
        }
    }

    HANDLE port_;
    std::string partial_;
    std::deque<std::string> queue_;
};

bool IsAckLine(const std::string& line) {
    return line == "OK" || line.rfind("ERR", 0) == 0;
}

bool IsAnyRcv(const std::string& line) {
    return line.rfind("rcv", 0) == 0;
}

// ---- Building moteus command frames ----

std::string ByteToHex(uint8_t b) {
    static const char* digits = "0123456789abcdef";
    std::string s(2, '0');
    s[0] = digits[(b >> 4) & 0xF];
    s[1] = digits[b & 0xF];
    return s;
}

std::string FloatToHexLE(float value) {
    uint8_t bytes[4];
    std::memcpy(bytes, &value, sizeof(bytes));
    std::string out;
    for (uint8_t b : bytes) out += ByteToHex(b);
    return out;
}

// MODE=10(POSITION), COMMAND_POSITION=NaN (velocity-only), COMMAND_VELOCITY=target,
// then reads back MODE / POSITION,VELOCITY,TORQUE / VOLTAGE,TEMPERATURE,FAULT.
std::string BuildVelocityCommandHex(float velocity_rev_per_s) {
    const float position_nan = std::numeric_limits<float>::quiet_NaN();
    std::string hex;
    hex += "01" "00" "0a";
    hex += "0e" "20";
    hex += FloatToHexLE(position_nan);
    hex += FloatToHexLE(velocity_rev_per_s);
    hex += "11" "00";
    hex += "1f" "01";
    hex += "13" "0d";
    return hex;
}

// MODE=0 (STOPPED): cleanly disables the driver and clears any latched fault.
std::string BuildStopCommandHex() {
    return "01" "00" "00"
        "11" "00";
}

std::atomic<bool> g_stop_requested{ false };

BOOL WINAPI ConsoleHandler(DWORD signal) {
    if (signal == CTRL_C_EVENT || signal == CTRL_CLOSE_EVENT) {
        g_stop_requested = true;
        return TRUE;
    }
    return FALSE;
}

void SendAndMaybeCapture(HANDLE port, LineReader& reader, const std::string& hex_payload,
    std::string& last_rcv) {
    SendLine(port, "can send " + kMoteusId + " " + hex_payload + "\n");
    auto line = reader.Wait(std::chrono::steady_clock::now() + std::chrono::milliseconds(5),
        [](const std::string& l) { return IsAckLine(l) || IsAnyRcv(l); });
    if (!line.empty() && IsAnyRcv(line)) {
        last_rcv = line;
    }
}

void RunVelocityPhase(HANDLE port, LineReader& reader, float rpm,
    std::chrono::milliseconds duration, const char* label) {
    const float velocity_rev_per_s = rpm / 60.0f;
    std::cout << "\n-- " << label << ": " << rpm << " RPM ("
        << velocity_rev_per_s << " rev/s) --\n";

    const std::string hex_payload = BuildVelocityCommandHex(velocity_rev_per_s);
    const auto phase_end = std::chrono::steady_clock::now() + duration;
    std::string last_rcv;
    int tick = 0;

    while (std::chrono::steady_clock::now() < phase_end && !g_stop_requested) {
        auto tick_start = std::chrono::steady_clock::now();

        SendAndMaybeCapture(port, reader, hex_payload, last_rcv);

        if (++tick % 50 == 0 && !last_rcv.empty()) {  // ~once/second at 20ms ticks
            std::cout << last_rcv << '\n';
        }

        std::this_thread::sleep_until(tick_start + kCommandPeriod);
    }
}

int main() {
    SetConsoleCtrlHandler(ConsoleHandler, TRUE);

    ScopedHandle port(OpenCanAdapter());
    if (!port.IsValid()) {
        return 1;
    }
    LineReader reader(port);

    SendLine(port, "can on\n");
    reader.Wait(std::chrono::steady_clock::now() + std::chrono::milliseconds(300), IsAckLine);
    // An ERR here (e.g. "already in BusOn") is fine.

    std::cout << "Clearing to a known stopped state...\n";
    SendLine(port, "can send " + kMoteusId + " " + BuildStopCommandHex() + "\n");
    reader.Wait(std::chrono::steady_clock::now() + std::chrono::milliseconds(200), IsAnyRcv);

    RunVelocityPhase(port, reader, kRpm, kMaxDuration, "Spinning (Ctrl+C to stop)");

    std::cout << "\nStopping motor...\n";
    SendLine(port, "can send " + kMoteusId + " " + BuildStopCommandHex() + "\n");
    auto stop_reply = reader.Wait(std::chrono::steady_clock::now() + std::chrono::milliseconds(300), IsAnyRcv);
    if (!stop_reply.empty()) {
        std::cout << stop_reply << '\n';
    }

    return 0;  // ScopedHandle closes the port here
}