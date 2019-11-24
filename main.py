import sys
import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidgetItem


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.db = 'coffee.db'
        self.loadUi()
        self.btn.clicked.connect(self.change_table)

    def loadUi(self):
        con = sqlite3.connect(self.db)
        cur = con.cursor()
        result = cur.execute("SELECT * FROM about").fetchall()
        title = ['ID', 'Название сорта', 'Степень обжарки', 'Молотый/в зернах', 'Описание вкуса', 'Цена',
                 'Объём упаковки']

        self.tableWidget.setColumnCount(len(title))
        self.tableWidget.setHorizontalHeaderLabels(title)

        self.tableWidget.setRowCount(0)
        for i, row in enumerate(result):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))

        self.tableWidget.resizeColumnsToContents()

    def change_table(self):
        self.change_form = addEditCoffeeForm(self, self.db)
        self.change_form.show()
        # self.loadUi()


class addEditCoffeeForm(QWidget):
    def __init__(self, *db):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.db = db[-1]
        self.loadUi()
        self.tableWidget.itemChanged.connect(self.item_changed)
        self.save_btn.clicked.connect(self.save_table)
        self.modified = {}

    def loadUi(self):
        self.con = sqlite3.connect(self.db)
        cur = self.con.cursor()
        result = cur.execute("SELECT * FROM about").fetchall()
        self.titles = ['ID', 'Название сорта', 'Степень обжарки', 'Молотый/в зернах', 'Описание вкуса', 'Цена',
                       'Объём упаковки']

        self.tableWidget.setColumnCount(len(self.titles))
        self.tableWidget.setHorizontalHeaderLabels(self.titles)

        self.tableWidget.setRowCount(0)
        for i, row in enumerate(result):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()
        self.modified = {}

    def item_changed(self, item):
        self.modified[(self.titles[item.column()], item.row() + 1)] = item.text()

    def save_table(self):
        if self.modified:
            cur = self.con.cursor()
            for key in self.modified.keys():
                q = "UPDATE about SET\n [{}]='{}' WHERE id = {}\n".format(key[0], self.modified.get(key), key[1])
                cur.execute("UPDATE about SET\n [{}]='{}' WHERE id = {}\n".format(key[0], self.modified.get(key), key[1]))

            self.con.commit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
