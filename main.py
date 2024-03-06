import random
import time
from my_adafruit_connection import AdafruitConnection
from my_ai import DetectPersonModel
from my_serial import UART

my_serial = UART()
my_server = AdafruitConnection()
my_model = DetectPersonModel()

# timer = 10
timer_ai = 5
timer_connection = 2
pre_res = None
fsm_communication = "idle"
send_time = 0
while True:
    # print(fsm_communication)
    if fsm_communication == "idle":
        if my_server.received == True:
            fsm_communication = "send"
    elif fsm_communication == "send":
        send_time += 1
        mess = my_server.data
        my_serial.send_data(mess)
        if my_serial.check_connection == True:
            my_server.received = False
            fsm_communication = "idle"
            send_time = 0
        else:
            timer_connection = 2
            fsm_communication = "wait"
    elif fsm_communication == "wait":
        timer_connection -= 1
        if my_serial.check_connection == True:
            send_time = 0
            my_server.received = False
            fsm_communication = "idle"
        elif timer_connection <= 0:
            fsm_communication = "send"
        elif send_time >= 3:
            print("THERE IS SOME WRONG IN SERIAL")
            my_server.received = False
            fsm_communication = "idle"
            send_time = 0
    # timer -= 1
    # if timer <= 0:
    #     timer = 10
    #     # send a random data every 10s
    #     value = random.randint(0, 1)
    #     print(f'Publishing {value} to {my_server.AIO_FEED_NAMES[0]}.')
    #     my_server.client.publish(
    #         f'{my_server.AIO_USERNAME}/feeds/{my_server.AIO_FEED_NAMES[0]}',
    #         value)

    # read data from uart and send to my server
    if my_serial.port_error == False:
        my_serial.ReadSerial(my_server)
    # send the result of my AI model every 5s
    timer_ai -= 1
    if timer_ai < 0:
        timer_ai = 5
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
