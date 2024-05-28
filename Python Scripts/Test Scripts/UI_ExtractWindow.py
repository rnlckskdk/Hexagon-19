import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QDesktopWidget, QSizePolicy, QProgressBar, QVBoxLayout)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QThread, pyqtSignal, Qt
import sqlite3

import Backend_engine
import Database

# 쓰레드 관련한 것들은 db가 메모리가 아닌 특정 파일에 저장되어야 사용할 수 있음 (현재는 무시)
class LoadingThread(QThread):
    progress = pyqtSignal(int)

    def run(self):
        for i in range(101):
            self.msleep(50) # 50밀리초마다 대기
            self.progress.emit(i)

class WorkerThread(QThread):
    finished = pyqtSignal()

    def __init__(self, currentDir, currentDB):
        super().__init__()
        self.currentDir = currentDir
        self.currentDB = currentDB

    def run(self):
        # 각 스레드마다 별도의 DB 연결을 생성합니다.
        self.db_connection = sqlite3.connect(self.currentDB) # db 경로가 들어가야됨
        try:
            # Capstone_Backend 모듈의 함수가 DB 연결을 받도록 수정
            Backend_engine.explore_the_path(self.currentDir, self.db_connection)
        finally:
            self.db_connection.close()
        self.finished.emit()

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
        self.setWindowIcon(QIcon('Icon2.png'))
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

        self.btn.setText('확인')
        self.btn.clicked.disconnect(self.startExtract)
        self.btn.clicked.connect(self.close)

        self.update_signal.emit("updateResultBox")

        # self.btn.setEnabled(False)
        # 현재는 화면이 추출 중에 정지되는데 이를 해결하기 위한 쓰레드
        # (쓰레드에서 쓸 db가 파일경로로 전달되어야 해서 현재 비활성화)
        # self.thread = WorkerThread(self.currentDir, self.currentDB)
        # self.thread.finished.connect(self.onExtractFinished)
        # self.thread.start()

        # self.loadingThread = LoadingThread()
        # self.loadingThread.progress.connect(self.updateProgress)
        # self.loadingThread.start()

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
        self.loadingThread.terminate()  # 로딩 스레드 종료
    

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