#include "SDCard.h"
#include <SD.h>
#include <SPI.h>

#define DEBUG_STREAM SerialUSB
void initSd() {
  if (!SD.begin(PIN_SPI_SS)) {
    DEBUG_STREAM.println("sdcard initialization failed.");
    while (1)
      ;
  }
  DEBUG_STREAM.println("sdcard initialization done.");
}

boolean writeSD(const String fileName, const char *input) {
  File file = SD.open(fileName, FILE_WRITE);
  if (!file) {
    return false;
  }
  file.println(input);
  file.close();
  return true;
}

String generatePath(const unsigned long millis) {
  char fileName[16]; // max length is 11 255/255.txt
  int dir = millis & 0xff;
  int file = (millis >> 8) & 0xff;
  sprintf(fileName, "%d/%d.txt", dir, file);
  return String(fileName);
}