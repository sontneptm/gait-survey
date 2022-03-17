import cv2
import numpy as np
from PyQt5.QtCore import QDate, QObject, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5 import uic
import PyQt5.QtCore
import sys
from threading import Thread
import time
from glob import glob

form_class = uic.loadUiType("survey_gui.ui")[0]

class SurveyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.load_video_list()
        self.setup_buttons()
        
        self.vid_thread = Thread(target=self.load_video, args=())
        self.vid_thread.start()

    def load_video_list(self):
        self.vid_list = glob('GAIT_EMOTION/vid/*')
        self.vid_cursor = 0
        self.label_9.setText(str(self.vid_cursor+1) + '/' + str(len(self.vid_list)))

    def load_video(self):
        cap = cv2.VideoCapture(self.vid_list[self.vid_cursor])

        playing = self.vid_cursor

        while(True):
            if playing != self.vid_cursor:
                cap = cv2.VideoCapture(self.vid_list[self.vid_cursor])
                playing = self.vid_cursor

            if cap.isOpened():

                ret, self.frame = cap.read()
                vid_frame_rate = 60

                self.show_image(self.frame)
                time.sleep(1.0/vid_frame_rate)

    def show_image(self, img:np.ndarray):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h,w,c = img.shape

        qImg = QtGui.QImage(img.data, w, h, w*c, QtGui.QImage.Format_RGB888)
        pixmap  = QtGui.QPixmap.fromImage(qImg)
        self.vid_label.setPixmap(pixmap)

    def setup_buttons(self):
        self.next_button.clicked.connect(self.next_video)
        self.prev_button.clicked.connect(self.prev_video)

    @pyqtSlot()
    def next_video(self):
        if self.vid_cursor < len(self.vid_list) -1:
            self.vid_cursor += 1

    @pyqtSlot()
    def prev_video(self):
        if self.vid_cursor > -1:
            self.vid_cursor -= 1

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mWindow = SurveyWindow()
    mWindow.show()
    app.exec_()