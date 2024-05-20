import sys
import SearchWindow, ExtractWindow
# from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import (QApplication, QDesktopWidget, QGridLayout, QVBoxLayout, 
QPushButton, QSizePolicy, QWidget, QLineEdit, QFileDialog)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt


class App(QWidget):
    def __init__(self):
        super().__init__()
        # 전체 클래스 내에서 사용할 변수들
        self.currentDir = ''
        self.searchWindow = None
        self.extractWindow = None

        # 레이아웃 설정
        gridLayout = QGridLayout()
        horizontalLayout = QGridLayout()
        mainLayout = QVBoxLayout()
        mainLayout.addLayout(horizontalLayout)
        mainLayout.addLayout(gridLayout)
    
        # 디렉토리 입력,표시 창 / 레이아웃 설정
        self.dirLine = self.createLine('현재 경로')
        self.dirLine.returnPressed.connect(self.confirmDir)
        horizontalLayout.addWidget(self.dirLine, 0, 0)

        # 파일 탐색기 버튼, 디렉토리 확정 버튼 / 시그널 연결 / 레이아웃 설정
        fileBtn = self.createButton('파일탐색기')
        confirmBtn = self.createButton('경로 확정')
        fileBtn.clicked.connect(self.folderOpen)
        confirmBtn.clicked.connect(self.confirmDir)
        horizontalLayout.addWidget(fileBtn, 0, 2, 1, 2)
        horizontalLayout.addWidget(confirmBtn, 0, 4, 1, 2)

        # 추출, 검색, 정리 버튼 생성 / 시그널 연결 / 레이아웃 설정
        extractBtn = self.createButton('추출')
        searchBtn = self.createButton('검색')
        organizeBtn = self.createButton('정리')
        extractBtn.clicked.connect(self.openExtractWindow)
        searchBtn.clicked.connect(self.openSearchWindow)
        # organizeBtn.clicked.connect()
        gridLayout.addWidget(extractBtn, 0, 0, alignment=Qt.AlignmentFlag.AlignHCenter)
        gridLayout.addWidget(searchBtn, 0, 1, alignment=Qt.AlignmentFlag.AlignHCenter)
        gridLayout.addWidget(organizeBtn, 0, 2, alignment=Qt.AlignmentFlag.AlignHCenter)

        # ui 설정
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
        title = "Hexagon-19"
        self.setWindowTitle(title)
        width = 1280
        height = 360
        self.resize(width, height)
        self.setWindowIcon(QIcon('Icon2.png'))
        self.center()
        self.show()

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
        btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        btn.setStyleSheet(btnStyle)
        return btn

    # 라인 생성 메소드
    def createLine(self, text):
        lineStyle = '''
        QLineEdit
        {
            font: bold
        }
        '''
        dirLine = QLineEdit(self)
        dirLine.setPlaceholderText(text)
        dirLine.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        dirLine.setStyleSheet(lineStyle)
        return dirLine

    #################################
    ##### 버튼 시그널 위한 메소드 #####
    #################################

    # 파일 탐색기 메소드
    def folderOpen(self):
        fname = QFileDialog.getExistingDirectory(self,'폴더선택','')
        self.dirLine.setText(fname)

    # 경로 확정 메소드
    def confirmDir(self):
        self.currentDir = self.dirLine.text()
        print(self.currentDir)

    def openSearchWindow(self):
        if self.searchWindow == None:
            self.searchWindow = SearchWindow.SearchWindow()
        self.searchWindow.show()
        
    def openExtractWindow(self):
        if self.extractWindow == None:
            self.extractWindow = ExtractWindow.ExtractWindow()
        self.extractWindow.show()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = App()
    app.exec_()