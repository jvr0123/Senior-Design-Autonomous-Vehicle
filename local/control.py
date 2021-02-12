import pickle
import time
import cv2
import pigpio
import struct
import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 8000
msg = ""
MESSAGE = pickle.dumps(msg)

clientsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientsock.connect((UDP_IP, UDP_PORT))


pi = pigpio.pi(host = "192.168.1.204")

sdata = b""
#header for incoming image
payload_size = struct.calcsize("L")
def init(flag):
    # motors
    pi.set_mode(17, pigpio.OUTPUT)
    pi.set_mode(22, pigpio.OUTPUT)
    pi.set_mode(23, pigpio.OUTPUT)
    pi.set_mode(24, pigpio.OUTPUT)

    # servo
    # the bool flag decides whether we return none or an object for the servos
    if flag:
        pi.set_mode(4, pigpio.OUTPUT)
        pi.set_PWM_frequency(4, 50)
def cleargpio():
    pi.write(17, 0)
    pi.write(22, 0)
    pi.write(23, 0)
    pi.write(24, 0)

def forward(sec):
    init(False)
    pi.write(17, 1)
    pi.write(22, 0)
    pi.write(23, 1)
    pi.write(24, 0)
    time.sleep(sec)
    cleargpio()


def reverse(sec):
    init(False)
    pi.write(17, 0)
    pi.write(22, 1)
    pi.write(23, 0)
    pi.write(24, 1)
    time.sleep(sec)
    cleargpio()


while (True):
    conn, address = clientsock.recvfrom(4096)
    while len(sdata < payload_size):
        sdata += conn
    packed_msg_size = sdata[:payload_size]
    sdata = sdata[payload_size:]
    msg_size = struct.unpack("L", packed_msg_size)[0]
    frame_data = sdata[:msg_size]

    while len(sdata) < msg_size:
        sdata += conn.recv(4096)
    frame_data = sdata[:msg_size]
    sdata = sdata[msg_size:]

    frame = pickle.loads(frame_data)
    print(frame.size)
    cv2.imshow('frame', frame)
    keyPress = cv2.waitKey(20)
    if keyPress & 0xFF == ord('w'):
        forward(.03)

    elif keyPress & 0xFF == ord('s'):
        reverse(.03)
    elif keyPress & 0xFF == ord('q'):
        break