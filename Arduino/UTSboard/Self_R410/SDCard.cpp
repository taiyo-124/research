#include "SDCard.h"
#include <SD.h>
#include <SPI.h>

#define DEBUG_STREAM SerialUSB
#define DEBUG 1


const int chipselect = 9;

void initSd() {
  
  if (!SD.begin(chipselect)) {
    DEBUG_STREAM.println("sdcard initialization failed.");
    while (1);
  }
  DEBUG_STREAM.println("sdcard initialization done.");
}

boolean writeSD(const String fileName, const char *input) {
  File file = SD.open(fileName, FILE_WRITE);

  #if DEBUG
    DEBUG_STREAM.print("check open: ");
    DEBUG_STREAM.println(file);
  #endif

  
  if (!file) {

    #if DEBUG
      DEBUG_STREAM.println("writeSD: false");
    #endif
    return false;
  }
  file.println(input);
  file.close();

  #if DEBUG
    DEBUG_STREAM.println("writeSD: true");
  #endif
  
  return true;
}

String generatePath(const unsigned long millis) {
  char fileName[16]; // max length is 11 255/255.txt
  char dirName[8];
  int dir = millis & 0xff;
  // SDにディレクトリを作成
  sprintf(dirName, "%d", dir);
  SD.mkdir(dirName);
  
  #if DEBUG
    DEBUG_STREAM.print("check dir: ");
    DEBUG_STREAM.println(SD.exists(dirName));
  #endif
  
  int file = (millis >> 8) & 0xff;
  sprintf(fileName, "%d/%d.txt", dir, file);
  return String(fileName);
}
