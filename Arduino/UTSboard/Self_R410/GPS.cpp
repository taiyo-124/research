#include <Arduino.h>
#include <Sodaq_UBlox_GPS.h>

#define GPS_ENABLE 1

void initGps() { sodaq_gps.init(GPS_ENABLE); }

String findFix(uint32_t delay_until) {
  String s = "";
  // https://github.com/SodaqMoja/Sodaq_UBlox_GPS
  return s;
}
