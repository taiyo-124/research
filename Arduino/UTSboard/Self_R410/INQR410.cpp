#include "INQR410.h"
#include <Adafruit_BME680.h>
#include <Adafruit_Sensor.h>
#include <Sodaq_UBlox_GPS.h>
#include <Sodaq_wdt.h>
#include <Wire.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// #define BUFLEN 1024
// #define READGIVEUP 100

// #define ADC_AREF 3.3
// #define BATVOLT_R1 4.7f
// #define BATVOLT_R2 10.0f
// #define BATVOLT_PIN BAT_VOLT

// char buf[BUFLEN + 1];
// char buf1[BUFLEN + 1];
// #define SOKLEN 10
// char sok[SOKLEN + 1]; // assuming socket identifier needs less than 10 chars
// char gpsstr[BUFLEN + 1];
// char tmpstr[BUFLEN + 1];
// int udp_data_len;

// // buffering
// char* cache[CACHE_SIZE];
// MyQueue *queue;
// cached* data = (cached*)malloc(sizeof(cached)*CACHE_SIZE);

#define SEALEVELPRESSURE_HPA (1013.25)

Adafruit_BME680 bme; // I2C

// #if NBIOT
// mno select_mno = mno::vha_900mhz;
// #else
// mno select_mno = mno::tls_emtc_700mhz;
// #endif

// const char *nodeid = "2";

// bool buf_is_ending(char const *str, int n) {
//   int str_len = strlen(str);
//   int buf_len;
//   if (n == -1) {
//     buf_len = strlen(buf);
//   } else {
//     buf_len = n;
//   }
//   if (buf_len < str_len) {
//     return false;
//   }
//   for (int i = 0; i < str_len; i++) {
//     if (buf[buf_len - 1 - i] != str[str_len - 1 - i]) {
//       return false;
//     }
//   }
//   return true;
// }

// bool buf_is_begining(char const *str) {
//   int str_len = strlen(str);
//   int buf_len = strlen(buf);
//   if (buf_len < str_len) {
//     return false;
//   }
//   for (int i = 0; i < str_len; i++) {
//     if (buf[i] != str[i]) {
//       return false;
//     }
//   }
//   return true;
// }
// bool buf_is_middle(char const *str, int start_from) {
//   int str_len = strlen(str);
//   int buf_len = strlen(buf);
//   if (buf_len < str_len + start_from) {
//     return false;
//   }
//   for (int i = 0; i < str_len; i++) {
//     if (buf[i + start_from] != str[i]) {
//       return false;
//     }
//   }
//   return true;
// }
// bool buf_is_middle_fixed_size(char *str, int size, int start_from) {
//   int buf_len = strlen(buf);
//   if (buf_len < size + start_from) {
//     return false;
//   }
//   strncpy(str, buf + start_from, size);
//   return true;
// }

// response get_response() {
//   if (!MODEM_STREAM.available()) {
//     return response::notfound;
//   }
//   int j = 0;
//   for (int i = 0; i < READGIVEUP; i++) {
//     // if nothing is available try again
//     if (!MODEM_STREAM.available()) {
//       delay(10);
//       continue;
//     }
//     // if buffer is not large enough, keep the last 10 chars and wrap
//     if (j == BUFLEN) {
//       // DEBUG_STREAM.write('.');
//       for (int k = 0; k < 10; k++) {
//         buf[k] = buf[BUFLEN - 10 + k];
//       }
//       j = 0;
//     }
//     // read
//     buf[j++] = MODEM_STREAM.read();
//     DEBUG_STREAM.write(buf[j - 1]);
//     if (buf[j - 1] == '\n') {
//       break;
//     }
//   }
//   buf[j] = '\0';

//   // if expected_reponse is not given
//   if (buf_is_ending("OK")) {
//     DEBUG_STREAM.println("gotok");
//     return response::ok;
//   } else if (buf_is_ending("ERROR")) {
//     DEBUG_STREAM.println("goterror");
//     return response::error;
//   } else {
//     return response::invalid;
//   }
// }

// bool read_to_end(uint32_t timeout_s, char *expected_str) {
//   // DEBUG_STREAM.println("start timer!!!");
//   unsigned long t0 = millis();
//   int j = 0;
//   buf[j] = '\0';

//   while (j < BUFLEN) {
//     if (millis() - t0 > 300UL * timeout_s) { // 300 is the timeout-based
//       buf[j] = '\0';
//       DEBUG_STREAM.println("timeout");
//       return false;
//     }
//     if (!MODEM_STREAM.available()) {
//       delay(10);
//       continue;
//     }
//     buf[j++] = MODEM_STREAM.read();
// #if DEBUG_STREAM_ON
//     DEBUG_STREAM.write(buf[j - 1]);
// #endif
//     buf[j] = '\0';
//     if (expected_str != NULL && buf_is_ending(expected_str, j)) {
//       // DEBUG_STREAM.println("got expected");
//       return true;
//     }
//     if (expected_str == NULL &&
//         (buf_is_ending("OK\r\n", j) || buf_is_ending("RDY\r\n", j))) {
//       // DEBUG_STREAM.println("got ok/rdy");
//       return true;
//     }
//     if (expected_str == NULL && (buf_is_ending("ERROR\r\n", j))) {
//       // DEBUG_STREAM.println("got error");
//       return false;
//     }
//     if (expected_str == NULL && (buf_is_ending("no network service\r\n", j)))
//     {
//       DEBUG_STREAM.println("got no network service");
//       return false;
//     }
//     if (expected_str == NULL && (buf_is_ending("not allowed\r\n", j))) {
//       DEBUG_STREAM.println("got operation not allowed");
//       return false;
//     }
//     if (expected_str == NULL && (buf_is_ending("not allowed\r\n", j))) {
//       DEBUG_STREAM.println("got operation not allowed");
//       return false;
//     }
//     if (expected_str == NULL && (buf_is_ending("not supported\r\n", j))) {
//       DEBUG_STREAM.println("got operation not supported");
//       // return false;
//       Module_Reset();
//     }
//     if (expected_str == NULL &&
//         (buf_is_ending("No connection to phone\r\n", j))) {
//       DEBUG_STREAM.println("got no connection to phone");
//       // return false;
//       Module_Reset();
//     }
//     if (expected_str == NULL && (buf_is_ending("SIM failure\r\n", j))) {
//       DEBUG_STREAM.println("got sim failure");
//       Module_Reset();
//     }
//   }
//   if (j >= BUFLEN) {
// #if DEBUG_STREAM_ON
//     DEBUG_STREAM.println("read buffer overflow, increase BUFLEN");
// #endif
//     exit(1);
//   }
// }

// // read to OK/ERROR, this is blocking
// bool match_to_end(char const *expected_response) {
//   // DEBUG_STREAM.println("match_to_end");
//   int j = 0;
//   buf[j] = '\0';
//   while (j < BUFLEN) {
//     if (!MODEM_STREAM.available()) {
//       delay(10);
//       continue;
//     }
//     buf[j++] = MODEM_STREAM.read();
// #if DEBUG_STREAM_ON
//     DEBUG_STREAM.write(buf[j - 1]);
// #endif
//     buf[j] = '\0';
//     if (buf_is_ending(expected_response, j)) {
//       // DEBUG_STREAM.println("match");
//       return true;
//     }
//     if (buf_is_ending("OK\r\n", j) || buf_is_ending("ERROR\r\n", j)) {
//       DEBUG_STREAM.println("nomatch-response ended");
//       return false;
//     }
//   }
//   if (j >= BUFLEN) {
//     DEBUG_STREAM.println("read buffer overflow, increase BUFLEN");
//     exit(1);
//   }
// }

// void match_to_end_exitnomatch(char const *expected_response) {
//   if (!match_to_end(expected_response)) {
//     DEBUG_STREAM.println("expected result not found");
//     exit(1);
//   }
// }

// void send_cmd(char const *cmd) {
//   int cmd_len = strlen(cmd);
//   // DEBUG_STREAM.print("CMD:");
//   for (int i = 0; i < cmd_len; i++) {
//     MODEM_STREAM.write(cmd[i]);
//     // DEBUG_STREAM.write(cmd[i]);
//   }
//   MODEM_STREAM.write('\r');
//   MODEM_STREAM.write('\n');
// }

// // void do_config()
// //  at+nconfig ...
// //  at+cops=0,2,50503 (will give an error, ignore) -> at+nrb

// void check_config() {
//   // send_cmd("at+nconfig?");
//   //
//   match_to_end_exitnomatch("+NCONFIG:AUTOCONNECT,TRUE\r\n+NCONFIG:CR_0354_0338_SCRAMBLING,TRUE\r\n+NCONFIG:CR_0859_SI_AVOID,TRUE\r\n\r\nOK\r\n");
//   for (int i = 0; i < SOKLEN; i++) {
//     sok[i] = '\0';
//   }
// #if DEBUG_STREAM_ON
//   DEBUG_STREAM.println("check config");
// #endif
// }

// void disable_async() {
//   send_cmd("at+nsmi=0");
//   match_to_end_exitnomatch("OK\r\n");
// }

// bool radio_off() {
//   int count = 0;
//   send_cmd("at+cfun=0");
//   // match_to_end_exitnomatch("OK\r\n");
//   //  while(!read_to_end(2)){
//   //    #if DEBUG_STREAM_ON
//   //      DEBUG_STREAM.println("radio turn off fail");
//   //      count++;
//   //    #endif
//   //    if (count >= RESET_BOUNDARY_ON_OFF) {
//   //      #if DEBUG_STREAM_ON
//   //        DEBUG_STREAM.println("jump out of radio off");
//   //      #endif
//   //      // #if BOARD_TYPE
//   //      //   Module_Reset();
//   //      // #else
//   //      //   return false;
//   //      // #endif
//   //      return false;
//   //    }
//   //    delay(1000);
//   //    send_cmd("at+cfun=0");
//   //  }
//   return true;
// }

// bool radio_on() {
//   int count = 0;
//   send_cmd("at+cfun=1");
//   // match_to_end_exitnomatch("OK\r\n");
//   while (!read_to_end(2)) {
// #if DEBUG_STREAM_ON
//     DEBUG_STREAM.println("radio turn on fail");
//     count++;
// #endif
//     if (count >= RESET_BOUNDARY_ON_OFF) {
// #if DEBUG_STREAM_ON
//       DEBUG_STREAM.println("jump out of radio on");
// #endif
//       // #if BOARD_TYPE
//       //   Module_Reset();
//       // #else
//       //   return false;
//       // #endif
//       return false;
//     }
//     delay(1000);
//     send_cmd("at+cfun=1");
//   }
//   return true;
// }

// // void force_operator() {
// bool force_operator() {
// #if SEARCHING_MODE
// #if NBIOT
//   send_cmd("at+cops=1,2,\"50503\""); // Vodafone AU
// #else
//   send_cmd("at+cops=1,2,\"50501\""); // Telstra
// #endif
// #else
//   send_cmd("at+cops=0,0"); // Auto searching
// #endif

//   if (!read_to_end(COPS_TIMEOUT))
//     return false; // 3 min
//   // match_to_end_exitnomatch("OK\r\n");
//   send_cmd("at+cereg=2");
//   if (!read_to_end()) {
// #if DEBUG_STREAM_ON
//     DEBUG_STREAM.println("could not enable network location");
// #endif
//     return false;
//   }
//   return true;
// }

// bool do_config() {
// #if NBIOT
//   send_cmd("at+urat=8"); // NB
// #else
//   send_cmd("at+urat=7");   // CAT-M
// #endif

//   if (!read_to_end())
//     return false;
//   if (select_mno == mno::tls_1800mhz) {
//     send_cmd("at+umnoprof=4");
//     if (!read_to_end())
//       return false;
//     send_cmd("at+ubandmask=0,0"); // no band for cat m
//     if (!read_to_end())
//       return false;
//     send_cmd("at+ubandmask=1,4"); // band 3 for NB
//     if (!read_to_end())
//       return false;
//     delay(100);
//     send_cmd("at+cgdcont=1,\"IP\",\"telstra.internet\""); // Telstra
//     production
//                                                           // network
//     if (!read_to_end())
//       return false;
//     send_cmd("at+cfun=15");
//     delay(5000);
//     if (!read_to_end())
//       return false;
//   } else if (select_mno == mno::vha_900mhz) {
//     send_cmd("at+umnoprof=0");
//     if (!read_to_end())
//       return false;
//     send_cmd("at+ubandmask=0,0"); // no band for cat m
//     if (!read_to_end())
//       return false;
//     send_cmd("at+ubandmask=1,128"); // band 8 for NB
//     if (!read_to_end())
//       return false;
//     send_cmd("at+cgdcont=1,\"IP\",\"spe.inetd.vodafone.nbiot\""); // Vodafond
//                                                                   //
//                                                                   production
//                                                                   // network
//     if (!read_to_end())
//       return false;
//     delay(5000);
//   } else if (select_mno == mno::tls_emtc_700mhz) {
//     send_cmd("at+umnoprof=4");
//     if (!read_to_end())
//       return false;
//     send_cmd("at+ubandmask=0,134217728"); // band 28 for cat m
//     if (!read_to_end())
//       return false;
//     send_cmd("at+ubandmask=1,0"); // no band for NB
//     if (!read_to_end())
//       return false;
//     delay(100);
//     //    send_cmd("at+cgdcont=1,\"IP\",\"hologram\",,0,0,1");// Hologram APN
//     send_cmd("at+cgdcont=1,\"IP\",\"telstra.internet\"");
//     if (!read_to_end())
//       return false;
//     send_cmd("at+cfun=15");
//     delay(5000);
//     if (!read_to_end())
//       return false;
//   } else if (select_mno == mno::uae_nb_800mhz) {
//     send_cmd("at+umnoprof=0");
//     if (!read_to_end())
//       return false;
//     send_cmd("at+ubandmask=0,0"); // no band for cat m
//     if (!read_to_end())
//       return false;
//     send_cmd("at+ubandmask=1,524288"); // band 20 for NB
//     if (!read_to_end())
//       return false;
//     delay(100);
//     send_cmd(
//         "at+cgdcont=1,\"IP\",\"etisalat.ae\""); // Etisalat production
//         network
//     if (!read_to_end())
//       return false;
//     delay(5000);
//   }
//   return true;
// }

// void sleep_blink(int milisec, int on_milisec = 20, int off_milisec = 230) {
//   for (int i = 0; i < (milisec / (on_milisec + off_milisec)) + 1; i++) {
// #if BOARD_TYPE
//     digitalWrite(LED_GREEN, HIGH);
//     delay(on_milisec);
//     digitalWrite(LED_GREEN, LOW);
//     delay(off_milisec);
// #else
//     digitalWrite(LED_BUILTIN, HIGH);
//     delay(on_milisec);
//     digitalWrite(LED_BUILTIN, LOW);
//     delay(off_milisec);
// #endif
//   }
// }

// bool connect_to_network() {
//   send_cmd("at+cops?");
//   if (!read_to_end())
//     return false;
//   if (buf_is_middle("+cops: 1,0,\"", 11))
//     return false; // unknown error
//   unsigned long checkpoint = millis();
// #if !SEARCHING_MODE
//   if (!buf_is_middle("+cops: 0,0,\"", 11)) {
//     send_cmd("at+cops=0,0");
//     if (!read_to_end(COPS_TIMEOUT))
//       return false;
//     // while(!read_to_end(.23)) { // got stuck, why .23
//     while (!read_to_end(2)) {
//       if (millis() - checkpoint > 300UL * COPS_TIMEOUT) {
// #if DEBUG_STREAM_ON
//         DEBUG_STREAM.println("timeout in connect_to_network");
// #endif
//         return false;
//       }
//       sleep_blink(1000);
//     }
//   }
// #else
//   if (select_mno == mno::tls_1800mhz) {
//     if (!buf_is_middle("+cops: 1,2,\"50501\",8", 11)) {
//       send_cmd("at+cops=1,2,\"50501\"");
//       if (!read_to_end(COPS_TIMEOUT))
//         return false;
//       // while(!read_to_end(.23)) { // got stuck, why .23
//       while (!read_to_end(2)) {
//         if (millis() - checkpoint > 300UL * COPS_TIMEOUT) {
// #if DEBUG_STREAM_ON
//           DEBUG_STREAM.println("timeout in connect_to_network");
// #endif
//           return false;
//         }
//         sleep_blink(1000);
//       }
//     }
//   } else if (select_mno == mno::vha_900mhz) {
//     if (!buf_is_middle("+cops: 1,2,\"50503\",9", 11)) {
//       send_cmd("at+cops=1,2,\"50503\"");
//       if (!read_to_end(COPS_TIMEOUT))
//         return false;
//       // while(!read_to_end(.23)) {
//       while (!read_to_end(2)) {
//         if (millis() - checkpoint > 300UL * COPS_TIMEOUT) {
// #if DEBUG_STREAM_ON
//           DEBUG_STREAM.println("timeout in connect_to_network");
// #endif
//           return false;
//         }
//         sleep_blink(1000);
//       }
//     }
//   } else if (select_mno == mno::tls_emtc_700mhz) {
//     if (!buf_is_middle("+cops: 1,2,\"50501\",8",
//                        11)) { // 8 for LTE CAT-M1 with R410M
//       send_cmd("at+cops=1,2,\"50501\"");
//       if (!read_to_end(COPS_TIMEOUT))
//         return false;
//       // while(!read_to_end(.23)) { // got stuck, why .23
//       while (!read_to_end(2)) {
//         if (millis() - checkpoint > 300UL * COPS_TIMEOUT) {
// #if DEBUG_STREAM_ON
//           DEBUG_STREAM.println("timeout in connect_to_network");
// #endif
//           return false;
//         }
//         sleep_blink(1000);
//       }
//     }
//   }
// #endif
//   return true;
// }

// void getsock() {
//   if (sok[0] == '\0') {
//     delay(1000);
//     send_cmd("at+usocr=17"); // create sockets
//     while (!read_to_end()) {
// #if DEBUG_STREAM_ON
//       DEBUG_STREAM.println("could not create socket");
// #endif
//       delay(1000);
//       send_cmd("at+usocr=17");
//     }
//     /*
//     DEBUG_STREAM.println(buf);
//     int i;
//     int buflen = strlen(buf);
//     //... 0 \r \n \r \n O K \r \n --> buflen-9
//     for (i=0; i<SOKLEN && buf[buflen-9-i]!='\n'; i++){ //reverse order save
//       sok[i] = buf[buflen-9-i];
//     }
//     sok[i]='\0';
//     int soklen = strlen(sok);
//     for (i=0; i<soklen/2; i++){ //correct the order
//       char c = sok[i];
//       sok[i] = sok[soklen-1-i];
//       sok[soklen-1-i] = c;
//     }
//     */
//     sok[0] = buf[22]; //+USOCR: 0 ???
// #if DEBUG_STREAM_ON
//                       // DEBUG_STREAM.print("check buf[]: ");
//     // DEBUG_STREAM.println(buf);
//     // DEBUG_STREAM.println(buf[22]);
//     DEBUG_STREAM.print("created socket: ");
//     DEBUG_STREAM.println(sok);
// #endif
//   }
// }

// void float_to_hexstr(float f, char *hex_str) {
//   unsigned char *ch = (unsigned char *)&f;
//   sprintf(hex_str, "%02X%02X%02X%02X", ch[3], ch[2], ch[1], ch[0]);
//   // DEBUG_STREAM.print(hex_str);
// }

// void float_to_hexstr_both(float temp_float, float volt_float, char *hex_str)
// {
//   unsigned char *ch1 = (unsigned char *)&temp_float;
//   unsigned char *ch2 = (unsigned char *)&volt_float;
//   sprintf(hex_str, "%02X%02X%02X%02X,%02X%02X%02X%02X", ch1[3], ch1[2],
//   ch1[1],
//           ch1[0], ch2[3], ch2[2], ch2[1], ch2[0]);
// }

// void str_to_hexstr(char *str, char *hex_str) {
//   sprintf(hex_str, "%02X%02X%02X%02X,%02X%02X%02X%02X", str[7], str[6],
//   str[5],
//           str[4], str[3], str[2], str[1], str[0]);
// }

// float readbattery() {
//   float voltage = (float)((ADC_AREF / 1.023) * (BATVOLT_R1 + BATVOLT_R2) /
//                           BATVOLT_R2 * (float)analogRead(BATVOLT_PIN));
//   return voltage;
// }

// bool pre_connect() {
//   if (!radio_on()) { // directly exit to prevent from awaiting the timeout of
//                      // force_operator()
//     return false;
//   }
//   if (!force_operator())
//     return false;

// // Power Saving Mode
// #if POWER_SAVING
//   if (!power_saving())
//     return false;
// #endif

// // digitalWrite(LED_BUILTIN, LOW);
// #if DEBUG_STREAM_ON
//   if (DUMMY_GPS_MODE_ON) {
//     DEBUG_STREAM.println(
//         "WARNING: GPS receiver is active, but using a dummy location only");
//   }
//   DEBUG_STREAM.println("--ENDSETUP--");
// #endif
//   return true;
// }

// // bool dispatch_data(bool dummygpson, char* ID, float SN){
// bool dispatch_data(bool dummygpson, char *id_str, float SN) {
//   //  // Create sockets
//   //  getsock();
//   //  if (sok[0] == '\0') {
//   //    DEBUG_STREAM.println("sok is slash 0");
//   //  } else if (sok[0] == '0') {
//   //    DEBUG_STREAM.println("sok is 0");
//   //  }
//   //  DEBUG_STREAM.println(strlen(sok));
//   DEBUG_STREAM.print("try to get UTC time");

//   char time_str[30];
//   if (!get_UTCtime(time_str)) {
//     DEBUG_STREAM.print("Fail to get UTCtime");
//     get_gps_lock(GPS_TIMEOUT, dummygpson);
//     //    sprintf(buf1, time_str);
//     sprintf(buf1, gpsstr);
//     DEBUG_STREAM.print("gpsstr: ");
//     DEBUG_STREAM.println(gpsstr);
//     DEBUG_STREAM.print("udp_data_len: ");
//     DEBUG_STREAM.println(udp_data_len);
//     DEBUG_STREAM.println(time_str);
//     //    strcat(buf1, time_str);
//   } else {
//     DEBUG_STREAM.print("Got UTCtime");
//     udp_data_len = strlen(time_str);
//     DEBUG_STREAM.print("time_str: ");
//     DEBUG_STREAM.println(time_str);
//     DEBUG_STREAM.print("udp_data_len: ");
//     DEBUG_STREAM.println(udp_data_len);
//     sprintf(buf1, time_str);
//   }
//   return 1;

//   const int nread = 5;
//   float temp = 0;
//   float humid = 0;
//   float alti = 0;
// #if DUMMY_BME_MODE_ON
// #if DEBUG_STREAM_ON
//   DEBUG_STREAM.print("Use dummy sensor");
// #endif
//   temp = 30.00;
//   humid = 30.00;
//   alti = 30.00;
// #else

//   for (int i = 0; i < nread; i++) {
//     temp += bme.readTemperature();
//     humid += bme.readHumidity();
//     alti += bme.readAltitude(SEALEVELPRESSURE_HPA);
//     // sleep_blink(1000,20,60);
//   }
//   temp = temp / nread;
//   humid = humid / nread;
//   alti = alti / nread;
// #if DEBUG_STREAM_ON
//   DEBUG_STREAM.print("Use real sensor");
//   DEBUG_STREAM.print("temp: ");
//   DEBUG_STREAM.println(temp);
// #endif
// #endif

//   char humid_str[8]; // float - 4 bytes
//   // sprintf(buf1, gpsstr);

//   char id_sn_str[28];
//   //  char id_str[20];
//   char sn_str[8];
//   float_to_hexstr(SN, sn_str);
//   get_IMEI_IMSI(id_str);
//   // sprintf(id_sn_str, "%s,%s,",ID, sn_str);
//   sprintf(id_sn_str, "%s,%s,", id_str, sn_str);
//   DEBUG_STREAM.println("check id here");
//   DEBUG_STREAM.println(id_sn_str);
//   DEBUG_STREAM.println(buf1);
//   strcat(buf1, id_sn_str);

// #if TEMPERATURE_AND_VOLT
//   DEBUG_STREAM.println("We are now in tem and vol");
//   char temp_battery_str[17];
//   float battery_volt = readbattery();
//   float_to_hexstr_both(temp, battery_volt, temp_battery_str);
//   strcat(buf1, temp_battery_str);
// #else
//   DEBUG_STREAM.println("We are now need to choose either tem or vol");
// #if TX_BATTERY_VOLT
//   DEBUG_STREAM.println("Only vol");
//   char battery_str[8];
//   float battery_volt = readbattery();
//   float_to_hexstr(battery_volt, battery_str);
//   strcat(buf1, battery_str);
// #else
//   DEBUG_STREAM.println("Only temp");
//   char temp_str[8]; // float - 4 bytes
//   float_to_hexstr(temp, temp_str);
//   strcat(buf1, temp_str);
// #endif
//   // buf1[udp_data_len] = '\0'; // to end the buf1
// #endif

// #if AIRPLANE_MODE
// #if DEBUG_STREAM_ON
//   DEBUG_STREAM.print("altitude: ");
//   DEBUG_STREAM.println(alti);
// #endif
//   if (alti > 1000) {
//     radio_off();
//     return false;
//   }
// #endif
//   return true;
// }

// bool send_messages(char const *ip, char const *port) {
//   getsock();
//   if (sok[0] == '\0') {
//     DEBUG_STREAM.println("sok is slash 0");
//   } else if (sok[0] == '0') {
//     DEBUG_STREAM.println("sok is 0");
//   }
//   DEBUG_STREAM.println(strlen(sok));
//   // send the older data first
//   int count = 0;
//   while (myListGetSize(queue)) {
// #if DEBUG_STREAM_ON
//     DEBUG_STREAM.println("Send the older message firstly");
// #endif
//     // fetch data from the queue
//     char *message;
//     // message = (char*)malloc(150*sizeof(char));
//     // strcpy(message, (char*) myQueueGetTop(queue));
//     message = (char *)myQueueGetTop(queue);
//     // send data

//     sprintf(buf, "at+usost=%s,\"%s\",%s,%d,\"%s\"", sok, ip, port,
//             strlen(message), message);
//     send_cmd(buf); // exe the cmd
//     if (!read_to_end())
//       return false;
//     myQueueRemove(queue);
//     free(message);
//     count++;
//   }
// #if DEBUG_STREAM_ON
//   DEBUG_STREAM.print("old message: ");
//   DEBUG_STREAM.println(count);
// #endif
//   // // send data
//   DEBUG_STREAM.println(udp_data_len);
//   DEBUG_STREAM.println(strlen(buf1));
//   DEBUG_STREAM.println(buf1);
// #if TEMPERATURE_AND_VOLT
// #if DEBUG_STREAM_ON
//   DEBUG_STREAM.println("Temp and Vol enabled");
// #endif
//   sprintf(buf, "at+usost=%s,\"%s\",%s,%d,\"%s\"", sok, ip, port,
//   strlen(buf1),
//           buf1);
// #else
//   // sprintf(buf,"at+usost=%s,\"%s\",%s,%d,\"%s\"",sok,ip,port,udp_data_len +
//   //    8, buf1);
//   sprintf(buf, "at+usost=%s,\"%s\",%s,%d,\"%s\"", sok, ip, port,
//   strlen(buf1),
//           buf1);
// #endif
//   send_cmd(buf); // exe the cmd
//   if (!read_to_end())
//     return false;
//   // Create the message
//   // String message = String(temp) + "C" +
//   // " " + String(humid) + "% - ";
//   //+ temp_str+" "+humid_str;
//   // Print the message we want to send
//   // DEBUG_STREAM.println(message);
//   sprintf(buf, "at+usocl=%s", sok); // close sockets
//   send_cmd(buf);
//   check_config();   // clear socket buffer
//   read_to_end(400); // 120s
//   sleep_blink(500, 20, 230);

//   return true;
// }

// /*!
//  * Find a GPS fix, timeout in seconds
//  */
// bool get_gps_lock(uint32_t timeout_s, bool dummygpson) {
//   uint32_t start = millis();
//   uint32_t timeout = timeout_s * 1000L;
//   char date_str[9], time_str[7], lat_str[12], lon_str[12];
//   double getLat, getLon;
// #if DEBUG_STREAM_ON
//   DEBUG_STREAM.println(String("waiting for fix ..., timeout=") + timeout +
//                        String("ms"));
// #endif
//   if (dummygpson) {
//     // sprintf(gpsstr, "NID-vha-3,31277,035932.0,3352.4033S,15111.9333E,");
//     String a = "00000000000000";
//     strncpy(date_str, a.c_str(), 8);
//     date_str[8] = '\0';
//     strncpy(time_str, a.c_str() + 8, 6);
//     time_str[6] = '\0';
//     getLat = -33.8219157;
//     getLon = 151.0944987;
//     // sprintf(gpsstr,
//     // "NID-vha-3,%s,%s,%3.7f,%3.7f,",date_str,time_str,getLat,getLon);
//     // sprintf(gpsstr, "NID-vha-3,%s,%s,",date_str,time_str);
//     sprintf(gpsstr, "%s,%s,%3.7f,%3.7f,", date_str, time_str, getLat,
//     getLon);
// #if DEBUG_STREAM_ON
//     // DEBUG_STREAM.println(gpsstr);
//     DEBUG_STREAM.println("Dummy GPS mode");
// #endif
//     udp_data_len = strlen(gpsstr);
//     // #if DEBUG_STREAM_ON
//     //   DEBUG_STREAM.println("check str in get_gps()");
//     //   DEBUG_STREAM.println(gpsstr);
//     // #endif
//     return true;
//   } else if (sodaq_gps.scan(false, timeout)) { // set to false to switch off
//   the
//                                                // gps at the end of each scan
//     String message = "NID-vha-3";
//     message +=
//         sodaq_gps
//             .getDateTimeString(); // need to seperate the date and time later
//     message += String(",") + String(sodaq_gps.getLat(), 7);
//     message += String(",") + String(sodaq_gps.getLon(), 7);
//     message += String(",");

//     // strncpy(gpsstr, message.c_str(), sizeof(gpsstr));
//     strncpy(date_str, sodaq_gps.getDateTimeString().c_str(), 8);
//     date_str[8] = '\0';
//     strncpy(time_str, sodaq_gps.getDateTimeString().c_str() + 8, 6);
//     time_str[6] = '\0';
//     getLat = sodaq_gps.getLat();
//     getLon = sodaq_gps.getLon();
//     // sprintf(lat_str, "%3.7",sodaq_gps.getLat());
//     // sprintf(lon_str, "%3.7",sodaq_gps.getLon());
//     // sprintf(gpsstr,
//     // "NID-vha-3,%s,%s,%3.7f,%3.7f,",date_str,time_str,getLat,getLon);
//     // sprintf(gpsstr, "NID-vha-3,%s,%s,",date_str,time_str);
//     sprintf(gpsstr, "%s,%s,%3.7f,%3.7f,", date_str, time_str, getLat,
//     getLon); gpsstr[sizeof(gpsstr) - 1] = '\0';

// #if DEBUG_STREAM_ON
//     DEBUG_STREAM.println(gpsstr);
//     message +=
//         (String(" time to find fix: ") + (millis() - start) + String("ms"));
//     message += (String(" datetime = ") + sodaq_gps.getDateTimeString());
//     message += (String(" lat = ") + String(sodaq_gps.getLat(), 7));
//     message += (String(" lon = ") + String(sodaq_gps.getLon(), 7));
//     message +=
//         (String(" num sats = ") + String(sodaq_gps.getNumberOfSatellites()));
//     // DEBUG_STREAM.println(message);
// #endif
//     udp_data_len = strlen(gpsstr);
//     return true;
//   } else {
// #if DEBUG_STREAM_ON
//     DEBUG_STREAM.println("No GPS Fix");
// #endif
//     // return false; // for demo use
//     // sprintf(gpsstr, "NID-vha-3,31277,035932.0,3352.4033S,15111.9333E,");
//     String a = "00000000000000";
//     strncpy(date_str, a.c_str(), 8);
//     date_str[8] = '\0';
//     strncpy(time_str, a.c_str() + 8, 6);
//     time_str[6] = '\0';
//     getLat = 0.0000000;
//     getLon = 0.0000000;
//     // sprintf(lat_str, "%3.7",sodaq_gps.getLat());
//     // sprintf(lon_str, "%3.7",sodaq_gps.getLon());
//     //  sprintf(gpsstr,
//     //  "NID-vha-3,%s,%s,%3.7f,%3.7f,",date_str,time_str,getLat,getLon);
//     //  sprintf(gpsstr, "NID-vha-3,%s,%s,",date_str,time_str);
//     sprintf(gpsstr, "%s,%s,%3.7f,%3.7f,", date_str, time_str, getLat,
//     getLon);
// #if DEBUG_STREAM_ON
//     // DEBUG_STREAM.println(gpsstr);
//     DEBUG_STREAM.println("Dummy GPS mode when failing to retrieve GPS
//     signal");
// #endif
//     udp_data_len = strlen(gpsstr);
//     return false;
//   }
//   sleep_blink(200, 20, 100);
//   delay(5000);
//   sleep_blink(200, 20, 100);
// }

void initSensors() {
#if !DUMMY_BME_MODE_ON
  while (!bme.begin(0x76)) {
    DEBUG_STREAM.println("Could not find a valid BME680 sensor, check wiring!");
    // sleep_blink(2000);
    delay(1000);
  }
#endif
#if DEBUG_STREAM_ON
  DEBUG_STREAM.println("init temp humid sensor success");
#endif
  // power conservation
  // sodaq_gps.init(GPS_ENABLE);
  // sodaq_gps.setDiag(DEBUG_STREAM); // comment to reduce debug info
}

// bool power_saving() {
//   send_cmd("at+cpsms=1,,,\"01100000\",\"00000000\"");
//   if (!read_to_end(40))
//     return false; // 12s
// // while(!read_to_end()){
// //   delay(100);
// //   send_cmd("at+cpsms=1,,,\"01100000\",\"00000000\"");
// // }
// #if DEBUG_STREAM_ON
//   send_cmd("at+cpsms?");
//   if (!read_to_end(40))
//     return false; // 12s
//                   // if(!read_to_end()) {
//                   //   delay(100);
//                   //   send_cmd("at+cpsms?");
//                   // }
// #endif
//   return true;
// }

// void initial_cache() {
// #if DEBUG_STREAM_ON
//   DEBUG_STREAM.println("Initial the cache");
// #endif
//   queue = createMyQueue();
// }

// void free_cache() {
// #if DEBUG_STREAM_ON
//   DEBUG_STREAM.println("Free the cache");
// #endif
//   freeMyQueue(queue);
// }

// void buffering_to_cache() {
//   if (myListGetSize(queue) == CACHE_SIZE) {
// #if DEBUG_STREAM_ON
//     DEBUG_STREAM.println("Cache is full, pop the oldest");
// #endif
//     char *removed = (char *)myQueueRemove(queue);
//     free(removed);
//     // cached* remove_ele = myQueueRemove(queue);
//     // #if DEBUG_STREAM_ON
//     //   DEBUG_STREAM.println("%c", *remove_ele);
//     // #endif
//   }
// #if DEBUG_STREAM_ON
//   DEBUG_STREAM.println("Push to cache: ");
//   DEBUG_STREAM.println(buf1);
// #endif
//   char *push_ele;
//   // push_ele = buf1;
//   push_ele = (char *)malloc(150 * sizeof(char));
//   if (push_ele == NULL) {
//     return;
//   }
//   strcpy(push_ele, buf1);

//   myQueueAdd(queue, push_ele);
//   // data[0].message = buf1;
//   // data[0].datalen = udp_data_len;
//   // myQueueAdd(queue, &data[0]);
//   // data->message = buf1;
//   // data->datalen = udp_data_len;
//   // myQueueAdd(queue, data);
// }

// void R410_Sleep_long(int sleepTime) {
// // #if DEBUG_STREAM_ON
// //   DEBUG_STREAM.println("--START SLEEP--");
// // #endif
// #if BOARD_TYPE
//   sleep_SFF_long(sleepTime);
// #else
//   sleep_SARA();
// #endif

// #if DEBUG_STREAM_ON
//   DEBUG_STREAM.println("--AWAKE UP--");
// #endif
// }

// void R410_Sleep() {
// #if DEBUG_STREAM_ON
//   DEBUG_STREAM.println("--START SLEEP--");
// #endif
// #if BOARD_TYPE
//   sleep_SFF();
// #else
//   sleep_SARA();
// #endif

// #if DEBUG_STREAM_ON
//   DEBUG_STREAM.println("--AWAKE UP--");
// #endif
// }

/**
 * Initializes the CPU sleep mode.
 */
// void initSleep() {
//   DEBUG_STREAM.println("initSleep");
//   // Set the sleep mode
//   SCB->SCR |= SCB_SCR_SLEEPDEEP_Msk;
// }

/**
 * Powers down all devices and puts the system to deep sllep.
 */
// void systemSleep() {
//   __WFI(); // SAMD sleep
// }

// void Module_Reset() {
// #if DEBUG_STREAM_ON
//   DEBUG_STREAM.println("--RESET--");
// #endif
//   sodaq_wdt_enable(WDT_PERIOD_2X); // ~2s
//   while (true)
//     ;
// }

// void RF_Reset() {
// #if !BOARD_TYPE
//   pinMode(SARA_RESET, OUTPUT);
//   digitalWrite(SARA_RESET, LOW);
//   delay(100);
//   digitalWrite(SARA_RESET, HIGH);
//   delay(5000);
// #else
//   delay(5000);
// #endif
// }

// void network_register() {
// #if !BOARD_TYPE
//   digitalWrite(SARA_ENABLE, HIGH);
//   RF_Reset();
//   digitalWrite(SARA_R4XX_TOGGLE, LOW);
//   digitalWrite(SARA_TX_ENABLE, HIGH);
//   digitalWrite(LED_BUILTIN, HIGH);
//   // while(1) {
//   //   if(do_config()) break; // succeed
//   //   delay(100); // faster because the RF is off now
//   // }
// #else
//   digitalWrite(SARA_ENABLE, HIGH);
//   RF_Reset();
//   digitalWrite(SARA_R4XX_TOGGLE, LOW);
//   digitalWrite(LED_GREEN, HIGH);
// #endif
// #if DEBUG_STREAM_ON
//   DEBUG_STREAM.println("network_register");
// #endif
// }

// void sleep_SARA() {
// #if !BOARD_TYPE
//   int count = 0;
//   sodaq_wdt_enable(WDT_PERIOD_8X); // ~8s

//   digitalWrite(SARA_TX_ENABLE, LOW);
//   digitalWrite(SARA_ENABLE, LOW);

//   while (true) {
//     if (count >= (SLEEP_TIMEOUT / 8)) {
//       sodaq_wdt_flag = false;
//       sodaq_wdt_reset();
//       break;
//     }
//     if (sodaq_wdt_flag) {
//       sodaq_wdt_flag = false;
//       sodaq_wdt_reset();
//       // #if DEBUG_STREAM_ON
//       //   DEBUG_STREAM.println("WDT interrupt has been triggered");
//       // #endif
//     }
//     count++;
// #if DEBUG_STREAM_ON
//     // DEBUG_STREAM.print("sleep mode timeout: ");
//     // DEBUG_STREAM.println(count*8);
// #endif
//     systemSleep();
//   }

//   sodaq_wdt_disable();
// //   network_register();
// #endif
// }

// void sleep_SFF_long(int sleepTime) {
//   // radio_off();
//   int count = 0;
//   sodaq_wdt_enable(WDT_PERIOD_8X);
//   //  digitalWrite(SARA_TX_ENABLE, LOW);
//   //  digitalWrite(SARA_ENABLE, LOW);
//   // #if DEBUG_STREAM_ON
//   //   DEBUG_STREAM.println("Step into long SFF sleep");
//   // #endif
//   while (true) {
//     // DEBUG_STREAM.println(count);
//     if (count >= (sleepTime)) {
//       sodaq_wdt_flag = false;
//       sodaq_wdt_reset();
//       break;
//     }
//     if (sodaq_wdt_flag) {
//       sodaq_wdt_flag = false;
//       sodaq_wdt_reset();
//       // #if DEBUG_STREAM_ON
//       //   DEBUG_STREAM.println("WDT interrupt has been triggered");
//       // #endif
//     }
//     count++;
//     systemSleep();
//   }
// }

// void sleep_SFF() {
//   radio_off();
//   int count = 0;
//   sodaq_wdt_enable(WDT_PERIOD_8X); // ~8s
//   // digitalWrite(SARA_TX_ENABLE, LOW);
//   digitalWrite(SARA_ENABLE, LOW);
// #if DEBUG_STREAM_ON
//   DEBUG_STREAM.println("Step into SFF sleep");
// #endif
//   while (true) {
//     if (count >= (SLEEP_TIMEOUT / 8)) {
//       sodaq_wdt_flag = false;
//       sodaq_wdt_reset();
//       break;
//     }
//     if (sodaq_wdt_flag) {
//       sodaq_wdt_flag = false;
//       sodaq_wdt_reset();
//       // #if DEBUG_STREAM_ON
//       //   DEBUG_STREAM.println("WDT interrupt has been triggered");
//       // #endif
//     }
//     count++;
//     systemSleep();
//   }

//   sodaq_wdt_disable();
//   // network_register();
// }

// void burning_ID(char* id_str) {
//   char lists[63] =
//   "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"; char
//   letter[1]; char id[ID_SIZE]; randomSeed(analogRead(0)); for(int i = 0; i <
//   ID_SIZE; i++) {
//     letter[0] = lists[random(63)];
// //    strncat(id_str, letter, 1);
//     strncat(id, letter, 1);
//   }
// //  DEBUG_STREAM.print("id: ");
// //  DEBUG_STREAM.println(id);
//   str_to_hexstr(id, id_str);
// }

// bool get_IMEI_IMSI(char *id_str) {
//   char imei_id[10];
//   char imsi_id[10];
//   char id[ID_SIZE];
//   send_cmd("at+cgsn"); // IMEI
//   if (!read_to_end())
//     return false;
//   if (!buf_is_middle_fixed_size(imei_id, IMEI_SIZE - 11, 11 + 11))
//     return false;
//   send_cmd("at+cimi"); // IMSI
//   if (!read_to_end())
//     return false;
//   if (!buf_is_middle_fixed_size(imsi_id, IMSI_SIZE - 11, 11 + 11))
//     return false;
//   sprintf(id, "%s%s", imei_id, imsi_id);
//   str_to_hexstr(id, id_str);
//   return true;
// }

// bool get_UTCtime(char *time_str) {
//   send_cmd("at+cops?");
//   if (!read_to_end())
//     return false;
//   for (int i = 0; i < 5; i++) {
//     send_cmd("at+cclk?");
//     if (!read_to_end())
//       return false;
//     if (!buf_is_middle_fixed_size(time_str, 26 - 7, 11 + 7))
//       return false;
//     if (time_str[1] != '8') {
//       break;
//     } else {
//       DEBUG_STREAM.println("time_str got a wrong time from the base
//       station"); send_cmd("at+ctzu=1"); if (!read_to_end(10))
//         continue; // 3s
//                   //        send_cmd("at+creg=1");
//                   //        if(!read_to_end(10)) continue;  // 3s
//       if (time_str[1] == '8')
//         continue; // Ok...we try again.
//     }
//     delay(500);
//   }
//   if (time_str[1] == '8')
//     return false;

//   //  if(!buf_is_middle_fixed_size(time_str, 26-7, 11+7)) return false;
//   time_converted(time_str);
//   strncat(time_str, ",", 1);
//   return true;
// }

// void time_converted(char *time_str) {
//   char temp[strlen(time_str)];
//   char temp2[strlen(time_str)];
//   strncpy(temp, time_str + 1, strlen(time_str) - 2);
//   strncpy(temp2, "20", 2);
//   strncat(temp2, temp, 2);
//   strncat(temp2, temp + 3, 2);
//   strncat(temp2, temp + 3 * 2, 2);
//   strncat(temp2, ",", 1);
//   strncat(temp2, temp + 3 * 3, 2);
//   strncat(temp2, temp + 3 * 4, 2);
//   strncat(temp2, temp + 3 * 5, 2);
//   strcpy(time_str, temp2);
// }
