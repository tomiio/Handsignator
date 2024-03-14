#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <Adafruit_MPU6050.h>
#include <utility/imumaths.h>

#include <WiFi.h>
#include "AsyncUDP.h"

AsyncUDP udp;

const char * ssid = "pihand";
const char * password = "";

#define TCAADDR 0x70
#define LED_PIN 15

Adafruit_MPU6050 mpu;
Adafruit_BNO055 bno = Adafruit_BNO055(55,0x29);

void selectChannel(uint8_t channel) {
  Wire.begin();
  Wire.beginTransmission(TCAADDR);
  Wire.write(1 << channel);
  Wire.endTransmission();
}

sensors_event_t event_acc, event_gyro;
sensors_event_t a, g, temp;
// double calib_offset[6][3] = {{0.12, 0.02, 0.0},
//                           {0.05, 0.03,-0.03},
//                           {0.05,-0.01, 0.02},
//                           {0.09,-0.01, 0.01},
//                           {0.12, 0.03, 0.00},
//                           {0.05, 0.00, 0.02}};

double calib_offset[6][3] = {0};

void setup() {
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, HIGH);

  Serial.begin(115200);
  // Initialize I2C bus at 400 kHz
  Wire.setClock(400000);
  Wire.begin();

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  if (WiFi.waitForConnectResult() != WL_CONNECTED) {
      Serial.println("WiFi Failed");
      while(1) {
          delay(1000);
      }
  }

  if(udp.connect(IPAddress(10,42,0,1), 3000)) {
          Serial.println("UDP connected");
          udp.onPacket([](AsyncUDPPacket packet) {
              Serial.print("UDP Packet Type: ");
              Serial.print(packet.isBroadcast()?"Broadcast":packet.isMulticast()?"Multicast":"Unicast");
              Serial.print(", From: ");
              Serial.print(packet.remoteIP());
              Serial.print(":");
              Serial.print(packet.remotePort());
              Serial.print(", To: ");
              Serial.print(packet.localIP());
              Serial.print(":");
              Serial.print(packet.localPort());
              Serial.print(", Length: ");
              Serial.print(packet.length());
              Serial.print(", Data: ");
              Serial.write(packet.data(), packet.length());
              Serial.println();
              //reply to the client
              packet.printf("Got %u bytes of data", packet.length());
          });
          //Send unicast
          //udp.print("Hello Server!");
      }

  Wire.beginTransmission(TCAADDR);
  Wire.write(0xFF);
  Wire.endTransmission();

  for (uint8_t t = 0; t < 6; t++) {
    selectChannel(t);

    if (t == 0 && !bno.begin()) {
      Serial.println("Failed to initialize BNO055 sensor!");
      while (1);
    }

    if (t > 0){
      if (!mpu.begin()) {
        Serial.println("Failed to find MPU6050 chip");
        while (1) {
          delay(10);
        }
      }
      mpu.setAccelerometerRange(MPU6050_RANGE_4_G);
      mpu.setGyroRange(MPU6050_RANGE_250_DEG);
      mpu.setFilterBandwidth(MPU6050_BAND_5_HZ);
      delay(100);
    }
    //Serial.println("");
  }

  Wire.setClock(400000);

  Serial.println("Init successfully!!!");
  delay(100);
  digitalWrite(LED_PIN, LOW);
  
}

void loop() {
  long int timestamp, start_time = millis();
  double data[37] = {0};

  // for (int i = 0; i < 50; i++) {
  //   //Serial.println("timestamp,a0x,a0y,a0z,g0x,g0y,g0z,a1x,a1y,a1z,g1x,g1y,g1z,a2x,a2y,a2z,g2x,g2y,g2z,a3x,a3y,a3z,g3x,g3y,g3z,a4x,a4y,a4z,g4x,g4y,g4z,a5x,a5y,a5z,g5x,g5y,g5z");
  //   timestamp = millis();
  //   Serial.print(timestamp - start_time);
  //   Serial.print(",");
    uint8_t j = 7;
    
    for (uint8_t i = 0; i<6; i++)
    {
      selectChannel(i);

      if (i == 0){
        bno.getEvent(&event_acc, Adafruit_BNO055::VECTOR_ACCELEROMETER);
        bno.getEvent(&event_gyro, Adafruit_BNO055::VECTOR_GYROSCOPE);

        data[1] = event_acc.acceleration.x;
        data[2] = event_acc.acceleration.y;
        data[3] = event_acc.acceleration.z;
        data[4] = event_gyro.gyro.x;
        data[5] = event_gyro.gyro.y;
        data[6] = event_gyro.gyro.z;

        
      }
      else if (i>0){
        mpu.getEvent(&a, &g, &temp);

        data[j] = a.acceleration.x;
        data[j+1] = a.acceleration.y;
        data[j+2] = a.acceleration.z;
        data[j+3] = g.gyro.x;
        data[j+4] = g.gyro.y;
        data[j+5] = g.gyro.z;
        j = j + 6;
      }
    }
    // if left hand -> data[0] = 0
    // if right hand -> data[0] = 1
    String message = "1," + String(data[1],2)  + "," + String(data[2],2)  + "," + String(data[3],2)  + "," + String(data[4],2)  + "," + String(data[5],2)  + "," + String(data[6],2) 
                    + "," + String(data[7],2)  + "," + String(data[8],2)  + "," + String(data[9],2)  + "," + String(data[10],2) + "," + String(data[11],2) + "," + String(data[12],2)
                    + "," + String(data[13],2) + "," + String(data[14],2) + "," + String(data[15],2) + "," + String(data[16],2) + "," + String(data[17],2) + "," + String(data[18],2)
                    + "," + String(data[19],2) + "," + String(data[20],2) + "," + String(data[21],2) + "," + String(data[22],2) + "," + String(data[23],2) + "," + String(data[24],2) 
                    + "," + String(data[25],2) + "," + String(data[26],2) + "," + String(data[27],2) + "," + String(data[28],2) + "," + String(data[29],2) + "," + String(data[30],2) 
                    + "," + String(data[31],2) + "," + String(data[32],2) + "," + String(data[33],2) + "," + String(data[34],2) + "," + String(data[35],2) + "," + String(data[36],2);

    Serial.println(message);
    udp.print(message);
  // }
}


