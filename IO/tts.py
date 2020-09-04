import pyttsx3 as _tts

from Falcon2.IO.ttt import *
from Falcon2.System.IO_Style import *

class TTS():
	def __init__(self, title, auto_init=True, speechRate=140):
		self.title = title
		self.speechRate = speechRate
		
		self.ttt = TTT(title=self.title)

		if auto_init:
			self.Initialize(self.speechRate)

	def SetTitle(self, title):
		self.title = title

	def Initialize(self, speechRate=140):
		self.engine = _tts.init()
		self.engine.setProperty('rate', speechRate)

	def Speak(self, data, show=True):
		try:
			if show:
				self.ttt.Show_Output(data, show_title=True)

			self.engine.say(data)
			self.engine.runAndWait()
		except Exception as e:
			print_error(e, str(__name__)+".Speak()")

if __name__ == '__main__':
	tts = TTS(title='[SPEAKER]: ', auto_init=False)
	tts.Initialize(speechRate=150)

	tts.Speak('Hello, from TTS engine!')
