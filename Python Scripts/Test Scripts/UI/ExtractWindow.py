import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QDesktopWidget, QSizePolicy, QProgressBar, QVBoxLayout)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QThread, pyqtSignal, Qt

class LoadingThread(QThread):
    # 시험용
    progress = pyqtSignal(int)

    def run(self):
        for i in range(101):
            self.msleep(50) # 50밀리초마다 대기
            self.progress.emit(i)


class ExtractWindow(QWidget):
    def __init__(self):
        super().__init__()

        mainLayout = QVBoxLayout()

        # 진행 바
        self.progressBar = QProgressBar(self)
        self.progressBar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        mainLayout.addWidget(self.progressBar)

        # 확인 버튼
        self.btn = self.createButton('확인')
        self.btn.clicked.connect(self.close)
        mainLayout.addWidget(self.btn, alignment=Qt.AlignmentFlag.AlignHCenter)

        # self.startLoading()
        self.progressBar.setMinimum(0) # 무한 로딩
        self.progressBar.setMaximum(0)

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
            border-color: black;
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
            border-color: black;
            font: bold 23px;
            min-width: 10em;
            padding: 6px;
        }
        '''
        btn = QPushButton(text)
        btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        btn.setStyleSheet(btnStyle)
        return btn

    ###########################
    #####  로딩함수/시험용 #####
    ###########################

    def startLoading(self):
        self.btn.setEnabled(False)
        self.thread = LoadingThread()
        self.thread.progress.connect(self.updateProgress)
        self.thread.start()
        self.thread.finished.connect(self.loadingFinished)

    def updateProgress(self, value):
        self.progressBar.setValue(value)

    def loadingFinished(self):
        self.btn.setEnabled(True)

    ###########################
    ##### 추출 함수들 호출 #####
    ###########################


    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = ExtractWindow()
    mainWindow.show()
    app.exec_()