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
  Serial1.begin(9600);
  HS300x.begin();
  BARO.begin();
  while(!Serial1);

  mode3();

  delay(50);

  Set_parameters();

  delay(50);

}

void loop(){

  int voltage = analogRead(A0);
  
  float vinput = 3300.0*voltage/512;
  
  float temp = HS300x.readTemperature(CELSIUS);
  float humid = HS300x.readHumidity();
  float pressure = BARO.readPressure();
  
  delay(50);


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

  mode0();
  
  delay(10);
  
  Serial1.write(payload, sizeof(payload));

  delay(10 * SEC);

  return;
}


  
