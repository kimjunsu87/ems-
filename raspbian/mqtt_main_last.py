# MQTT Pub/Sub App
from threading import Thread, Timer
import threading
import time
import paho.mqtt.client as mqtt
import json
import datetime as dt
import adafruit_dht as dht  # DHT센서용
import board

import RPi.GPIO as GPIO

RED = 17
BLUE = 27
SENSOR = dht.DHT22(board.D4)

GPIO.setmode(GPIO.BCM)
GPIO.setup(RED, GPIO.OUT)
GPIO.setup(BLUE, GPIO.OUT)

# DHT 센서값 publish
class publisher(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.host = '192.168.0.26' 
        self.port = 1883
        print('publisher 스레드 시작')
        self.client = mqtt.Client(client_id='EMS02')


    def run(self):
        self.client.connect(self.host, self.port)
        self.publish_data_auto()
       
    def publish_data_auto(self):
        try:

            curr = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            t = SENSOR.temperature
            h = SENSOR.humidity
            origin_data = {'DEV_ID' : 'EMS02', 'CURR_DT' : curr, 'TEMP' : t, 'HUMID' : h }
            pub_data = json.dumps(origin_data)
            self.client.publish(topic='ems/rasp/data/', payload=pub_data)
            print(f'{curr} -> MQTT Published')
        except RuntimeError as e:
            print(f'ERROR > {e.args[0]}')

        Timer(2.0, self.publish_data_auto).start()
        

class subscriber(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.host = '192.168.0.26'  # 추후 변경
        self.port = 1883
        print('subscriber 스레드 시작')
        self.client = mqtt.Client(client_id='EMS92')

    def onConnect(self, mqttc, obj, flags, rc):
        print(f'sub:connected with rc > {rc}')

    def onMessage(self, mqttc, obj, msg):
        rcv_msg = str(msg.payload.decode('utf-8'))
        print(f'{msg.topic} / {rcv_msg}')
        data = json.loads(rcv_msg)
        type = data['TYPE']
        stat = data['STAT']
        if type == 'AIRCON' and stat == 'ON':
            GPIO.output(RED, GPIO.HIGH)
        elif type == 'AIRCON' and stat == 'OFF':
            GPIO.output(RED, GPIO.LOW)
        elif type == 'DEHUMD' and stat == 'ON':
            GPIO.output(BLUE, GPIO.HIGH)
        elif type == 'DEHUMD' and stat == 'OFF':
            GPIO.output(BLUE, GPIO.LOW)

        time.sleep(1.0)



    def run(self):


        self.client.on_connect = self.onConnect
        self.client.on_message = self.onMessage
        self.client.connect(self.host, self.port)
        self.client.subscribe(topic='ems/rasp/control/')
        self.client.loop_forever()

if __name__ == '__main__':
    try:
        thPub = publisher()
        thSub = subscriber()
        thPub.start()
        thSub.start()
    except KeyboardInterrupt:
        GPIO.output(RED, GPIO.LOW)
        GPIO.output(BLUE, GPIO.LOW)
