from PyQt5 import uic
import keyboard
from PyQt5.Qt import QMenu
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QPlainTextEdit, QTableWidget, \
    QTableWidgetItem
import sys


class ManageWin(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.win_count = 0
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

    def clear_wins(self):
        self.wins.pop(self.wins[-1])
        print(self.wins)


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

    def contextMenuEvent(self, event):
        menu = QMenu(self)

        action_add = menu.addAction("Добавить строку")
        action_del = None
        if self.tableWidget.rowCount() > 0:
            action_del = menu.addAction("Удалить строку")
        choice = menu.exec_(self.mapToGlobal(event.pos()))
        if action_add == choice:
            self.add_row()
        if action_del == choice:
            self.del_row(self.tableWidget.currentRow())

    def add_row(self):
        self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
        item = QTableWidgetItem()
        self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 0, item)
        self.tableWidget.setCurrentItem(item)
        self.tableWidget.editItem(item)

    def del_row(self, row):
        self.tableWidget.removeRow(row)

    def closeEvent(self, event):
        ManageWin.clear_wins(ManageWin)


def exception_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


app = QApplication(sys.argv)
win = ManageWin()
win.show()
sys.excepthook = exception_hook
sys.exit(app.exec())
