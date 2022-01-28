#include "Arduino_BHY2.h"

#define FREQUENCY_HZ        100
#define INTERVAL_MS         (1000 / (FREQUENCY_HZ + 1))
SensorXYZ accel(SENSOR_ID_ACC);

void setup(){
  Serial.begin(115200);
  while(!Serial);
  BHY2.begin();
  accel.begin();
}

void loop(){
  static auto lastUpdate = millis();
  BHY2.update();

  if (millis() - lastUpdate >= INTERVAL_MS) {
    lastUpdate = millis();
    //Serial.println(String("Acceleration: ") + accel.toString());
    auto power = sqrt(accel.x() * accel.x() + accel.y() * accel.y() + accel.z() * accel.z());        
    Serial.println(power);
  }
}
