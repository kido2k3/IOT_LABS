import random
import time
from my_adafruit_connection import AdafruitConnection


my_server = AdafruitConnection()
counter = 10

while True:
    counter = counter-1
    if counter <= 0:
        counter = 10
        value = random.randint(0, 1)
        print(f'Publishing {value} to {my_server.AIO_FEED_NAMES[0]}.')
        my_server.client.publish(
            f'{my_server.AIO_USERNAME}/feeds/{my_server.AIO_FEED_NAMES[0]}', value)
    time.sleep(1)
