import speech_recognition as sr

from threading import Thread
from Falcon2.System.IO_Style import *


class STT():
	def __init__(self, title, details=False, show=True):
		self.data = ''
		self.running = True

		self.title = title

		self.r = sr.Recognizer()
		self.m = sr.Microphone()

		self.initialize(details=details)

	def SetTitle(self, title):
		self.title = title

	def DeActivate(self):
		self.running = False

	def GetVoiceInput(self, show=False):
		data = str(self.data)
		self.data = ''
		return data

	def initialize(self, details=False):
		self.show_details('initializing output system, please wait...', 
		proceed=details)
		
		with self.m as source: self.r.adjust_for_ambient_noise(source)

		self.show_details(f'Setteled minimum energy threshold: {self.r.energy_threshold}'
			, proceed=details)
		#os.system('clear')

	def _recognize(self, details=False, show=True):
		value = None
		cprint(f"{self.title}\r", ('i', 'b'), color='green', end='\r')
		
		with self.m as source: audio = self.r.listen(source)
		
		print(colors.CLEAR, end='\r')
		cprint('processing...', ('bl', 'b'), color='yellow', end='\r')

		try:
			value = self.r.recognize_google(audio)
			print(colors.CLEAR, end='\r')
			cprint(f"{self.title}{value}\n", ('l'), color='green')
		except sr.UnknownValueError as e:
			print(colors.CLEAR, end='\r')
			cprint(f"Oops, didn't catch that! -> {e}\n", ('l'), color='gray')
			#return e
		except sr.RequestError as e:
			print(colors.CLEAR, end='\r')
			cprint(f"[Unable to receive return value from Google]: {e}\n", ('l'), 
				color='red')
			#return e
		finally:
			if value is not None:
				returnValue = value
				value = ''
				return returnValue

	def show_details(self, value='', proceed=False):
		if proceed:
			cprint(value, ('l', 'i'), color='purple')

if __name__ == '__main__':
	cprint('initializing, please wait...', ('bl', 'b', ), color='yellow')
	cprint('say [quit] or press [Ctrl+Alt+C] to quit...', ('b', 'i', ), color='blue')
	
	stt = STT(title='You> ', details=True)
	
	while True:
		value = stt.GetVoiceInput(show=True)

		if value.lower() == 'quit':
			stt.DeActivate()