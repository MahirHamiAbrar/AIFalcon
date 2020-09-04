from pyfirmata import util, Arduino, ArduinoMega, SERVO, INPUT, OUTPUT

from Falcon2.main.Properties import *
from Falcon2.System.IO_Style import *

class Firmata():
    def __init__(self, auto_init=True):
        self.is_activated = True

        self.port = DEVICE_PORT
        self.mode = None

        self.modes = {'in': INPUT, 'out': OUTPUT, 'pwm': SERVO}

        try:
            self.board = ArduinoMega(self.port)
            self.iterator = util.Iterator(self.board)
        except Exception as e:
            self.is_activated = False
            print_error(e, __name__)

        if auto_init is True and self.is_activated is True:
            self._initialize()

        if not self.is_activated:
            print_error("No hardware was founded! So `Firmata` is closing!", __name__)

    def _initialize(self):
        try:
            self.iterator.start()
        except Exception as e:
            print_error(e, __name__)

    def SetMode(self, mode):
        self.mode = self.modes[mode]

    def _get_pin_mode(self, pin):
        try:
            if 'A' in str(pin):
                pin = int(str(pin).split('A')[1])
                digital = False
            else:
                pin = int(pin)
                digital = True
            return pin, digital
        except Exception as e:
            print_error(e, __name__+"._get_pin_mode()")

    def Write(self, pin, value):
        try:
            if self.is_activated:
                pin, digital = self._get_pin_mode(pin)

                if digital:
                    self.board.digital[pin].mode = self.mode
                    self.board.digital[pin].write(value)
                else:
                    self.board.analog[pin].mode = self.mode
                    self.board.analog[pin].write(value)
                #else:
                    #print_error("Analog pin is currently readable only!", __name__+".Write()")
        except Exception as e:
            print_error(e, __name__+".Write()")

    def Read(self, pin):
        try:
            if self.is_activated:
                pin, digital = self._get_pin_mode(pin)

                if digital:
                    self.board.digital[pin].mode = self.mode
                    return self.board.digital[pin].read()
                else:
                    self.board.analog[pin].mode = self.mode
                    return self.board.analog[pin].read()
        except Exception as e:
            print_error(e, __name__+".Read()")

def main():
    protocol = Firmata()
    protocol.SetMode('out')

    while True:
        pin = input("pin $$ ")

        if pin == 'quit':
            break

        val = input("value $$ ")

        protocol.Write(pin, int(val))

if __name__ == '__main__':
    main()
