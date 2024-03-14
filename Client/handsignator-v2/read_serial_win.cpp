#include <Windows.h>
#include <iostream>

int main() {
    HANDLE serialHandle;
    DCB dcbSerialParams = { 0 };
    COMMTIMEOUTS timeouts = { 0 };
    char buffer[256];
    DWORD bytesRead;

    // Open the serial port
    serialHandle = CreateFile("COM1", GENERIC_READ, 0, NULL, OPEN_EXISTING, 0, NULL);
    if (serialHandle == INVALID_HANDLE_VALUE) {
        std::cerr << "Failed to open the serial port." << std::endl;
        return 1;
    }

    // Set serial port parameters
    dcbSerialParams.DCBlength = sizeof(dcbSerialParams);
    if (!GetCommState(serialHandle, &dcbSerialParams)) {
        std::cerr << "Failed to get serial port parameters." << std::endl;
        CloseHandle(serialHandle);
        return 1;
    }
    dcbSerialParams.BaudRate = CBR_9600;  // Set the baud rate to 9600
    dcbSerialParams.ByteSize = 8;         // 8-bit data
    dcbSerialParams.StopBits = ONESTOPBIT;// 1 stop bit
    dcbSerialParams.Parity = NOPARITY;    // No parity

    if (!SetCommState(serialHandle, &dcbSerialParams)) {
        std::cerr << "Failed to set serial port parameters." << std::endl;
        CloseHandle(serialHandle);
        return 1;
    }

    // Set timeouts for reading
    timeouts.ReadIntervalTimeout = 50;           // Max time between receiving two bytes (milliseconds)
    timeouts.ReadTotalTimeoutConstant = 50;      // Total time for reading (milliseconds)
    timeouts.ReadTotalTimeoutMultiplier = 10;    // Additional time per byte (milliseconds)
    timeouts.WriteTotalTimeoutConstant = 50;     // Total time for writing (milliseconds)
    timeouts.WriteTotalTimeoutMultiplier = 10;   // Additional time per byte (milliseconds)
    if (!SetCommTimeouts(serialHandle, &timeouts)) {
        std::cerr << "Failed to set serial port timeouts." << std::endl;
        CloseHandle(serialHandle);
        return 1;
    }

    // Read data from the serial port
    if (!ReadFile(serialHandle, buffer, sizeof(buffer), &bytesRead, NULL)) {
        std::cerr << "Failed to read data from the serial port." << std::endl;
        CloseHandle(serialHandle);
        return 1;
    }

    // Display the received data
    std::cout << "Received data: " << buffer << std::endl;

    // Close the serial port
    CloseHandle(serialHandle);

    return 0;
}