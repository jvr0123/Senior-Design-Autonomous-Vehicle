import socket
import sys
import cv2
import pickle
import numpy as np
import struct
import os
import pigpio
import time

HOST = '192.168.1.219'
PORT = 8083


pi = pigpio.pi(host = "192.168.1.204")

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')

s.bind((HOST, PORT))
print('Socket bind complete')
s.listen(10)
print('Socket now listening')

conn, addr = s.accept()

data = b''
payload_size = struct.calcsize("L")
#TODO THIS IS CURRENTLY HARDCODED TO SPECIFIC DEVICES!!!
path = 'C:/Users\danny\PycharmProjects\eecs159b\images'
os.chdir(path)
count = 0

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

while True:
    while len(data) < payload_size:
        data += conn.recv(4096)
    packed_msg_size = data[:payload_size]

    data = data[payload_size:]
    msg_size = struct.unpack("L", packed_msg_size)[0]

    while len(data) < msg_size:
        data += conn.recv(4096)
    frame_data = data[:msg_size]
    data = data[msg_size:]

    frame = cv2.flip(pickle.loads(frame_data), -1)
    cv2.imwrite("frame%d.jpeg" % count, frame) # save as jpeg

    cv2.imshow('frame', frame)
    keyPress = cv2.waitKey(10)
    if keyPress & 0xFF == ord('w'): forward(.03)

    elif keyPress & 0xFF == ord('s'): reverse(.03)

    elif keyPress & 0xFF == ord('q'):
        break
    count += 1
