#include <HS300x.h>
#include <Arduino_LPS22HB.h>
#include <Arduino.h>

#include "mbed.h"
using namespace mbed;
LowPowerTimeout timer;


volatile bool shouldWakeup = false;

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


void wake(){
  shouldWakeup = true;
}

void setup(){

  // 初期化
  pinMode(M0, OUTPUT);
  pinMode(M1, OUTPUT);
  
  Serial.begin(9600);
  Serial1.begin(9600);
  while(!Serial1);
  delay(50);
  Serial.println("Setup Start");

  // LoRaモジュールの初期化
  mode3();

  Set_parameters();

  // SleepModeをSLEEPDEEPに設定
  SCB->SCR |= (1 << 2);
  

  Serial.println("Setup done");

  Serial.end();
  Serial1.end();
  delay(50);

  
}

void loop(){

  shouldWakeup = false;

  timer.attach(&wake, 59.5f);
  while(!shouldWakeup){
    sleep();
  }

  Serial.begin(9600);
  Serial1.begin(9600);
  delay(50);

  Serial.println("Wakeup");
  
  int voltage = analogRead(A0);
  
  float vinput = 3300.0*voltage/512;

  HS300x.begin();
  BARO.begin();

  delay(50);
  
  float temp = HS300x.readTemperature(CELSIUS);
  float humid = HS300x.readHumidity();
  float pressure = BARO.readPressure();

  delay(50);

  HS300x.end();
  BARO.end();

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

  delay(50);
  
  Serial1.write(payload, sizeof(payload));

  delay(50);

  mode3();
  Serial.println("Data Sended");

  Serial.end();
  Serial1.end();

  return;
}


  
