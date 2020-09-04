import os
from threading import Thread

from Falcon2.System.IO_Style import *
from Falcon2.main.Properties import *
from Falcon2.Networks.Socket_Server import Server
from Falcon2.Processor.MainProcessor import Processor
from Falcon2.Object_Detection.ObjectFinder import main as ObjectDetector

def Start():
	server = Server(LOCAL_IP, LOCAL_PORT, auto_quit=True)
	Thread(target=server.HandleServer).start()
	print_info(f"Falcon server has started successfully at http://{server.IP}:{server.PORT}", __name__)

	Thread(target=ObjectDetector).start()
	print_info(f"Falcon Object Detection System has started successfully.", __name__)

def main():
	print_warning("write [quit] to quit", __name__)
	processor = Processor()
	processor.Activate(auto_deactivate=True)
