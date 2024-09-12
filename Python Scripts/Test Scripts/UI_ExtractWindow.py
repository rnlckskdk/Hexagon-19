import sys, os
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QDesktopWidget, QSizePolicy, QProgressBar, QVBoxLayout)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QThread, pyqtSignal, Qt
import sqlite3

import Backend_engine
import Database

class ExtractWindow(QWidget):
    update_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        # 변수들
        self.currentDir = ''
        self.currentDB = None

        mainLayout = QVBoxLayout()

        # 진행 바
        self.progressBar = QProgressBar(self)
        self.progressBar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        mainLayout.addWidget(self.progressBar)

        # 확인 버튼
        self.btn = self.createButton('추출')
        self.btn.clicked.connect(self.startExtract)
        mainLayout.addWidget(self.btn, alignment=Qt.AlignmentFlag.AlignHCenter)
        
        self.setLayout(mainLayout)
        self.setupUI()

    ###########################
    ##### 셋업/생성 메소드 #####
    ###########################

    # 윈도우 생성 시 화면 가운데 정렬
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # 윈도우 기본 설정
    def setupUI(self):
        title = '추출'
        self.setWindowTitle(title)
        width = 720
        height = 360
        self.resize(width, height)
        # 아이콘 설정 / 상대경로
        script_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(script_dir, 'Icon2.png')
        self.setWindowIcon(QIcon(icon_path))
        self.center()

    # 버튼 생성 메소드
    def createButton(self, text):
        btnStyle = '''
        QPushButton
        {
            background-color: white;
            border-style: outset;
            border-width: 2px;
            border-radius: 10px;
            border-color: gray;
            font: bold 23px;
            min-width: 10em;
            padding: 6px;
        }
        QPushButton:pressed
        {
            background-color: gray;
            border-style: outset;
            border-width: 2px;
            border-radius: 10px;
            border-color: gray;
            font: bold 23px;
            min-width: 10em;
            padding: 6px;
        }
        '''
        btn = QPushButton(text)
        btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        btn.setStyleSheet(btnStyle)
        return btn

    #################################
    ##### 버튼 시그널 위한 메소드 #####
    #################################

    # 추출 버튼 시그널(추출 시작)
    def startExtract(self):
        Backend_engine.explore_the_path(self.currentDir, self.currentDB)
        self.progressBar.setMinimum(0)  # 무한 로딩 시작
        self.progressBar.setMaximum(0)

        self.currentDB.deleteDuplicateData()

        self.btn.setText('확인')
        self.btn.clicked.disconnect(self.startExtract)
        self.btn.clicked.connect(self.close)

        self.update_signal.emit("updateResultBox")

    ###########################
    #####  로딩함수/시험용 #####
    ###########################

    def updateProgress(self, value):
        self.progressBar.setValue(value)

    def onExtractFinished(self):
        self.progressBar.setMaximum(100)  # 무한 로딩 종료
        self.progressBar.setValue(100)
        self.btn.setEnabled(True)
        self.btn.setText('확인')
        self.btn.clicked.disconnect(self.startExtract)
        self.btn.clicked.connect(self.close)
    

    ####################
    ##### 기타 함수 #####
    ####################

    def setCurrentDir(self, dir):
        self.currentDir = dir

    def setDB(self, db):
        self.currentDB = db


    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = ExtractWindow()
    mainWindow.show()
    app.exec_()