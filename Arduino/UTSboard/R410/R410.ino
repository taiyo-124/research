// constants
#define SEC1 1000
#define SEC10 (10 * SEC1)
#define MIN1 (60 * SEC1)
#define MIN10 (10 * MIN1)
#define MIN30 (3 * MIN10)
#define MIN60 (6 * MIN10)
#define WDT_PER_SEC (8 * SEC1)

// variables
#define LOOP_PER_MILLI_SEC MIN10
#define SAVE_SD false

#define SAVE_GPS_LTE false

#define USE_WDT true
#define USE_DEEP_SLEEP true
/*
How to use WDT and DEEP_SLEEP
- !USE_WDT
    - NORMAL
- USE_WDT && USE_DEEP_SLEEP
    - STANDBY
- USE_WDT && !USE_DEEP_SLEEP
    - IDLE
*/
//#include <Adafruit_TinyUSB.h> // for Serial
//#include <bluefruit.h>
// variables but as constants
#define SAVE_CO2 
#define GET_GPS false

/*
 * Counter of WDT 8s
 * 8 * 8 * 1000 = 64000 ms = 1 min 4 sec
 * 75 * 8 * 10000 = 600000 ms = 10min
 * 75 * 8 * 3 * 10000 = 1800000 ms = 30min
 * 75 * 8 * 3 * 2 * 10000 = 3600000 ms = 60min
 */

#include "CO2.h"
#include "GPS.h"
#include "INQR410.h"
#include "SDCard.h"
#include "WDT.h"

#include <Adafruit_BME680.h>
extern Adafruit_BME680 bme; // I2C
// https://github.com/adafruit/Adafruit_BME680

#define SEALEVELPRESSURE_HPA (1013.25)
#define DEBUG 1
#define DEBUG_STREAM SerialUSB
#define hr "===================="
#define SERIAL_BPS 9600
#define CO2_ENABLE A6

// Sodaq_LSM303AGR accelerometer;
// https://github.com/SodaqMoja/Sodaq_LSM303AGR

// DEEP_SLEEPの回数
unsigned long deepSleepCount = 0;
// 1回のlongSleep中のDEEP_SLEEP(STANDBYモードにおいて)の回数
unsigned long sleepTimesPerDeepSleep = LOOP_PER_MILLI_SEC / WDT_PER_SEC;

// TODO: メモリ圧迫のため改善
template <class T> String anyToString(T value) { return String(value); }

void setup() {
  pinMode(LED_GREEN, OUTPUT);

  Serial.begin(SERIAL_BPS);

  if (SAVE_CO2) {
    pinMode(CO2_ENABLE, OUTPUT);
  }

  if (SAVE_SD) {
    initSd();
  }

  if (GET_GPS) {
    initGps();
  }

  if (USE_WDT) {
    initWdt();
  }

  initSensors();

  if (SAVE_GPS_LTE) {
    digitalWrite(GPS_ENABLE, LOW);
    pinMode(GPS_ENABLE, OUTPUT);

    digitalWrite(SARA_ENABLE, LOW); // 前からHIGH
    pinMode(SARA_ENABLE, OUTPUT);

    // digitalWrite(SARA_R4XX_TOGGLE, LOW); // 元からLOW
    // pinMode(SARA_R4XX_TOGGLE, OUTPUT);

    // digitalWrite(SARA_TX_ENABLE, LOW); // 元からLOW
    // pinMode(SARA_TX_ENABLE, OUTPUT);
  } else {
    digitalWrite(GPS_ENABLE, HIGH);
    pinMode(GPS_ENABLE, OUTPUT);

    digitalWrite(SARA_ENABLE, HIGH);
    pinMode(SARA_ENABLE, OUTPUT);

    // digitalWrite(SARA_R4XX_TOGGLE, HIGH); 元からLOW
    // pinMode(SARA_R4XX_TOGGLE, OUTPUT);

    // digitalWrite(SARA_TX_ENABLE, HIGH); 元からLOW
    // pinMode(SARA_TX_ENABLE, OUTPUT);
  }
  DEBUG_STREAM.println(hr);
  DEBUG_STREAM.println(SAVE_SD ? "SD Save" : "SD Not Save");
  DEBUG_STREAM.println(GET_GPS ? "GPS" : "GPS Not");
  if (!USE_WDT) {
    DEBUG_STREAM.println("NORMAL");
  } else if (USE_DEEP_SLEEP) {
    DEBUG_STREAM.println("STANDBY");
  } else {
    DEBUG_STREAM.println("IDLE");
  }
  DEBUG_STREAM.println(hr);
  pinMode(LED_RED, OUTPUT);
  delay(2 * SEC1);
}

void loop() {
  char outputBuf[256];

  if (SAVE_CO2) {
    digitalWrite(CO2_ENABLE, HIGH);
    delay(SEC1);
  }
  // TODO: バグの温床になるので改善
  // NORMAL：単にmillis()が経過時間
  // IDLE：NORMAL同様
  // STANDBY：このCPUモード中はCPU停止するが5msずつ経過するため、停止している時間を加え5msを引く
  unsigned long nowMilli = millis() + LOOP_PER_MILLI_SEC * deepSleepCount -
                           5 * sleepTimesPerDeepSleep * deepSleepCount;

  // TODO: floatをsprintfできないため冗長になっているが改善できるとベター
  String temp = anyToString(bme.readTemperature());
  String humid = anyToString(bme.readHumidity());
  String pres = anyToString(bme.readPressure());
  String gas = anyToString(bme.readGas());
  String alti = anyToString(bme.readAltitude(SEALEVELPRESSURE_HPA));
  String volt = anyToString(analogRead(BAT_VOLT));
  String co2 = anyToString(read_sensor_measurements());

  sprintf(outputBuf, "%lu %s %s %s %s %s %s %s", nowMilli, temp.c_str(),
          humid.c_str(), pres.c_str(), gas.c_str(), alti.c_str(), volt.c_str(),
          co2.c_str());

  if (GET_GPS) {
    String gps = findFix(0);
  }

  String filename = generatePath(nowMilli);
  DEBUG_STREAM.println(filename);
  DEBUG_STREAM.println(outputBuf);
  
  DEBUG_STREAM.println(hr);

  if (SAVE_SD) {
    writeSD(filename, outputBuf);
  }

  if (SAVE_CO2) {
    digitalWrite(CO2_ENABLE, LOW);
  }

  if (USE_WDT) {
    longSleep(LOOP_PER_MILLI_SEC, USE_DEEP_SLEEP);
    if (USE_DEEP_SLEEP) {
      deepSleepCount++;
    }
  } else {
    delay(LOOP_PER_MILLI_SEC);
  }

  return;
}
