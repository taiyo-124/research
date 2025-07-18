#include <Arduino.h>

#include "lora_lib.h"


#define M0 D2
#define M1 D3


uint8_t request[256];
uint8_t response[256];



// コマンド詳細
const uint8_t WhatToDo = 0xC0;
const uint8_t StartAddr = 0x00;
const uint8_t NumAddr = 0x08; //後ろに8コマンド続く
const uint8_t ModuleAddHi = 0x00; // モジュールアドレス上位
const uint8_t ModuleAddLo = 0x00; // モジュールアドレス下位
const uint8_t BwSf = 0x70; // 帯域と拡散率それぞれ4bitで定める(1758bps, SF=9, BW=125kHz)
const uint8_t PacketDbm = 0x23; //パケット長と送信電力最小
const uint8_t ChFreq = 0x00; //周波数チャネル 0
const uint8_t OtherSetting = 0xC5; // RSSI有効化, 固定送信モード, reserved, WOR=3000msに設定
const uint8_t SecretCodeHi = 0x00;
const uint8_t SecretCodeLo = 0x00; // 暗号



void mode0(){
  digitalWrite(M0, LOW);
  digitalWrite(M1, LOW);
  delay(10);
  
  return ;
}

void mode3(){
  digitalWrite(M0, HIGH);
  digitalWrite(M1, HIGH);
  delay(10);
  
  return ;
}

void Set_parameters(){
  
  request[0] = WhatToDo;
  request[1] = StartAddr;
  request[2] = NumAddr;
  request[3] = ModuleAddHi;
  request[4] = ModuleAddLo;
  request[5] = BwSf;
  request[6] = PacketDbm;
  request[7] = ChFreq;
  request[8] = OtherSetting;
  request[9] = SecretCodeHi;
  request[10] = SecretCodeLo;

  Serial1.write(request, 11);

  delay(1000);
  
  Serial1.readBytes(response, 11);

  return;
}

void float2bytes(float val, byte* bytes_array) {
  union {
    float f;
    byte b[4];
  } data;
  data.f = val;
  for (int i = 0; i < 4; i++) {
    bytes_array[i] = data.b[i];
  }
}
