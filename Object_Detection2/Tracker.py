import sys
from threading import Thread

from Falcon2.System.IO_Style import *

from Falcon2.Features.Video import *
from Falcon2.Features.Firmata import *

from Falcon2.Networks.Socket_Server import *

from Falcon2.Object_Detection.ObjectFinder import *
from Falcon2.main.Properties import *

class Tracker():
    def __init__(self, object_name):
        self.object_name = object_name
        self.running = True

        self.protocol = Firmata()
        self.protocol.SetMode('pwm')

        self.server = Server(LOCAL_IP, VIDEO_PORT, show=True)
        self.Server.Start()

        self.servo_x = SERVO_X
        self.servo_y = SERVO_Y

        self.MIN_POS = 0
        self.MAX_POS = 180
        self.MID_POS_X = (40, 50)
        self.MID_POS_Y = (40, 50)

        self.srv_x = 0
        self.srv_y = 0

        self._servo_err_attempts = 0

        self.servos = {'x': self.servo_x, 'y': self.servo_y}

        self.video = Video()
        self.video.SetSize(200, 200)

        self.finder = Finder()
        self._start_finder()

    def SetObject(self, object_name):
        self.object_name = object_name

    def _start_finder(self):
        Thread(target=self.finder.Find).start()

    def _map(self, value):
        val_a = 650/180
        return value/val_a

    def _move_servo(self, servo, pos):
        try:
            self.protocol.Write(self.servos[servo], pos)
        except Exception as e:
            print_error(e, __name__+"._move_servo()")

    def _track_with_servo(self):
        try:
            (x, y), _ = self.finder.GetAxisValue(self.object_name)

            if self.MID_POS_X[0] <= int(x):
                if self.srv_x > self.MIN_POS:
                    self.srv_x -= 1
            elif self.MID_POS_X[1] >= int(x):
                if self.srv_x < self.MAX_POS:
                    self.srv_x += 1

            if self.MID_POS_Y[0] <= int(x):
                self.srv_y += 1
            elif self.MID_POS_Y[1] >= int(x):
                self.srv_y -= 1

            self._move_servo('x', self.srv_x)
            self._move_servo('y', self.srv_y)

            print(x, y)
        except Exception as e:
            self._servo_err_attempts += 1
            if self._servo_err_attempts < 3:
                print_error(e, __name__+"._track_with_servo()")

    def Track(self):
        while self.running:
            try:
                _, video = self.video.GetVideo()

                self.finder.SetVideo(video)
                new_video = self.finder.GetVideo()

                show = self.video.ShowVideo(new_video)

                if show is False:
                    self.finder.Stop()
                    break
                self._track_with_servo()
            except Exception as e:
                print_error(e, __name__+".Track()")

def main():
    tracker = Tracker(sys.argv[1])
    tracker.Track()

if __name__ == '__main__':
    Thread(target=main).start()
