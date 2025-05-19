#include<SPI.h>
#include <SD.h>
#include <HS300x.h>
#include <BARO.h>

#define SEC 1000
#define MIN 60000
#define HOUR 3600000

const int chipselect = D10;

template <class T> String anyToString(T value) { return String(value); }

void setup(){
  pinMode(chipselect, OUTPUT);
  Serial.begin(9600);
  HS300x.begin();
  BARO.begin();
  delay(1000);

  if (!SD.begin(chipselect)){
    Serial.println("SD initialization failed");
    while(1);
  }

    Serial.println("Setup done");
}

void loop(){
  char outputbuf[256];
  
  int voltage = analogRead(A0);
  Serial.print("analogRead: ");
  Serial.println(voltage);
  
  float vinput = 3300.0*voltage/512;
  String Vinput = anyToString(vinput);
  
  Serial.print("Voltage: ");
  Serial.print(vinput);
  Serial.println("mV");
  
  float temp = HS300x.readTemperature(CELSIUS);
  float humid = HS300x.readHumidity();
  float pressure = BARO.readPressure();

  String Temp = anyToString(temp);
  String Humid = anyToString(humid);
  String Pressure = anyToString(pressure);

  Serial.print("Temperature: ");
  Serial.println(temp);

  Serial.print("Humidity: ");
  Serial.println(humid);

  Serial.print("Pressure: ");
  Serial.println(pressure);

  delay(SEC);

  unsigned long nowMillis = millis();

  Serial.print("millis: ");
  Serial.println(nowMillis);

  sprintf(outputbuf, "%lu %s %s %s %s", nowMillis, Temp.c_str(), Humid.c_str(), Pressure.c_str(), Vinput.c_str());
  Serial.println(outputbuf);

  String date = String(__DATE__);
  date.replace(" ", "");
  date.replace("2025", "");

  Serial.println(date);
  
  if (!SD.exists(date)){
    SD.mkdir(date);
    Serial.println("make directory");
  }
  
  Serial.print("directory exists:");
  Serial.println(SD.exists(date));
  
  int fileIndex = nowMillis / HOUR;
  Serial.println(fileIndex);
  String filename = date + "/HOUR" + String(fileIndex) + ".txt";

  writeSD(filename, outputbuf);

  Serial.println("==========================================================");
  

  delay(1 * MIN);
}


void writeSD(const String fileName, const char *input) {
    File file = SD.open(fileName, FILE_WRITE);
    file.println(input);
    file.close();
    
    Serial.println(fileName);
    Serial.println("Save SD done");

    return;
}
