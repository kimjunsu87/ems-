import Adafruit_DHT as dht
import time

sensor = dht.DHT11
PIN = 4  # Adafruit 는 GPIO.BCM mode 

try:
    while True:
        (humid, temp) = dht.read_retry(sensor, PIN)
        if humid is not None and temp is not None:
            print(f'TEMP > {temp:.1f} C / Humidity > {humid:.1f}')
        else:
            print('Sensor error!')
        time.sleep(1.0) 

except KeyboardInterrupt:
    print('End of program')