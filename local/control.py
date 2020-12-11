import RPi.GPIO as gpio
import time
import cv2

#for our servo, a duty of 6 for the input wave sends the servo to the middle. the relationship between the duty and
#angle is duty = 2+angle/15
duty = 6


def init(flag):
    gpio.setmode(gpio.BCM)
    # motors
    gpio.setup(17, gpio.OUT)
    gpio.setup(22, gpio.OUT)
    gpio.setup(23, gpio.OUT)
    gpio.setup(24, gpio.OUT)

    # servo
    #the bool flag decides whether we return none or an object for the servos
    if flag:
        gpio.setup(4, gpio.OUT)
        servo1 = gpio.PWM(4, 50)
        servo1.start(0)
        return servo1
    else:
        return


def forward(sec):
    init(False)
    gpio.output(17, True)
    gpio.output(22, False)
    gpio.output(23, True)
    gpio.output(24, False)
    time.sleep(sec)
    gpio.cleanup()


def reverse(sec):
    init(False)
    gpio.output(17, False)
    gpio.output(22, True)
    gpio.output(23, False)
    gpio.output(24, True)
    time.sleep(sec)
    gpio.cleanup()


def turnRight(sec):
    servo1 = init(True)
    global duty
    if duty >= 2.6:
        duty = duty - 2.6
    servo1.ChangeDutyCycle(duty)
    time.sleep(sec)
    servo1.stop()
    gpio.cleanup()


def turnLeft(sec):
    servo1 = init(True)
    global duty
    if duty <= 9.4:
        duty = duty + 2.6
    servo1.ChangeDutyCycle(duty)
    time.sleep(sec)
    servo1.stop()
    gpio.cleanup()


def center(sec):
    servo1 = init(True)
    global duty
    duty = 6
    servo1.ChangeDutyCycle(duty)
    time.sleep(sec)
    servo1.stop()
    gpio.cleanup()


# start video capture

cap = cv2.VideoCapture(0)

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

while (True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    # flips camera as required by our system
    frame = cv2.flip(frame, 0)

    out.write(frame)
    # Display the resulting frame
    cv2.imshow('frame', frame)

    keyPress = cv2.waitKey(20)
    #these values are picked experimentally
    if keyPress & 0xFF == ord('w'):
        forward(.03)
    elif keyPress & 0xFF == ord('s'):
        reverse(.03)
    elif keyPress & 0xFF == ord('a'):
        turnLeft(.1)
    elif keyPress & 0xFF == ord('d'):
        turnRight(.1)
    elif keyPress & 0xFF == ord('t'):
        center(.1)
    elif keyPress & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
out.release()
cv2.destroyAllWindows()