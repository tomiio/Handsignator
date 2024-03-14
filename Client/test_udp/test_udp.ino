#include <BluetoothSerial.h>

BluetoothSerial SerialBT;

void setup() {
  Serial.begin(115200);
  SerialBT.begin("ESP32-S2"); // Set the name for your ESP32-S2 Bluetooth device
}

void loop() {
  if (Serial.available()) {
    String data = "Hello!!!"; 
    SerialBT.print(data); // Send the data to the Bluetooth Serial server

    // If you want to add a newline character at the end of each message, use the following line instead:
    // SerialBT.println(data);

    // Print the sent data to the serial monitor
    Serial.print("Sent: ");
    Serial.println(data);
  }
}