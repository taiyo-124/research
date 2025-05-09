#include <PDM.h>
#include <SD.h>

#define SAVE_SD true

const int channels = 1;
const int samples = 16000;

const int chipselect = D10;

short sampleBuffer[512];
volatile int samplesRead;
volatile bool dataReady = false;

String filename = "sample.txt";

void setup(){

    pinMode(D10, OUTPUT);
    Serial.begin(9600);
    Serial1.begin(9600);

    delay(100);

    
    if (!PDM.begin(channels, samples)) {
        Serial.println("failed to start PDM");
        while(1);
    }

    if (SAVE_SD) {
        initSD();
    }

    PDM.onReceive(onPDMdata);

    delay(1000);
}

void loop(){
  if (samplesRead) {
    bool check_sd = writeSD(filename, sampleBuffer);
    Serial.print("WriteSD: ");
    Serial.println(check_sd);
  }

  samplesRead = 0;
}

void initSD(){
    if (!SD.begin(chipselect)){
      Serial.println("SDCard initialization failed");
        while(1);
    }
    Serial.println("SDCard initialization done");
    return;
}


boolean writeSD(const String fileName, const short *input) {
    File file = SD.open(fileName, FILE_WRITE);

    if (!file) {
        return false;
    }
    for (int i = 0; i < samplesRead; i++){
      file.println(input[i]);
    }
    file.close();

    return true;
}

void onPDMdata(){
    int bytesAvailable = PDM.available();
    PDM.read(sampleBuffer, bytesAvailable);
    samplesRead = bytesAvailable / 2;

}
