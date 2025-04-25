import RPi.GPIO as GPIO

# モードを0に設定する(M0=0, M1=0)

# GPIO番号で指定
GPIO.setmode(GPIO.BCM)
M0 = 5
M1 = 6

# RasPiから出力
GPIO.setup(M0, GPIO.OUT)
GPIO.setup(M1, GPIO.OUT)

# 1に設定
GPIO.output(M0, GPIO.LOW) 
GPIO.output(M1, GPIO.LOW)


# GPIOを解放
GPIO.cleanup(M0)
GPIO.cleanup(M1)