from PyQt5 import uic, Qt
import keyboard
from PyQt5.QtGui import QTextListFormat, QTextCursor, QTextDocument
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QPlainTextEdit, QTextEdit, QTableWidget
import sys


class ManageWin(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.win_count = 0
        # self.win_list_count = 0
        self.wins = []

    def initUI(self):
        self.setGeometry(500, 500, 300, 400)
        self.setWindowTitle("okno")

        self.btn = QPushButton('Создать записку', self)

        self.btn.resize(100, 100)
        self.btn.move(100, 50)
        self.btn.clicked.connect(self.create_note)

        keyboard.add_hotkey('ctrl+1', self.btn.click, suppress=False)

        self.btn3 = QPushButton('Создать список', self)

        self.btn3.resize(100, 100)
        self.btn3.move(100, 150)

        self.btn3.clicked.connect(self.create_note)

        keyboard.add_hotkey('ctrl+2', self.btn3.click, suppress=False)

    def create_note(self):
        self.win_count += 1
        for i in self.wins:
            if not i.isVisible():
                self.wins.pop(self.wins.index(i))
                self.win_count = 1
        if self.sender().text() == 'Создать записку':
            self.wins.append(WinObject(self, 0, self.win_count))
        else:
            self.wins.append(WinObject(self, 1, self.win_count))
        self.wins[-1].show()

    # def create_list_note(self):
    #     self.win_list_count += 1
    #     for i in self.wins:
    #         if not i.isVisible():
    #             self.wins.pop(self.wins.index(i))
    #             self.win_list_count = 1
    #     self.wins.append(Win_List(self, self.win_list_count))
    #     self.wins[-1].show()


class WinObject(QMainWindow):
    def __init__(self, *args):
        super().__init__()
        if args[1] == 0:
            uic.loadUi('ui/win.ui', self)
        else:
            uic.loadUi('ui/win_list.ui', self)
        self.initUI(args)

    def initUI(self, args):
        if args[1] == 0:
            self.setWindowTitle(f"Новая записка {args[-1]}")
            self.qwe: QPlainTextEdit = self.qwe
            self.qwe.setStyleSheet('font: 12pt; background-color: #FEF9C7')
        else:
            self.setWindowTitle(f"Новый список {args[-1]}")
            self.tableWidget: QTableWidget = self.tableWidget
            self.tableWidget.setStyleSheet('font: 12pt; background-color: #F4DEFF')


# class WinNote(QMainWindow):
#     def __init__(self, *args):
#         super().__init__()
#         uic.loadUi('ui/win.ui', self)
#         self.initUI(args)
#
#     def initUI(self, args):
#         self.i = 0
#         self.setWindowTitle(f"Новая записка {args[-1]}")
#         self.qwe: QPlainTextEdit = self.qwe
#         self.qwe.setStyleSheet('font: 12pt; background-color: #FEF9C7')
#         self.btn2.clicked.connect(self.create_list)
#         keyboard.add_hotkey('l', self.btn2.click, suppress=False)
#
#     def create_list(self):
#         if self.i == 0:
#             self.qwe.insertPlainText(f'{1}) ')
#         else:
#             self.qwe.insertPlainText(f'\n{self.i + 1}) ')
#         self.i += 1
#
#
# class WinList(QMainWindow):
#     def __init__(self, *args):
#         super().__init__()
#         uic.loadUi('ui/win_list.ui', self)
#         self.initUI(args)
#
#     def initUI(self, args):
#         self.i = 0
#         self.setWindowTitle(f"Новый список {args[-1]}")
#         self.tableWidget: QTableWidget = self.tableWidget
#         self.tableWidget.setStyleSheet('font: 12pt; background-color: #F4DEFF')
#         # self.btn2.clicked.connect(self.create_list)
#         # keyboard.add_hotkey('ctrl+2', self.btn2.click, suppress=False)
#
#     def create_list(self):
#         if self.i == 0:
#             self.qwe.insertPlainText(f'{1}) ')
#         else:
#             self.qwe.insertPlainText(f'\n{self.i + 1}) ')
#         self.i += 1


def exception_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


app = QApplication(sys.argv)
win = ManageWin()
win.show()
sys.excepthook = exception_hook
sys.exit(app.exec())
