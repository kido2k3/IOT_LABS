import serial.tools.list_ports
COM_WSL = "/dev/pts/3"
ser = None
mess = ""
port_error = False
ser = serial.Serial(port=COM_WSL, baudrate=9600)
print(ser)
if ser.port == None:
    port_error = True

ser.write("hello world".encode())