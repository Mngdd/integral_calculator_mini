import sys

from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow
import wolframalpha
from urllib.request import urlopen


class calculata(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui.ui', self)
        self.setWindowTitle('производные функции и первообразные приколы')
        self.go1.clicked.connect(self.calculate)
        self.go2.clicked.connect(self.calculate)
        self.go3.clicked.connect(self.calculate)
        self.up.clicked.connect(self.move_)
        self.down.clicked.connect(self.move_)

        self.pixmapA = QPixmap()
        self.pixmapB = QPixmap()
        self.pixmapC = QPixmap()

        self.ID = "EEGTYX-KXW3JHU59T"
        self.client = wolframalpha.Client(self.ID)

    def move_(self):
        if 'down' in self.sender().objectName():
            self.C.setText(self.B.text())
            self.B.setText(self.A.text())
            self.A.setText('')

            # if self.pixmapB is not None:
            #     self.picC.setPixmap(self.pixmapB)
            # else:
            #     self.picC.clear()
            #     self.pixmapC = None
            # if self.pixmapA is not None:
            #     self.picB.setPixmap(self.pixmapA)
            # else:
            #     self.picB.clear()
            #     self.pixmapB=None
            self.picA.clear()
            self.picB.clear()
            self.picC.clear()
            # self.pixmapA = None
        else:
            # self.A.setText(self.B.text())
            # self.B.setText(self.C.text())
            # self.C.setText('')
            #
            # if self.pixmapB is not None:
            #     self.picA.setPixmap(self.pixmapB)
            # else:
            #     self.picA.clear()
            #     self.pixmapA = None
            # if self.pixmapC is not None:
            #     self.picB.setPixmap(self.pixmapC)
            # else:
            #     self.picB.clear()
            #     self.pixmapB = None
            # self.picC.clear()
            # self.pixmapC = None

            self.picA.clear()
            self.picB.clear()
            self.picC.clear()
    
    def calculate(self):
        if '1' in self.sender().objectName():  # от произв
            self.search(self.A.text(), 'B', 'Integrate')
            self.search(self.B.text(), 'C', 'Integrate')
            self.search(self.A.text(), 'A', '', True)
        elif '2' in self.sender().objectName():  # от ф-ции
            self.search(self.B.text(), 'A', 'D')
            self.search(self.B.text(), 'C', 'Integrate')
            self.search(self.B.text(), 'B', '', True)
        else:  # от первообр
            self.search(self.C.text(), 'B', 'D')
            self.search(self.B.text(), 'A', 'D')
            self.search(self.C.text(), 'C', '', True)

    def search(self, from_: str, to, what, no_func=False):
        # print(from_.find('+ constant'))
        question = from_ if no_func else f'{what}[{from_},x]'
        res = self.client.query(question.strip(), params=(("format", "image,plaintext"),))
        if not no_func:
            pic = next(res.results)['subpod']['img']['@src']
            txt = next(res.results)['subpod']['img']['@alt']
        else:
            pic = list(res)[0]['subpod']['img']['@src']
            txt = list(res)[0]['subpod']['img']['@alt']
        print(no_func, pic, txt)
        if to == 'A':
            self.A.setText(txt if no_func else txt.split('=')[1][1:])
            self.pixmapA.loadFromData(self.load(pic))
            self.picA.setPixmap(self.pixmapA)
        elif to == 'B':
            self.B.setText(txt if no_func else txt.split('=')[1][1:])
            self.pixmapB.loadFromData(self.load(pic))
            self.picB.setPixmap(self.pixmapB)
        else:
            self.C.setText(txt if no_func else txt.split('=')[1][1:])
            self.pixmapC.loadFromData(self.load(pic))
            self.picC.setPixmap(self.pixmapC)
        return pic, txt

    def load(self, url):
        image2_byt = urlopen(url).read()
        return image2_byt


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    sys.excepthook = except_hook
    app = QApplication(sys.argv)
    ex = calculata()
    ex.show()
    sys.exit(app.exec_())
