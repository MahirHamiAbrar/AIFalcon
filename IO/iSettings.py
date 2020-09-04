import json

from Falcon2.System.IO_Style import *
from Falcon2.Settings.IOSettings import *

class iSettings():
	def __init__(self):
		self.settings = IOSettings()

		self.ask_mode = 'ASK'
		self.text_mode = 'TEXT'
		self.voice_mode = 'VOICE'

		self.modes = {'t': self.text_mode, 'v': self.voice_mode, 
						'a': self.ask_mode}
		self.types = {'cur': self.settings.cur_input, 
						'std': self.settings.std_input}

		self.cur_mode = self.GetMode('cur')
		self.std_mode = self.GetMode('std')

	def GetMode(self, mode='cur'):
		try:
			settings = self.settings.Load(self.settings.input_settings)

			return settings[self.types[mode]]
		except Exception as e:
			print_error(e, __name__+".GetMode()")

	def UpdateModes(self):
		self.cur_mode = self.GetMode('cur')
		self.std_mode = self.GetMode('std')

	def ChangeToText(self):
		self.ChangeMode('cur', 't', 4)

	def ChangeToVoice(self):
		self.ChangeMode('cur', 'v', 4)

	def ChangeToAsk(self):
		self.ChangeMode('cur', 'a', 4)

	def ChangeMode(self, type, mode, indent=4):
		try:
			self.settings.Return(self.settings.input_settings, self.types[type], 
				self.modes[mode], indent=4)
		except Exception as e:
			print_error(e, __name__+".ChangeInput()")

	def RestoreDefault(self):
		self.settings.Return(self.settings.input_settings, self.types['cur'], 
			self.GetMode('std'), indent=4)

if __name__ == '__main__':
	settings = iSettings()
	settings.RestoreDefault()

	#print(settings.modes)