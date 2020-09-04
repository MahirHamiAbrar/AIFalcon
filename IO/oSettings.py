import json

from Falcon2.System.IO_Style import *
from Falcon2.Settings.IOSettings import *

class oSettings():
	def __init__(self):
		self.settings = IOSettings()

		self.text_mode = 'TEXT'
		self.voice_mode = 'VOICE'

		self.modes = {'cur': self.settings.cur_output, 
					'std': self.settings.std_output}

		self.output_modes = {'t': self.text_mode, 'v': self.voice_mode}

		self.cur_mode = self.GetMode('cur')
		self.std_mode = self.GetMode('std')

	def GetMode(self, mode='cur'):
		try:		
			settings = self.settings.Load(self.settings.output_settings)

			return settings[self.modes[mode]]
		except Exception as e:
			print_error(e, __name__+"GetMode()")

	def UpdateModes(self):
		self.cur_mode = self.GetMode('cur')
		self.std_mode = self.GetMode('std')

	def ChangeToText(self):
		self.ChangeMode('cur', 't', 4)

	def ChangeToVoice(self):
		self.ChangeMode('cur', 'v', 4)

	def ChangeMode(self, type, mode, indent=4):
		try:
			types = {'cur': self.settings.cur_output, 
						'std': self.settings.std_output}
			
			self.settings.Return(self.settings.output_settings, self.modes[mode],
				self.output_modes[type], indent=4)
		except Exception as e:
			print_error(e, __name__+"ChangeInput()")

	def RestoreDefault(self):
		self.settings.Return(self.settings.output_settings, self.modes['cur'], 
			self.GetMode('std'), indent=4)

if __name__ == '__main__':
	settings = oSettings()
	settings.ChangeToVoice()