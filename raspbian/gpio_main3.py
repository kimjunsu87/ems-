## PUSH BUTTON RGB LED Control
import RPi.GPIO as GPIO
import time 

BUTTON = 3
RED = 11
GREEN = 12
BLUE = 13

GPIO.setmode(GPIO.BOARD)
GPIO.setup(BUTTON, GPIO.IN)
GPIO.setup(RED, GPIO.OUT) # 11번 핀 출력셋팅
GPIO.setup(GREEN,GPIO.OUT) # 12번 핀 출력셋팅
GPIO.setup(BLUE, GPIO.OUT) # 13번 핀 출력셋팅

is_click = False

def button_push(val):
    global is_click
    if is_click == True:
        GPIO.output(RED, GPIO.HIGH)
        GPIO.output(GREEN, GPIO.HIGH)
        GPIO.output(BLUE, GPIO.HIGH)
    else:
        GPIO.output(RED, GPIO.LOW)
        GPIO.output(GREEN, GPIO.LOW)
        GPIO.output(BLUE, GPIO.LOW)

    is_click = not is_click


while True:
    GPIO.wait_for_edge(BUTTON, GPIO.RISING, bouncetime=100)
    time.sleep(0.1)

    button_push(GPIO.input(BUTTON))