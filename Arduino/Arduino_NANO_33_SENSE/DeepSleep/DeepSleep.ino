#include <Arduino.h>
#include <HS300x.h>
#include <Arduino_LPS22HB.h>

#include "lora_lib.h"

#define SEC 1000
#define MIN (60*SEC)
#define HOUR (60*MIN)

// WDTのタイムアウト時間を設定
#define WDT_TIMEOUT_SECONDS 60


// WDT CONFIG レジスタのビットフィールド値
#define WDT_CONFIG_SLEEP_Pos                 (0UL)   /**< Bit position for SLEEP field. */
#define WDT_CONFIG_SLEEP_RunInSleep          (1UL)   /**< Enable watchdog in CPU sleep mode. */
#define WDT_CONFIG_HALT_Pos                  (3UL)   /**< Bit position for HALT field. */
#define WDT_CONFIG_HALT_Pause                (1UL)   /**< Pause watchdog while CPU is halted by debugger. */

// POWER RESETREAS レジスタのビットフィールド値
#define POWER_RESETREAS_DOG_Pos              (1UL)   /**< Bit position for DOG field. */

// CLOCK TASKS_LFCLKSTART レジスタのビットフィールド値
#define CLOCK_TASKS_LFCLKSTART_Trigger_Pos   (0UL)   /**< Bit position for Trigger field. */
#define CLOCK_TASKS_LFCLKSTART_Trigger       (1UL)   /**< Trigger task. */

// CLOCK EVENTS_LFCLKSTARTED レジスタのビットフィールド値
#define CLOCK_EVENTS_LFCLKSTARTED_Generated_Pos (0UL)  /**< Bit position for Generated field. */
#define CLOCK_EVENTS_LFCLKSTARTED_Generated     (1UL)  /**< Event generated. */

// ピンを定義
#define M0 D2
#define M1 D3

// 必要変数の定義
uint8_t payload[32];

byte temp_bytes[4];
byte humid_bytes[4];
byte pressure_bytes[4];
byte vinput_bytes[4];

/* WFIモード(Sleepモード)に入るようにする. 
 * WDTで間隔を管理して, センシングとLoRaによる送信を行う
 */

void setup() {
  Serial1.begin(9600);
  pinMode(M0, OUTPUT);
  pinMode(M1, OUTPUT);
  HS300x.begin();
  BARO.begin();

  while(!Serial1);

  mode3();
  delay(50);
  Set_parameters();


  // 電圧読み取り
  int voltage = analogRead(A0);
  float vinput = 3300.0*voltage/512;

  // センシング
  float temp = HS300x.readTemperature(CELSIUS);
  float humid = HS300x.readHumidity();
  float pressure = BARO.readPressure();


  delay(50);

  // floatをbyteに変換(LoRaで送る都合上)
  float2bytes(temp, temp_bytes);
  float2bytes(humid, humid_bytes);
  float2bytes(pressure, pressure_bytes);
  float2bytes(vinput, vinput_bytes);

  payload[0] = 0x00;
  payload[1] = 0x00;
  payload[2] = 0x00;
  for (int i = 0; i<sizeof(float); i++) {
    payload[3+i] = temp_bytes[i];
    payload[7+i] = humid_bytes[i];
    payload[11+i] = pressure_bytes[i];
    payload[15+i] = vinput_bytes[i];
    }
  mode0();
  delay(10);
  Serial1.write(payload, sizeof(payload));
  delay(10);
  mode3();

  Serial1.end();
  HS300x.end();
  BARO.end();

  
  // --- リセット要因の確認 --- (WDTになっているはず)
  uint32_t resetReason = NRF_POWER->RESETREAS;

  // WDTの設定
  
  // 1. LFRC (低周波RC発振器) の開始 (WDTが動作するために必須)
  ((NRF_CLOCK_Type *)0x40000000UL)->TASKS_LFCLKSTART = CLOCK_TASKS_LFCLKSTART_Trigger; 
  // EVENTS_LFCLKSTARTED イベントが発生するまで待機
  while (((NRF_CLOCK_Type *)0x40000000UL)->EVENTS_LFCLKSTARTED == 0) {
    // イベントフラグが立つまで待機 (ポーリング)
  }
  ((NRF_CLOCK_Type *)0x40000000UL)->EVENTS_LFCLKSTARTED = 0; // ★重要: イベントフラグをクリア

  // 2.WDTの設定レジスタ(CONFIG)
  // WDT_CONFIG_SLEEP_RunInSleep: System ON の SLEEP モードでも WDT を動作させる
  // WDT_CONFIG_HALT_Pause: デバッグ時に WDT を一時停止させるかどうかの設定
  NRF_WDT->CONFIG = (WDT_CONFIG_SLEEP_RunInSleep << WDT_CONFIG_SLEEP_Pos) |
                    (WDT_CONFIG_HALT_Pause << WDT_CONFIG_HALT_Pos);

  // 3. WDT のカウンタリロード値 (CRV)
  // CRV は、WDT がリセットをトリガーするまでの時間を設定
  // 32768 は LFRC の周波数 (32.768 kHz)
  NRF_WDT->CRV = (uint32_t)(WDT_TIMEOUT_SECONDS * 32768) - 1;

  delay(10);

  // 4. WDT 開始
  NRF_WDT->TASKS_START = 1;
}

void loop(){
  __WFI();
}
