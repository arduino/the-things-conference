#include <Wire.h>

#define USE_IOT_CLOUD true
#define I2C_ADDRESS 8

#if USE_IOT_CLOUD
  #include "arduino_secrets.h"
  #include "thingProperties.h"  
#endif

String sortedClasses[4] = {"Centipede", "﻿Cockroach", "Spider", "Unknown"};
int amounts[4] = {0, 0, 0, 0};

void initializeIoTCloud(){
  #if USE_IOT_CLOUD  
  initProperties(); // Defined in thingProperties.h
  ArduinoCloud.begin(ArduinoIoTPreferredConnection);
  
  setDebugMessageLevel(2);
  ArduinoCloud.printDebugInfo();

  while(!ArduinoCloud.connected()) {
    ArduinoCloud.update();
    delay(10);
  }
  #endif
}

void setup(){
  pinMode(LED_BUILTIN, OUTPUT);  
  Serial.begin(115200);  // start serial for output
  while(!Serial && millis() < 5000);
  Wire.begin(I2C_ADDRESS);        // join i2c bus as slave
  Wire.onReceive(receiveEvent); // register event
  initializeIoTCloud();
}

void blink(){
  digitalWrite(LED_BUILTIN, HIGH);
  delay(250);
  digitalWrite(LED_BUILTIN, LOW);
}

void updateCloudValues(){
  #if USE_IOT_CLOUD  
  Serial.println("Updating cloud values...");  
  cockroachCount = amounts[0];
  centipedeCount = amounts[1];
  spiderCount = amounts[2];
  #endif
}

void receiveEvent(int amountOfBytes){
  Serial.println("\n-------------------------");
  
  int i=0;
  while(Wire.available()){     
    char data = Wire.read(); // receive a byte as character
    amounts[i] = (int) data;
    Serial.println(sortedClasses[i] + String(": ") + String(amounts[i]));
    ++i;
  }
  
  Serial.println("-------------------------\n");
  blink();
  updateCloudValues();
}

void loop(){
  #if USE_IOT_CLOUD  
  ArduinoCloud.update();
  #endif
}
