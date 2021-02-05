import sys

import cv2
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *

from Client.VideoThread import VideoThread


class Ui_MainWindow(object):
    # UI
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        # create the label that holds camera feed
        self.feed = QtWidgets.QLabel(self.centralwidget)
        self.feed.setGeometry(QtCore.QRect(306, 130, 481, 411))
        self.feed.setFrameShape(QtWidgets.QFrame.Box)
        self.feed.setText("")
        self.feed.setWordWrap(False)
        self.feed.setObjectName("feed")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(30, 130, 261, 411))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.toggleDataCollection = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toggleDataCollection.sizePolicy().hasHeightForWidth())
        self.toggleDataCollection.setSizePolicy(sizePolicy)
        self.toggleDataCollection.setObjectName("toggleDataCollection")
        self.verticalLayout.addWidget(self.toggleDataCollection)
        self.toggleDataCollection.setCheckable(True)
        self.toggleCamera = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toggleCamera.sizePolicy().hasHeightForWidth())

        self.toggleCamera.setSizePolicy(sizePolicy)
        self.toggleCamera.setObjectName("toggleCamera")
        self.toggleCamera.setCheckable(True)
        self.verticalLayout.addWidget(self.toggleCamera)

        self.toggleCollisionAvoidance = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toggleCollisionAvoidance.sizePolicy().hasHeightForWidth())
        self.toggleCollisionAvoidance.setSizePolicy(sizePolicy)
        self.toggleCollisionAvoidance.setObjectName("toggleCollisionAvoidance")
        self.verticalLayout.addWidget(self.toggleCollisionAvoidance)
        self.route = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.route.sizePolicy().hasHeightForWidth())
        self.route.setSizePolicy(sizePolicy)
        self.route.setObjectName("route")
        self.verticalLayout.addWidget(self.route)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.menuSettings = QtWidgets.QMenu(self.menubar)
        self.menuSettings.setObjectName("menuSettings")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOptions = QtWidgets.QAction(MainWindow)
        self.actionOptions.setObjectName("actionOptions")
        self.actionConnect = QtWidgets.QAction(MainWindow)
        self.actionConnect.setObjectName("actionConnect")
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.menuSettings.addAction(self.actionOptions)
        self.menuSettings.addAction(self.actionConnect)
        self.menuSettings.addSeparator()
        self.menuSettings.addAction(self.actionQuit)
        self.menubar.addAction(self.menuSettings.menuAction())
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # connect buttons

        self.toggleCamera.clicked.connect(self.clickedToggleCamera)

        self.toggleDataCollection.clicked.connect(self.clickedToggleDataCollection)

    def update_image(self, cv_img):
        # Updates the image_label with a new opencv image
        qt_img = self.convert_cv_qt(cv_img)
        self.feed.setPixmap(qt_img)

    def convert_cv_qt(self, cv_img):
        # Convert from an opencv image to QPixmap
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(481, 411, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

        # self.actionQuit.triggered.connect(sys.exit())

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Controller"))
        self.toggleDataCollection.setText(_translate("MainWindow", "Toggle Data Collection"))
        self.toggleCamera.setText(_translate("MainWindow", "Toggle Camera"))
        self.toggleCollisionAvoidance.setText(_translate("MainWindow", "Toggle Collision Avoidance"))
        self.route.setText(_translate("MainWindow", "Route"))
        self.menuSettings.setTitle(_translate("MainWindow", "Settings"))
        self.actionOptions.setText(_translate("MainWindow", "Options"))
        self.actionConnect.setText(_translate("MainWindow", "Connect"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))

    def clickedToggleCamera(self):
        if self.toggleCamera.isChecked():
            self.thread = VideoThread()
            self.thread.change_pixmap_signal.connect(self.update_image)
            self.thread.start()
        else:
            self.thread.change_pixmap_signal.disconnect()
            self.feed.clear()
    def clickedToggleDataCollection(self):
        if self.toggleCamera.isChecked():
            if self.toggleDataCollection.isChecked(self):
                print("test")

    def closeEvent(self, event):
        self.thread.stop()
        event.accept()

    def keyPressEvent(self, event):
       #only allowed to move if camera is on
        if event.key() == QtCore.Qt.Key_Up:
            print("forward")
        elif event.key() == QtCore.Qt.Key_Down:
            print("forward")
        elif event.key() == QtCore.Qt.Key_Left:
            print("forward")
        elif event.key() == QtCore.Qt.Key_Right:
            print("forward")
        else:
            QtWidgets.QLabel.keyPressEvent(self, event)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())
