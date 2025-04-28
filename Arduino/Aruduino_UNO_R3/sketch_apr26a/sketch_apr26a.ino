
// MHZ19CのUARTでCO2濃度を取得
uint16_t uartco2;
bool reset = false;

// MHZ19CのCO2取得コマンド
byte ReadCO2[9] = {0xFF, 0x01, 0x86, 0x00, 0x00, 0x00, 0x00, 0x00, 0x79};
byte retval[9];


void setup() {
  pinMode(40u, INPUT);
  pinMode(39u, INPUT);
  DEBUG_STREAM.begin(9600);
  MODEM_STREAM.begin(9600);
  DEBUG_STREAM.print("Start UARTCommunication");
  delay(2000);
}

void loop() {
  //UARTでデータ取得

  // コマンド書き込み(書き込み後少し待つ)
  MODEM_STREAM.write(ReadCO2, sizeof(ReadCO2));
  delay(10);

  // response読み込み(retvalに)
  MODEM_STREAM.readBytes((char *)retval, sizeof(retval));
  uartco2 = retval[2]*256 + retval[3];
  DEBUG_STREAM.print(uartco2);
  DEBUG_STREAM.println("ppm");
  delay(1600);
}
