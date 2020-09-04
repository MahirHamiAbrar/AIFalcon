from Falcon2.System.IO_Style import *
from Falcon2.main.Starter import Start
from Falcon2.Object_Detection.Tracker import Tracker
from Falcon2.Processor.MainProcessor import Processor

from threading import Thread

class AI():
	def __init__(self):
		#Thread(target=Start).start()
		self.tracker = Tracker()
		self.LaunchTracker()
		
		self.processor = Processor()

	def LaunchTracker(self):
		Thread(target=self.tracker.Track).start()
		print_info("Object Detection System has started successfully.", __name__)

	def Warn(self):
		print_warning("write [quit] to quit", __name__)

	def Activate(self):
		self.Warn()
		self.processor.Activate(auto_deactivate=True)