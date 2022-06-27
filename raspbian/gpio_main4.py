## PUSH BUTTON RGB LED Control2
import RPi.GPIO as GPIO
import time 

BUTTON = 3
RED = 11
GREEN = 12
BLUE = 13

GPIO.setmode(GPIO.BOARD)
GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(RED, GPIO.OUT) # 11번 핀 출력셋팅
GPIO.setup(GREEN,GPIO.OUT) # 12번 핀 출력셋팅
GPIO.setup(BLUE, GPIO.OUT) # 13번 핀 출력셋팅

count = 0

def button_push(channel):
    global count
    if count % 5 == 1:
        GPIO.output(RED, GPIO.HIGH)
        GPIO.output(GREEN, GPIO.LOW)
        GPIO.output(BLUE, GPIO.LOW)
    elif count % 5 == 2:
        GPIO.output(RED, GPIO.LOW)
        GPIO.output(GREEN, GPIO.HIGH)
        GPIO.output(BLUE, GPIO.LOW)
    elif count % 5 == 3:
        GPIO.output(RED, GPIO.LOW)
        GPIO.output(GREEN, GPIO.LOW)
        GPIO.output(BLUE, GPIO.HIGH)
    elif count % 5 == 4:
        GPIO.output(RED, GPIO.HIGH)
        GPIO.output(GREEN, GPIO.HIGH)
        GPIO.output(BLUE, GPIO.HIGH)
    else: 
        GPIO.output(RED, GPIO.LOW)
        GPIO.output(GREEN, GPIO.LOW)
        GPIO.output(BLUE, GPIO.LOW)

    count += 1
        
    # global is_click
    # print('Button pushed!')
    # if is_click == False:
    #     GPIO.output(RED, GPIO.HIGH)
    #     GPIO.output(GREEN, GPIO.HIGH)
    #     GPIO.output(BLUE, GPIO.HIGH)
    # else:
    #     GPIO.output(RED, GPIO.LOW)
    #     GPIO.output(GREEN, GPIO.LOW)
    #     GPIO.output(BLUE, GPIO.LOW)

GPIO.add_event_detect(BUTTON, GPIO.RISING, callback=button_push,bouncetime=100)
# is_click = not is_click

try:
    while True: time.sleep(0.1)
except KeyboardInterrupt:
    GPIO.output(RED, GPIO.LOW)
    GPIO.output(GREEN, GPIO.LOW)
    GPIO.output(BLUE, GPIO.LOW)
    GPIO.cleanup()