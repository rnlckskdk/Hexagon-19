from PyQt5.QtWidgets import QApplication
from UI_main import App
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = App()
    app.exec_()


#
# 메모
# 
# 현재 추출을 한 번 진행한 이후 같은 폴더를 대상으로 다시 한 번 추출을 할 경우 같은 파일이 db안에 두번 정보가 저장되버림
#
# db가 메모리에 저장되는 방식이라 꺼지면 날아감 + 추출 창에서 쓰레드 이용해서 추출 중에 진행 중임을 표시하는 작업이
# 작동하지 않음 (db가 보조기억장치에 있어야 쓰레드에서 별개의 작업 수행 시 db 접근이 가능해짐)
#
# 위가 해결 시 이미 추출한 결과에 대해 해당 폴더 안에서 변경점이 없는 경우 두 번 추출하지 않게 추적/관리할 필요가 있을 것 같음