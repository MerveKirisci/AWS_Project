import RPi.GPIO as GPIO
import time
import requests

GPIO.setmode(GPIO.BCM)

TRIG = 17
ECHO = 27

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)


def measure_distance():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    start_time = time.time()
    stop_time = time.time()

    while GPIO.input(ECHO) == 0:
        start_time = time.time()

    while GPIO.input(ECHO) == 1:
        stop_time = time.time()

    elapsed_time = stop_time - start_time
    distance = int((elapsed_time * 34300) / 2)


    return distance


try:
    while True:
        time.sleep(1)
        distance = measure_distance()
        print(f"Distance: {distance} cm")

        if distance > 30 :
            continue

        x = requests.get(
            'https://x8stc0ezqf.execute-api.eu-north-1.amazonaws.com/default/sus_insert_db?range=' + str(distance))



except KeyboardInterrupt:
    print("Measurement stopped by user")
    GPIO.cleanup()
