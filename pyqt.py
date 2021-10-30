from PyQt5 import uic
import keyboard
import sqlite3
from PyQt5.Qt import QMenu
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QPlainTextEdit, QTableWidget, \
    QTableWidgetItem, QCheckBox
import sys

db = 'db/db.db'


class ManageWin(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.win_count = 0
        self.wins = []

    def initUI(self):
        self.setGeometry(500, 500, 300, 400)
        self.setWindowTitle("okno")
        self.btn = QPushButton('Note', self)

        self.btn.resize(100, 100)
        self.btn.move(100, 50)
        self.btn.clicked.connect(self.create_new_win)

        keyboard.add_hotkey('ctrl+1', self.btn.click, suppress=False)

        self.btn3 = QPushButton('List', self)

        self.btn3.resize(100, 100)
        self.btn3.move(100, 150)

        self.btn3.clicked.connect(self.create_new_win)

        keyboard.add_hotkey('ctrl+2', self.btn3.click, suppress=False)

    def create_new_win(self):

        win_title = f'New {self.sender().text()} ({self.win_count + 1})'
        # con = sqlite3.connect(db)
        # cur = con.cursor()
        # type_id = cur.execute("SELECT id FROM TYPES WHERE type=?", (self.sender().text(),)).fetchone()
        # cur.execute("""INSERT INTO windows (type.id, title) VALUES (?, ?)""", (type_id[0], win_title))

        # win_id = cur.lastrowid
        # print(win_id)
        # con.commit()
        # con.close()

        self.win_count += 1
        if self.sender().text() == 'Note':
            self.wins.append(WinObject(self, 0, self.win_count, win_title))
        else:
            self.wins.append(WinObject(self, 1, self.win_count, win_title))
        self.wins[-1].show()

    def clear_wins(self):
        self.wins.pop(-1)
        self.win_count -= 1


class WinObject(QMainWindow):
    def __init__(self, parent, type, win_id, win_title):
        super().__init__()
        self.type = type
        self.win_id = win_id
        self.title = win_title
        if self.type == 0:
            uic.loadUi('ui/win.ui', self)
        else:
            uic.loadUi('ui/win_list.ui', self)
        self.initUI()

    def initUI(self):
        if self.type == 0:
            self.setWindowTitle(f"{self.title}")
            self.qwe: QPlainTextEdit = self.qwe
            self.qwe.setStyleSheet('font: 12pt; background-color: #FEF9C7')
        else:
            self.setWindowTitle(f"{self.title}")

            self.tableWidget: QTableWidget = self.tableWidget
            self.tableWidget.setStyleSheet('font: 12pt; background-color: #F4DEFF')
            self.tableWidget.setColumnCount(2)
            self.check = QCheckBox()
            self.boxex = [self.check]

            b1, b2 = QPushButton(), QPushButton()
            b1.clicked.connect(self.add_row)
            b2.clicked.connect(self.del_row)
            keyboard.add_hotkey('alt+a', b1.click, suppress=False)
            keyboard.add_hotkey('alt+d', b2.click, suppress=False)

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
            self.del_row()

    def add_row(self):
        self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
        self.tableWidget.setCellWidget(self.tableWidget.rowCount() - 1, 0, QCheckBox())
        self.boxex.append(self.check)
        item = QTableWidgetItem()
        self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 1, item)
        self.tableWidget.setCurrentItem(item)
        self.tableWidget.resizeColumnsToContents()

    def del_row(self):
        self.tableWidget.removeRow(self.tableWidget.currentRow())

    def closeEvent(self, event):
        win.clear_wins()


def exception_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


app = QApplication(sys.argv)
win = ManageWin()
win.show()
sys.excepthook = exception_hook
sys.exit(app.exec())
