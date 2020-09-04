from pyfirmata import util, ArduinoMega, SERVO

from Falcon2.main.Properties import *
from Falcon2.System.IO_Style import *

class ServoControl():
    def __init__(self, auto_init=True):
        self.is_activated = True

        self.servo_x = SERVO_X
        self.servo_y = SERVO_Y
        self.port = DEVICE_PORT

        try:
            self.board = ArduinoMega(self.port)
            self.iterator = util.Iterator(self.board)
        except Exception as e:
            self.is_activated = False
            print_error(e, __name__)

        if auto_init is True and self.is_activated is True:
            self.Setup()

        if not self.is_activated:
            print_error("No hardware was founded! So `ServoControl` is closing!", __name__)

    def Setup(self):
        try:
            self.iterator.start()
            self.board.digital[self.servo_x].mode = SERVO
            self.board.digital[self.servo_y].mode = SERVO
        except Exception as e:
            print_error(e, __name__+".Setup()")

    def GetData(self):
        pass

    def SetTo(self, servo, pos):
        if self.is_activated:
            servos = {'x': self.servo_x, 'y': self.servo_y}
            self.board.digital[servos[servo]].write(pos)

    def CSetTo(self, pin, pos, digital=True):
        if self.is_activated:
            if digital:
                self.board.digital[pin].write(pos)
            else:
                self.board.analog[pin].write(pos)

def main():
    servo = ServoControl(auto_init=True)

    while True:
        s = str(input('servo $$ '))

        if s == 'quit':
            break

        pos = int(input('pos $$ '))
        servo.SetTo(s, pos)

if __name__ == '__main__':
    main()
