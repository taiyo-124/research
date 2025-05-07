#include <SD.h>
#include <SPI.h>

void initSd();
boolean writeSD(const String fileName, const char *input);
String generatePath(const unsigned long millis);