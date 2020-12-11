
import sys
import cv2


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import  QWidget, QLabel, QApplication
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import qimage2ndarray

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Control")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
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
        self.toggleRectangles = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toggleRectangles.sizePolicy().hasHeightForWidth())
        self.toggleRectangles.setSizePolicy(sizePolicy)
        self.toggleRectangles.setObjectName("toggleRectangles")
        self.verticalLayout.addWidget(self.toggleRectangles)
        self.toggleCamera = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toggleCamera.sizePolicy().hasHeightForWidth())
        self.toggleCamera.setSizePolicy(sizePolicy)
        self.toggleCamera.setObjectName("toggleCamera")
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

        #create timer object for async opencv call
        self.timer = QTimer()
        self.timer.timeout.connect(self.clickedToggleCamera)
        self.toggleCamera.clicked.connect(self.clickedToggleCamera)

        #self.actionQuit.triggered.connect(sys.exit())

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.toggleRectangles.setText(_translate("MainWindow", "Toggle Rectangles"))
        self.toggleCamera.setText(_translate("MainWindow", "Toggle Camera"))
        self.toggleCollisionAvoidance.setText(_translate("MainWindow", "Toggle Collision Avoidance"))
        self.route.setText(_translate("MainWindow", "Route"))
        self.menuSettings.setTitle(_translate("MainWindow", "Settings"))
        self.actionOptions.setText(_translate("MainWindow", "Options"))
        self.actionConnect.setText(_translate("MainWindow", "Connect"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))

    def clickedToggleCamera(self):
        ret, frame = cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = qimage2ndarray.array2qimage(frame)
        self.startTimer()
        self.feed.setPixmap(QPixmap.fromImage(image))

    def startTimer(self):
        self.timer.start(60)

    def endTimer(self):
        self.timer.stop()
        cv2.destroyAllWindows()

    #def wPressEvent(self, event):


if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 481)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 411)

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    #timer = QTimer()
    #timer.timeout.connect(ui.clickedToggleCamera)
    #timer.start(60)
    sys.exit(app.exec_())


