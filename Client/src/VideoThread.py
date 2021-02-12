
import cv2
import numpy as np
from PyQt5.QtCore import pyqtSignal, QThread
import math


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self._run_flag = True
    def run(self):
        # capture from web cam
        cap = cv2.VideoCapture(0)
        frameRate = cap.get(5)
        x = 1
        while self._run_flag:
            ret, cv_img = cap.read()
            frameId = cap.get(1)
            if ret:
                self.change_pixmap_signal.emit(cv_img)
                if (frameId % math.floor(frameRate) == 0):
                    filename = './images/image' + str(int(x)) + ".jpg"
                    x += 1
                    cv2.imwrite(filename, cv_img)
        # shut down capture system
        cap.release()

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()
cap = cv2.VideoCapture(0)
print(type(cap))