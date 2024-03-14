#include <iostream>
#include <cstring>
#include <fcntl.h>
#include <termios.h>
#include <unistd.h>
#include <chrono>
#include <thread>

int main() {
    int serialPort;
    char buffer_char[256];
    ssize_t bytesRead;

    // Open the serial port
    serialPort = open("/dev/ttyACM0", O_RDWR);

    if (serialPort == -1) {
        std::cout << "Error opening serial port." << std::endl;
        return 1;
    }

    // Set serial port parameters
    struct termios tty;
    if (tcgetattr(serialPort, &tty) != 0) {
        std::cout << "Error getting serial port attributes." << std::endl;
        close(serialPort);
        return 1;
    }

    tty.c_cflag &= ~PARENB;            // Disable parity
    tty.c_cflag &= ~CSTOPB;            // Use one stop bit
    tty.c_cflag &= ~CSIZE;
    tty.c_cflag |= CS8;                // Set data bits to 8
    tty.c_cflag &= ~CRTSCTS;           // Disable hardware flow control
    tty.c_cflag |= CREAD | CLOCAL;     // Enable receiver and ignore control lines

    tty.c_iflag &= ~(IXON | IXOFF | IXANY);  // Disable software flow control

    tty.c_lflag = 0;                   // Disable terminal processing

    tty.c_oflag = 0;                   // Disable output processing

    tty.c_cc[VMIN] = 1;                // Read at least 1 character
    tty.c_cc[VTIME] = 5;               // Wait for up to 0.5 seconds

    if (tcsetattr(serialPort, TCSANOW, &tty) != 0) {
        std::cout << "Error setting serial port attributes." << std::endl;
        close(serialPort);
        return 1;
    }

    bool check_start = false;
    uint16_t k = 0, h = 0;               // k refer to index of buffer_temp, h refer to buffer_float
    char buffer_temp[256];
    float buffer_float[36] = {0};
    float input_buf[1800] = {0};

    // Read data from the serial port
    while (true) {
        
        bytesRead = read(serialPort, buffer_char, sizeof(buffer_char));
        if (bytesRead > 0) {
            // Process the received data
            for (ssize_t i = 0; i < bytesRead; ++i) {

                //std::cout << buffer_char[i]; // Each elements in the buffer
                
                if (buffer_char[i] == ','){
                    buffer_float[h] = std::strtof(buffer_temp, nullptr);
                    h++;
                    k = 0;
                    std::memset(buffer_temp, 0, sizeof(buffer_temp));
                }
                
                else if (buffer_char[i] == 10){    // 10 in ascii refer to enter to newline
     
                    buffer_float[h] = std::strtof(buffer_temp, nullptr);
  
                    std::memset(buffer_temp, 0, sizeof(buffer_temp));
                    
                    check_start = true;
                    k = 0;
                    h = 0;

                    // for (u_int8_t i = 0; i < 36; ++i) {
                    //     std::cout << buffer_float[i] << " ";
                    // }
                    // std::cout << std::endl;
                    i++;

                    for (uint16_t i = 0; i < 1750; i++){
                        input_buf[i] = input_buf[i+36];
                    }

                    for (uint16_t i = 1750; i < 1800; i++){
                        input_buf[i] = buffer_float[i-1750];
                    }

                    for (uint16_t i = 0; i < 1800; i++){
                        std::cout << input_buf[i] << ' ';
                    }
                    std::cout << std::endl;
                    //std::this_thread::sleep_for(std::chrono::seconds(1));

                    

                }
                else if (check_start == true){
                    buffer_temp[k] = buffer_char[i];
                    k++;
                }
            }
        }

        else if (bytesRead == -1) {
            std::cout << "Error reading from serial port." << std::endl;
            break;
        }
        //std::this_thread::sleep_for(std::chrono::seconds(1));
    }

    // Close the serial port
    close(serialPort);

    return 0;
}
