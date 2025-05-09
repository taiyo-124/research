#include <Arduino.h>
#include <Sodaq_UBlox_GPS.h>


#define DEBUG 1
#define DEBUG_STREAM SerialUSB
#define GPS_ENABLE 1



void initGps() { 
  //GPS初期化
  sodaq_gps.init(GPS_ENABLE); 
//  
  #if DEBUG
    sodaq_gps.setDiag(SerialUSB);
  #endif
}

String findFix(uint32_t delay_until) {
  String s = "";
  
  #if DEBUG
    DEBUG_STREAM.println("findFix Initialaized");
  #endif
  
  if(sodaq_gps.scan(true)){
    s += String(sodaq_gps.getLat(), 5);
    s += " ";
    s += String(sodaq_gps.getLon(), 5);
  }

  #if DEBUG
    #if GET_GPS
      DEBUG_STREAM.print("LAT LON: ");
      DEBUG_STREAM.println(s);
    #endif
  #endif

    
  return s;
}
