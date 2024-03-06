import serial.tools.list_ports
import time

COM4 = "COM4"
COM5 = "COM5"
COM7 = "COM7"
COM_WSL = "/dev/pts/2"
OK_ANS = "OK"


class UART:
    ser = None
    mess = ""
    port_error = False
    check_connection = True

    def __init__(self) -> None:
        self.ser = serial.Serial(port=self.getPort(), baudrate=115200)

        # self.ser = serial.Serial(port=COM5, baudrate=9600)
        # print(self.ser)
        if self.ser.port == None:
            self.port_error = True

    def getPort(self):
        ports = serial.tools.list_ports.comports()
        N = len(ports)
        # print(N)
        commPort = None
        for i in range(0, N):
            port = ports[i]
            strPort = str(port)
            # print(strPort)
            if "serial port emulator CNCA1" in strPort:
                splitPort = strPort.split(" ")
                # print(splitPort)
                commPort = (splitPort[0])
        return commPort

    def ProcessData(self, data, my_server):
        data = data.replace("!", "")
        data = data.replace("#", "")
        feed, value = data.split(":")
        print([feed, value])
        text = ''
        address = ''
        answer = '!'+feed+':'+OK_ANS+'#'
        if answer != '!send:OK#':
            self.ser.write(answer.encode())
        if feed == "temp":
            text = f'Publishing {value} to {my_server.AIO_FEED_NAMES[4]}.'
            address = f'{my_server.AIO_USERNAME}/feeds/{my_server.AIO_FEED_NAMES[4]}'
        elif feed == "humid":
            text = f'Publishing {value} to {my_server.AIO_FEED_NAMES[3]}.'
            address = f'{my_server.AIO_USERNAME}/feeds/{my_server.AIO_FEED_NAMES[3]}'
        elif feed == "bright":
            text = f'Publishing {value} to {my_server.AIO_FEED_NAMES[2]}.'
            address = f'{my_server.AIO_USERNAME}/feeds/{my_server.AIO_FEED_NAMES[2]}'
        elif feed == "send" and value == "OK":
            self.check_connection = True
        if text != '':
            print(text)
            my_server.client.publish(address, value)

        #     # client.publish("bbc-temp", splitData[2])
        #     print(splitData[2])

    def ReadSerial(self, my_server):
        bytesToRead = self.ser.inWaiting()
        if (bytesToRead > 0):
            self.mess = self.mess + self.ser.read(bytesToRead).decode("UTF-8")
            while ("#" in self.mess) and ("!" in self.mess):
                start = self.mess.find("!")
                end = self.mess.find("#")
                self.ProcessData(self.mess[start:end + 1], my_server)
                if (end == len(self.mess)):
                    self.mess = ""
                else:
                    self.mess = self.mess[end+1:]

    def send_data(self, mess):
        self.check_connection = False
        self.ser.write(mess.encode())
        return


# for testing
# temp = UART()
# while True:
#     bytesToRead = temp.ser.inWaiting()
#     if (bytesToRead > 0):
#         temp.mess = temp.mess + temp.ser.read(bytesToRead).decode("UTF-8")
#         print(temp.mess)
#     time.sleep(1)
