#include <HS300x.h>
#include <Arduino_LPS22HB.h>

#include "lora_lib.h"

#define SEC 1000
#define MIN (60*SEC)
#define HOUR (60*MIN)


#define M0 D2
#define M1 D3

uint8_t payload[32];

byte temp_bytes[4];
byte humid_bytes[4];
byte pressure_bytes[4];
byte vinput_bytes[4];





void setup(){
  pinMode(M0, OUTPUT);
  pinMode(M1, OUTPUT);
  
  Serial.begin(9600);
  Serial1.begin(9600);
  HS300x.begin();
  BARO.begin();
  while(!Serial1);
  
  delay(1000);

  Serial.println("Setup Start");

  bool check_3 = mode3();
  if (!check_3) {
    Serial.println("Mode 3 ERROR");
    while(1);
  }

  Set_parameters();

  Serial.println("Setup done");
}

void loop(){

  int voltage = analogRead(A0);
  Serial.print("analogRead: ");
  Serial.println(voltage);
  
  float vinput = 3300.0*voltage/512;
  Serial.print("Voltage: ");
  Serial.print(vinput);
  Serial.println("mV");
  

  bool check_1 = mode0();

  Serial.println("Mode 0 done");
  
  float temp = HS300x.readTemperature(CELSIUS);
  float humid = HS300x.readHumidity();
  float pressure = BARO.readPressure();

  Serial.print("Temperature: ");
  Serial.println(temp);

  Serial.print("Humidity: ");
  Serial.println(humid);

  Serial.print("Pressure: ");
  Serial.println(pressure);

  delay(SEC);

  float2bytes(temp, temp_bytes);
  float2bytes(humid, humid_bytes);
  float2bytes(pressure, pressure_bytes);
  float2bytes(vinput, vinput_bytes);

  payload[0] = 0x00;
  payload[1] = 0x00;
  payload[2] = 0x00;
  for (int i = 0; i<sizeof(float); i++) {
    payload[3+i] = temp_bytes[i];
    payload[7+i] = humid_bytes[i];
    payload[11+i] = pressure_bytes[i];
    payload[15+i] = vinput_bytes[i];
  }
  
  Serial1.write(payload, sizeof(payload));
  Serial.println("Data Sended");

  delay(1 * MIN);

  return;
}


  
