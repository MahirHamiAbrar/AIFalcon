from Falcon2.IO.ttt import *
from Falcon2.IO.iSettings import *
from Falcon2.System.IO_Style import *

class SelectMode():
	def __init__(self):
		self.ttt = TTT(None)
		self.settings = iSettings()

		self.select_modes = {'1': self.settings.ChangeToText, 
						'2': self.settings.ChangeToVoice}
		self.modes = {'1': self.settings.text_mode, '2': self.settings.voice_mode}

	def Select(self):
		attempts = 3

		cprint('==='*26, ('b', 'i', ), color='blue', start='\n\n')
		cprint('|'+' '*32+'Mode Selector'+' '*32+'|', ('b', 'i', 's'), 
			color='blue')
		cprint('==='*26, ('b', 'i', ), color='blue')

		while True:
			if attempts <= 0:
				print_warning('seems like you had problems to select mode..So I selected the "Text Mode" by my self.You can change the mode from AI Settings later.', __name__+".Select()")
				self.select_modes['1']()
				return self.modes['1']

			cprint('   1 >> Text Input\n   2 >> Voice Input', color='yellow', start="\n\n")

			mode = str(input(cprint('enter the number to select mode: ', 
				('i', 'l', ), color='green', _return=True)))

			if mode not in ['1', '2']:
				print_error("select the shown number to select the mode.", __name__+'.Select()')
				attempts -= 1
				continue

			cprint('=DONE='*13, ('b', 'i', ), color='blue', start='\n', end='\n\n')

			self.select_modes[mode]()
			return self.modes[mode]

	def GetMode(self):
		return self.Select()

if __name__ == '__main__':
	mode = SelectMode()
	cur_mode = mode.GetMode()

	print(cur_mode)