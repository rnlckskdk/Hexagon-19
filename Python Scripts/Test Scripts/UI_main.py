import sys
import UI_SearchWindow, UI_ExtractWindow
# from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import (QApplication, QDesktopWidget, QGridLayout, QVBoxLayout, QPushButton, QSizePolicy, 
QWidget, QLineEdit, QFileDialog, QMessageBox, QTableWidget, QAbstractItemView, QHeaderView, QTableWidgetItem)
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtCore import Qt, QUrl

# sys.path.append("C:/Users/sj/Documents/GitHub/Hexagon-19/Python Scripts/Test Scripts")
import Backend_engine
import Database

class App(QWidget):
    def __init__(self):
        super().__init__()
        # 추출 결과 창
        resultBox = self.createResultTable()
        # 전체 클래스 내에서 사용할 변수들
        self.currentDir = ''
        self.searchWindow = UI_SearchWindow.SearchWindow()
        # self.extractWindow = UI_ExtractWindow.ExtractWindow()
        self.extractWindow = None
        self.db = Database.DB()
        self.searchWindow.setDB(self.db)

        # 결과창 업데이트 위한 시그널 연결(추출 창으로부터)
        # self.extractWindow.update_signal.connect(self.updateResultBox)

        # 레이아웃 설정
        gridLayout = QGridLayout()
        topLayout = QGridLayout()
        mainLayout = QVBoxLayout()
        menuLayout = QVBoxLayout()
        mainLayout.addLayout(topLayout)
        mainLayout.addLayout(gridLayout)
        gridLayout.addLayout(menuLayout, 0, 0)
        gridLayout.addWidget(resultBox, 0, 1)
    
        # 디렉토리 입력,표시 창 / 레이아웃 설정
        self.dirLine = self.createLine('현재 경로')
        self.dirLine.returnPressed.connect(self.confirmDir)
        topLayout.addWidget(self.dirLine, 0, 0)

        # 파일 탐색기 버튼, 디렉토리 확정 버튼 / 시그널 연결 / 레이아웃 설정
        fileBtn = self.createButton('파일탐색기')
        confirmBtn = self.createButton('업데이트')
        fileBtn.clicked.connect(self.folderOpen)
        confirmBtn.clicked.connect(self.confirmDir)
        topLayout.addWidget(fileBtn, 0, 2, 1, 2)
        topLayout.addWidget(confirmBtn, 0, 4, 1, 2)

        # 추출, 검색, 정리 버튼 생성 / 시그널 연결 / 레이아웃 설정
        extractBtn = self.createButton('추출')
        searchBtn = self.createButton('검색')
        organizeBtn = self.createButton('정리')
        extractBtn.clicked.connect(self.openExtractWindow)
        searchBtn.clicked.connect(self.openSearchWindow)
        # organizeBtn.clicked.connect()
        menuLayout.addWidget(extractBtn)
        menuLayout.addWidget(searchBtn)
        menuLayout.addWidget(organizeBtn)
        menuLayout.addStretch(1)
    
        # 레이아웃에 공간 추가
        gridLayout.setColumnStretch(1, 1)
        gridLayout.setRowStretch(0, 1)
        

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
        width = 2200
        height = 1200
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

    # 종료 시 종료 확인
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Hexagon-19', 
            "정말 종료하시겠습니까?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    # 결과 창 생성 메소드
    def createResultTable(self):
        columns = ['이름', '확장자', '경로', '키워드']
        self.tableWidget = QTableWidget()
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        # tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setHorizontalHeaderLabels(columns)
        self.tableWidget.cellClicked.connect(self.linkToLocalFile)

        return self.tableWidget

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
        self.searchWindow.setCurrentDir(self.currentDir)

    # 검색 버튼 시그널
    def openSearchWindow(self):
        self.searchWindow.show()
        
    # 추출 버튼 시그널
    def openExtractWindow(self):
        del self.extractWindow
        self.extractWindow = UI_ExtractWindow.ExtractWindow()
        # 결과창 업데이트 위한 시그널 연결(추출 창으로부터)
        self.extractWindow.update_signal.connect(self.updateResultBox)

        self.extractWindow.setCurrentDir(self.currentDir)
        self.extractWindow.setDB(self.db)
        self.extractWindow.show()

    # 결과 창에서 파일 열기 위한 메소드
    def linkToLocalFile(self, row, column):
        if column == 2:
            item = self.tableWidget.item(row, column)
            if item:
                url = item.data(Qt.DisplayRole)
                QDesktopServices.openUrl(QUrl.fromLocalFile(url))

    # 결과 창 업데이트
    def updateResultBox(self):
        # 테이블 초기화/업데이트
        self.tableWidget.setRowCount(0)

        # 결과 받아 오기
        # Capstone_Backend.explore_the_path(self.currentDir, self.currentDB)
        resultList = self.db.getFileInfoFromDB('') # serach all
        ### row 업데이트 ###
        for i in range(0, len(resultList)):
            rowPosition = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowPosition)
            self.tableWidget.setItem(rowPosition, 0, QTableWidgetItem(resultList[i][1])) # 이름
            self.tableWidget.setItem(rowPosition, 1, QTableWidgetItem(resultList[i][2])) # 확장자
            self.tableWidget.setItem(rowPosition, 2, QTableWidgetItem(resultList[i][0] + '/' + resultList[i][1] + '.' + resultList[i][2])) # 경로
            self.tableWidget.setItem(rowPosition, 3, QTableWidgetItem(resultList[i][3])) # 태그




if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = App()
    app.exec_()