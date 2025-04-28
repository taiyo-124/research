#include <Arduino.h>

#ifndef INQR410_H
#define INQR410_H

#define SERIAL_FORWARDER_MODE_ON 0
#define DUMMY_GPS_MODE_ON 0
#define DUMMY_BME_MODE_ON 0
#define DEBUG_STREAM_ON SERIAL_FORWARDER_MODE_ON || 1
#define TX_BATTERY_VOLT 1

#define TEMPERATURE_AND_VOLT 1

// // supported boards
// #if defined(ARDUINO_SODAQ_SARA)
/* SODAQ SARA */
#define DEBUG_STREAM SerialUSB
#define MODEM_STREAM Serial1

// Auto or Manual Searching, 0 for auto, 1 for manual
#define SEARCHING_MODE 1
// NB or CAT-M
#define NBIOT 0 // 0 for CAT-M, 1 for NB
// Note: telstra has CAT-M and NB-IoT, both tested; Vodafone only has NB-IoT

// SARA or SFF
#define BOARD_TYPE 1 // 0 for SARA, 1 for SFF

// Timeout Scheme
// #define COPS_TIMEOUT 600 // 600*300UL=180000ms=180s=3min
#define COPS_TIMEOUT 200       // 200*300UL=60000ms=60s=1min
#define GPS_TIMEOUT 10         // 180 seconds=3min
#define SLEEP_TIMEOUT 60       // 60 seconds
#define SLEEP_TIMEOUT_long 120 // deep sleep for 120s
// Airplane Mode
#define AIRPLANE_MODE 0

// Power Saving
#define POWER_SAVING 1

// Buffering
#define CACHE_SIZE 10
#define RESET_BOUNDARY 10
#define RESET_BOUNDARY_ON_OFF 20

// Unique ID
#define ID_SIZE 8
#define IMEI_SIZE 15
#define IMSI_SIZE 15

// Data-Network or Network-Data, 0 for dispatch first, 1 for connecting first
#define OPERATION_ORDER 0

// #else
// #error "Please select the SODAQ SARA as your board"
// #endif

enum class mno {
  tls_1800mhz = 0,
  tls_ctolab = 1,
  vha_900mhz = 2,
  tls_emtc_700mhz = 3,
  uae_nb_800mhz = 4,
};

// responses
enum class response {
  notfound = 0, // no response found
  ok = 1,       // OK
  error = 2,    // ERROR
  timeout = 3,  // no \n found within predefined number of attempts
  invalid = 4,  // not a valid response
};

response get_response();
void send_cmd(char const *cmd);
void check_config();
bool radio_off();
bool radio_on();
bool do_config();
void float_to_hexstr(float f, char *hex_str);
void float_to_hexstr_both(float temp_float, float volt_float, char *hex_str);
void str_to_hexstr(char *str, char *hex_str);
// bool dispatch_data(bool dummygpson, char* ID, float SN);
bool dispatch_data(bool dummygpson, char *id_str, float SN);
bool read_to_end(unsigned long timeout_s = 1000, char *expected_str = NULL);
void disable_async();
// void force_operator();
bool force_operator();
bool connect_to_network();
void getsock();
void initSensors();
bool get_gps_lock(uint32_t timeout_s, bool dummygpson = DUMMY_GPS_MODE_ON);
bool buf_is_ending(char const *str, int n = -1);
bool buf_is_begining(char const *str);

bool pre_connect();
bool send_messages(char const *ip, char const *port);
bool power_saving();
void initial_cache();
void buffering_to_cache();
void R410_Sleep();
void R410_Sleep_long(int sleepTime);
void initSleep();
void systemSleep();
void Module_Reset();
void sleep_SARA();
void sleep_SFF();
void sleep_SFF_long(int sleepTime);

void burning_ID(char *id_str);
bool get_IMEI_IMSI(char *id_str);
bool get_UTCtime(char *time_str);
void time_converted(char *time_str);

#endif
