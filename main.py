import random
import time
from my_adafruit_connection import AdafruitConnection
from my_ai import DetectPersonModel

my_server = AdafruitConnection()
my_model = DetectPersonModel()
timer = 10
timer_ai = 5
pre_res = None
while True:
    timer -= 1
    timer_ai -= 1
    if timer <= 0:
        timer = 10
        # send a random data every 10s
        value = random.randint(0, 1)
        print(f'Publishing {value} to {my_server.AIO_FEED_NAMES[0]}.')
        my_server.client.publish(
            f'{my_server.AIO_USERNAME}/feeds/{my_server.AIO_FEED_NAMES[0]}',
            value)
    if timer_ai < 0:
        timer_ai = 5
        # send the result of my AI model
        res, score = my_model.detect_person()
        # send the data only if the score high and not same result
        if score > 0.8 and pre_res != res:
            print(f'Publishing {res} to {my_server.AIO_FEED_NAMES[5]}.')
            my_server.client.publish(
                f'{my_server.AIO_USERNAME}/feeds/{my_server.AIO_FEED_NAMES[5]}',
                res)
            pre_res = res
    time.sleep(1)
    # ESC is pressed
    if my_model.exit() == 1:
        break
