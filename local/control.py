import cv2
import time
import gpiozero as gpio
import pigpio

pi = pigpio.pi(host='192.168.1.204')


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


cap = cv2.VideoCapture(0)

while (True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    #flips camera as required by our system
    frame = cv2.flip(frame, 0)

    # Display the resulting frame
    cv2.imshow('frame',frame)

    keyPress = cv2.waitKey(20)
    if keyPress & 0xFF == ord('w'):
        forward(.03)
    elif keyPress & 0xFF == ord('s'):
        reverse(.03)
    elif keyPress & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()