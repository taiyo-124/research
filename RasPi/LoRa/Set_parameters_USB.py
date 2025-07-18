import serial
import time 

# データシート: https://dragon-torch.tech/wp-content/uploads/2022/08/data_sheet.pdf

# 0xc0: レジスタ値の書き込みコマンド
# 0x00: 開始アドレス
# 0x08: 8アドレスに書き込み(後ろに8コマンド続く)
# 0x00 0x00: Module Address (default) ⇛ FFFF(ブロードキャストアドレス)に設定
# 0x61: BW, SFを設定(0110 0001)
# 0xC1; パケット長と送信出力電力(110, reserved000, 01)
# 0x00: 周波数チャネルを0に設定
# 0xc5: 1100 0101→RSSIバイト有効化, 固定送信モード, reserved(3bit), WORサイクルを3000msに設定
# 0x00 0x00: 暗号キーを0に設定

# params: パラメータの具体値

params = {
    "address_high": 0x00,
    "address_low": 0x00,
    "BPS": 0x70,
    "options_main": 0x23,
    "channel": 0x00,
    "options_sub": 0xC5,
    "crypt_high": 0x00,
    "crypt_low": 0x00
}

def make_config_command(
    address_high,
    address_low,
    BPS,
    options_main,
    channel,
    options_sub,
    crypt_high,
    crypt_low
):
    return bytearray([
        0xC0,
        0x00,
        0x08,
        address_high,
        address_low,
        BPS,
        options_main,
        channel,
        options_sub,
        crypt_high,
        crypt_low
    ])

def send_command(command):
    # ポート設定
    ser = serial.Serial(
        port='/dev/ttyUSB0',
        baudrate=9600,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        timeout=1
    )
    ser.write(command)
    time.sleep(0.1)
    response = ser.read(11)
    return response


def config(params=None):
    if params is None:
        params = {}
    command = make_config_command(**params)
    return send_command(command)

def check():
    request = bytearray([0xC1, 0x00, 0x08])
    return send_command(request)



print(config(params))
print(check())

