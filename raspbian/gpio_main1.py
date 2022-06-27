import RPi.GPIO as GPIO
import time

RED = 11
GREEN = 12
BLUE = 13

GPIO.setmode(GPIO.BOARD)  #GPIO.BCM 은 GPIO 번호 기준, BOARD 는 기판의 번호 기준
GPIO.setup(RED, GPIO.OUT) # 11번 핀 출력셋팅
GPIO.setup(GREEN,GPIO.OUT) # 12번 핀 출력셋팅
GPIO.setup(BLUE, GPIO.OUT) # 13번 핀 출력셋팅

try:
    while True:
        GPIO.output(RED, GPIO.HIGH)
        GPIO.output(GREEN, GPIO.LOW)
        GPIO.output(BLUE, GPIO.LOW)
        time.sleep(0.5)

        GPIO.output(RED, GPIO.LOW)
        GPIO.output(GREEN, GPIO.HIGH)
        GPIO.output(BLUE, GPIO.LOW)
        time.sleep(0.5)

        GPIO.output(RED, GPIO.LOW)
        GPIO.output(GREEN, GPIO.LOW)
        GPIO.output(BLUE, GPIO.HIGH)
        time.sleep(0.5)

        GPIO.output(RED, GPIO.HIGH)
        GPIO.output(GREEN, GPIO.HIGH)
        GPIO.output(BLUE, GPIO.HIGH)
        time.sleep(0.5)

except KeyboardInterrupt: 
    GPIO.output(RED, GPIO.LOW)
    GPIO.output(GREEN, GPIO.LOW)
    GPIO.output(BLUE, GPIO.LOW)
    GPIO.cleanup()
 # HIGH 켜짐, LOW 꺼짐