import sys

from time import sleep

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget, QLineEdit, QPushButton, QLabel,
            QVBoxLayout, QHBoxLayout, QGridLayout, QComboBox)

from Falcon2.Features.Firmata import *

class UI():
    def __init__(self, args=sys.argv):
        self.args = args

        self.servo = Firmata()
        self.app = QApplication(self.args)
        self.grid = QGridLayout()

        self.modes = {"Input": 'in', 'Output': 'out', 'PWM': 'pwm'}

        self.window = QMainWindow()
        self.window.setWindowTitle('Servo Control with Firmata Protocol')
        self.window.setStyleSheet('background-color: black;')
        self.window.setWindowOpacity(0.9)
        self.window.setFixedSize(500, 500)
        self.window.move(350, 100)

        title = QLabel('<center><h1 style="color: white; background-color: #086cff">Servo Testing Session</h1></center>', parent=self.window)
        title.setGeometry(0, 0, 500, 50)

        self.InitUI()

    def InitUI(self):
        text_1 = QLabel("Select Arduino Pin: ", parent=self.window)
        text_1.setStyleSheet("color: white; font-size: 26px; text-align: left;")
        text_1.setGeometry(0, 70, 250, 40)

        self.pin_line_edit = QLineEdit(parent=self.window)
        self.pin_line_edit.setStyleSheet('color: white; background-color: #ff1750;')

        self.pin_box = QComboBox(parent=self.window)
        self.pin_box.setGeometry(260, 70, 200, 40)
        self.pin_box.setStyleSheet("background-color: #068cff; color: white;")
        self.pin_box.setLineEdit(self.pin_line_edit)

        text_2 = QLabel("Choose pin mode: ", parent=self.window)
        text_2.setStyleSheet("color: white; font-size: 27px; text-align: left;")
        text_2.setGeometry(0, 140, 250, 40)

        self.mode_box = QComboBox(parent=self.window)
        self.mode_box.setGeometry(260, 140, 200, 40)
        self.mode_box.setStyleSheet('color: while; background-color: yellow;')
        self.mode_box.addItems(['Input', 'Output', 'PWM'])
        self.mode_box.setCurrentText('PWM')

        text_3 = QLabel('<hr style="color: white;">', parent=self.window)
        text_3.setGeometry(20, 200, 460, 20)

        text_4 = QLabel("<center>Read Pin State (or Value)</center>", parent=self.window)
        text_4.setStyleSheet('color: lime; font-size: 30px;')
        text_4.setGeometry(0, 223, 500, 40)

        self.read_box = QLineEdit(parent=self.window)
        self.read_box.setReadOnly(True)
        self.read_box.setText('Outputs here!')

        self.read_box.setStyleSheet('color: black; background-color: yellow; font-size: 28px;')
        self.read_box.setGeometry(30, 270, 300, 40)

        self.btn2 = QPushButton("Start", parent=self.window)
        self.btn2.setStyleSheet('background-color: #ffffff; color: lime; border-radius: 20px; font-size: 25px;')
        self.btn2.setGeometry(350, 270, 120, 40)
        self.btn2.clicked.connect(self.Read)

        text_5 = QLabel('<hr style="color: white;">', parent=self.window)
        text_5.setGeometry(20, 320, 460, 20)

        text_6 = QLabel('<hr style="color: white;">', parent=self.window)
        text_6.setGeometry(20, 320, 460, 20)

        self.btn3 = QPushButton("Servo Test", parent=self.window)
        self.btn3.setStyleSheet('background-color: #ffffff; color: blue; border-radius: 20px; font-size: 25px;')
        self.btn3.setGeometry(15, 350, 140, 40)
        self.btn3.clicked.connect(self.ServoTest)

        self.btn4 = QPushButton("Auto Test", parent=self.window)
        self.btn4.setStyleSheet('background-color: #ffffff; color: purple; border-radius: 20px; font-size: 25px;')
        self.btn4.setGeometry(180, 350, 140, 40)

        self.btn5 = QPushButton("Quick Test", parent=self.window)
        self.btn5.setStyleSheet('background-color: #ffffff; color: orangered; border-radius: 20px; font-size: 25px;')
        self.btn5.setGeometry(345, 350, 140, 40)

        text_7 = QLabel('<hr style="color: white;">', parent=self.window)
        text_7.setGeometry(15, 400, 470, 20)

        text_8 = QLabel("<b><center>Enter the value you want to send:</center></b>", parent=self.window)
        text_8.setGeometry(0, 410, 500, 40)
        text_8.setStyleSheet("color: #ff1717; font-size: 25px; text-align: left;")

        self.val_box = QLineEdit(parent=self.window)
        self.val_box.setGeometry(20, 450, 275, 40)
        self.val_box.setText('0')
        self.val_box.setStyleSheet("color: #ffffff; background-color: #057cff; border-radius: 12px; font-size: 30px;")

        self.btn = QPushButton("Send", parent=self.window)
        self.btn.setGeometry(320, 450, 150, 40)
        self.btn.setStyleSheet('background-color: #ffffff; color: #057cff; border-radius: 20px; font-size: 25px; text-align: center;')
        self.btn.clicked.connect(self.show)

        for i in range(2, 14):
            self.pin_box.addItem(f"{i}")
        for i in range(22, 54):
            self.pin_box.addItem(f"{i}")
        for i in range(0, 16):
            self.pin_box.addItem(f"A{i}")

    def ServoTest(self):
        try:
            pin = self.pin_line_edit.text()

            self.servo.SetMode('pwm')
            self.servo.Write(pin, 0)

            for i in range(0, 180):
                self.servo.Write(pin, i)
                sleep(0.001)
        except Exception as e:
            print_error(e, __name__+".ServoTest()")

    def Read(self):
        try:
            pin = self.pin_line_edit.text()

            self.servo.SetMode('in')
            value = self.servo.Read(pin)
            self.read_box.setText(str(value))
        except Exception as e:
            print_error(e, __name__+".Read()")

    def show(self):
        try:
            value = self.val_box.text()
            servo = self.pin_line_edit.text()
            mode = self.mode_box.currentText()

            self.servo.SetMode(self.modes[mode])
            self.servo.Write(servo, value)
        except Exception as e:
            print(e)

    def Launch(self, exit=True):
        self.window.show()
        sys.exit(self.app.exec_()) if exit else self.app.exec_()

def main():
    app = UI()
    app.Launch()

if __name__ == '__main__':
    main()
