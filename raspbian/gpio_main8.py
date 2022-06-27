## PUSH BUTTON Servo motor test
import RPi.GPIO as GPIO
import time 

SERVO = 12
BUTTON = 3

GPIO.setmode(GPIO.BOARD)
GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(SERVO, GPIO.OUT)

pwm = GPIO.PWM(SERVO, 50)  # 50Hz servo motor 동작 주파수
pwm.start(3.0) # 0.6ms
count = 0

def button_push(channel):
    global count
    if count % 3 == 1: # 90도
        pwm.ChangeDutyCycle(7.5)
    elif count % 3 == 2: # 180도
        pwm.ChangeDutyCycle(12.5)
    else:
        pwm.ChangeDutyCycle(3.0)  # 0도
    

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
    pwm.chaneDutyCycle(0.0)
    pwm.stop()
    GPIO.cleanup()