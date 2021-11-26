from PyQt5 import uic
import keyboard
import sqlite3
from PyQt5.Qt import QMenu
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QTableWidget, \
    QTableWidgetItem, QCheckBox, QPlainTextEdit
import sys

db = 'db/db.db'


def query_to_get(query, params=(), is_insert=False):
    con = None
    try:
        con = sqlite3.connect(db)
        cur = con.cursor()
        res = cur.execute(query, params).fetchall()
        con.close()
        return res
    except sqlite3.Error as e:
        print('Ошибка с бд', e)
    finally:
        print('Close connection')
        if con:
            con.close()


class ManageWin(QMainWindow):
    def __init__(self):
        super().__init__()
        self.win_count = 0
        self.wins = []
        self.initUI()

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

        self.btndel = QPushButton('Delete all notes', self)

        self.btndel.resize(100, 50)
        self.btndel.move(100, 350)

        self.btndel.clicked.connect(self.clear_db)

        keyboard.add_hotkey('ctrl+d', self.btndel.click, suppress=False)

        self.open_win()

    def close_wins(self):
        while len(self.wins) > 0:
            for i in self.wins:
                i.close()

    def clear_db(self):
        self.close_wins()
        con = sqlite3.connect(db)
        cur = con.cursor()
        cur.execute("DELETE FROM windows")
        cur.execute("DELETE FROM notes")
        con.commit()
        con.close()

    def open_win(self):
        con = sqlite3.connect(db)
        cur = con.cursor()
        db_wins = query_to_get("SELECT * FROM windows")
        for obj in db_wins:
            db_win_content = cur.execute("SELECT content FROM notes WHERE window_id=?", (obj[0],)).fetchone()
            if db_win_content != None:
                self.win_count += 1
                print(db_win_content[0].split(', '))
                self.wins.append(WinObject(self, obj[1], obj[2], obj[0], db_win_content[0]))
                self.wins[-1].show()
        con.commit()
        con.close()

    def create_new_win(self):
        win_title = f'New {self.sender().text()} ({self.win_count + 1})'
        con = sqlite3.connect(db)
        cur = con.cursor()
        type_id = query_to_get("SELECT id FROM TYPES WHERE type=?", (self.sender().text(),))
        cur.execute("""INSERT INTO windows (type_id, title) VALUES (?, ?)""", (type_id[0][0], win_title))
        con.commit()
        winn = query_to_get("SELECT id FROM windows")
        table_id = winn[-1][0]
        cur.execute("""INSERT INTO notes (window_id, content) VALUES (?, ?)""", (table_id, ''))
        con.commit()
        con.close()

        self.win_count += 1
        if self.sender().text() == 'Note':
            self.wins.append(WinObject(self, 1, win_title, table_id))
        else:
            self.wins.append(WinObject(self, 2, win_title, table_id))
        self.wins[-1].show()

    def clear_wins(self, win_name):
        self.wins.pop(self.wins.index(win_name))
        self.win_count -= 1

    def closeEvent(self, event):
        self.close_wins()


class WinObject(QMainWindow):
    def __init__(self, parent, type, win_title, table_id, content=None):
        super().__init__()
        self.type = type
        self.title = win_title
        self.table_id = table_id
        self.content = content
        if self.type == 1:
            uic.loadUi('ui/win.ui', self)
        else:
            uic.loadUi('ui/win_list.ui', self)
        self.initUI()

    def initUI(self):
        if self.type == 1:
            self.setWindowTitle(f"{self.title}")
            self.qwe: QPlainTextEdit = self.qwe
            self.qwe.setStyleSheet('font: 12pt; background-color: #FEF9C7')
            if self.content:
                self.qwe.setPlainText(self.content)
        else:
            self.setWindowTitle(f"{self.title}")

            self.tableWidget: QTableWidget = self.tableWidget
            self.tableWidget.setStyleSheet('font: 12pt; background-color: #F4DEFF')
            self.tableWidget.setColumnCount(2)
            self.boxex = []

            b1, b2 = QPushButton(), QPushButton()
            b1.clicked.connect(self.add_row)
            b2.clicked.connect(self.del_row)
            keyboard.add_hotkey('alt+a', b1.click, suppress=False)
            keyboard.add_hotkey('alt+d', b2.click, suppress=False)

    def save_data(self):
        con = sqlite3.connect(db)
        cur = con.cursor()
        if self.type == 1:
            cur.execute("UPDATE notes SET content = ? WHERE window_id = ?",
                        (self.qwe.toPlainText(), self.table_id))
        else:
            cur.execute("UPDATE notes SET content = ? WHERE window_id = ?",
                        (str(self.table_to_list()), self.table_id))
        con.commit()
        con.close()

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
        check = QCheckBox()
        self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
        self.tableWidget.setCellWidget(self.tableWidget.rowCount() - 1, 0, check)
        self.boxex.append(check)

        item = QTableWidgetItem()
        self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 1, item)
        self.tableWidget.setCurrentItem(item)
        self.tableWidget.resizeColumnsToContents()

    def table_to_list(self):
        # table = self.tableWidget
        # result = []
        # for col in range(table.columnCount()):
        #     rows = []
        #     for row in range(table.rowCount()):
        #         if col == 0:
        #             item = table.item(row, col)
        #             print(item, 0)
        #         else:
        #             item = table.item(row, col)
        #             print(item)
        #         rows.append(item.text() if item else '')
        #     result.append(rows)
        # return result
        result = []
        for row in range(self.tableWidget.rowCount()):
            rows = []
            for col in range(self.tableWidget.columnCount()):
                if col == 0:
                    item = self.boxex[row].checkState()
                    rows.append(item)
                else:
                    item = self.tableWidget.item(row, col)
                    rows.append(item.text() if item else '')
            result.append(rows)
        return result

    def del_row(self):
        self.tableWidget.removeRow(self.tableWidget.currentRow())
        self.boxex.pop(self.tableWidget.currentRow())

    def closeEvent(self, event):
        self.save_data()
        win.clear_wins(self)


def exception_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


app = QApplication(sys.argv)
win = ManageWin()
win.show()
sys.excepthook = exception_hook
sys.exit(app.exec())
