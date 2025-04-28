#include "INQR410.h"
#include <Adafruit_BME680.h>
#include <Sodaq_wdt.h>
#include <Wire.h>

#ifdef ARDUINO_ARCH_AVR
#include <avr/sleep.h>
#define DEBUG_STREAM Serial

#elif ARDUINO_ARCH_SAMD
#define DEBUG_STREAM SerialUSB

#endif

void initWdt() {
  DEBUG_STREAM.println("wdt init");
  sodaq_wdt_enable(WDT_PERIOD_8X);
  sodaq_wdt_flag = false;
  // ノイズなど存在するため初回リセット
  sodaq_wdt_reset();
}

void systemSleep(bool isDeepSleep) {
#ifdef ARDUINO_ARCH_AVR
  // Wait till the output has been transmitted
  DEBUG_STREAM.flush();

  ADCSRA &= ~_BV(ADEN); // ADC disabled

  /*
  * Possible sleep modes are (see sleep.h):
  #define SLEEP_MODE_IDLE         (0)
  #define SLEEP_MODE_ADC          _BV(SM0)
  #define SLEEP_MODE_PWR_DOWN     _BV(SM1)
  #define SLEEP_MODE_PWR_SAVE     (_BV(SM0) | _BV(SM1))
  #define SLEEP_MODE_STANDBY      (_BV(SM1) | _BV(SM2))
  #define SLEEP_MODE_EXT_STANDBY  (_BV(SM0) | _BV(SM1) | _BV(SM2))
  */
  set_sleep_mode(SLEEP_MODE_PWR_DOWN);

  /*
   * This code is from the documentation in avr/sleep.h
   */
  cli();
  // Only go to sleep if there was no watchdog interrupt.
  if (!sodaq_wdt_flag) {
    // Power on LED before sleep
    digitalWrite(SLEEP_LED, HIGH);

    sleep_enable();
    sei();
    sleep_cpu();
    sleep_disable();

    // Power off LED after sleep
    digitalWrite(SLEEP_LED, LOW);
    sodaq_wdt_safe_delay(LED_FLASH_MS);
  }
  sei();

  ADCSRA |= _BV(ADEN); // ADC enabled

#elif ARDUINO_ARCH_SAMD
  // Only go to sleep if there was no watchdog interrupt.
  if (!sodaq_wdt_flag) {
    // USBDevice.detach();

    if (isDeepSleep) {
      SCB->SCR |= SCB_SCR_SLEEPDEEP_Msk;
    }

    // SAMD sleep
    __WFI();
  }
#endif
}

void longSleep(unsigned long sleepTimeMilliSec, bool isDeepSleep) {
  /*
  sodaq_wdt_flag：上限時間となってカウント値がリセットされていない時にフラグが立つ
  sodaq_wdt_reset：カウント値をResetするはず
  */
  unsigned long counter = 0;
  // Max wait time
  const int longSleepTime = 8;
  // STANDBYではクロック止まるため割り算する
  // IDLEではクロック止まらないため割り算しない
  const int loopTimes = isDeepSleep ? sleepTimeMilliSec / (longSleepTime * 1000)
                                    : sleepTimeMilliSec;
  while (true) {
    // DEBUG_STREAM.print("millis ");
    // DEBUG_STREAM.print(millis());
    // DEBUG_STREAM.println(" in while loop");
    if (counter >= loopTimes) {
      sodaq_wdt_flag = false;
      sodaq_wdt_reset();
      return;
    } else if (sodaq_wdt_flag) {
      sodaq_wdt_flag = false;
      sodaq_wdt_reset();
    }
    counter++;
    systemSleep(isDeepSleep);
  }
  return;
}
