from Falcon2.IO.ttt import *
from Falcon2.IO.stt import *
from Falcon2.IO.iSettings import *
from Falcon2.System.IO_Style import *
from Falcon2.IO.mode_selection import *

class Input():
	def __init__(self, title, details=False, show=True):
		self.show = show
		self.title = title
		
		self.ttt = TTT(self.title)
		self.stt = STT(self.title, details=details, show=show)
		self.smode = SelectMode()

		self.settings = iSettings()
		self.settings.RestoreDefault()

		self.std_mode = self.settings.GetMode('std')
		self.cur_mode = self.settings.GetMode('cur')

		self.ConfirmStartUp()

	def ConfirmStartUp(self):
		print_info("Input System has started.", __name__)

	def SetTitle(self, title):
		self.title = str(title)
		self.ttt.SetTitle(title)
		self.stt.SetTitle(title)

	def Update(self):
		self.std_mode = self.settings.GetMode('std')
		self.cur_mode = self.settings.GetMode('cur')

	def GetInput(self):
		while True:
			self.Update()

			if self.cur_mode == self.settings.voice_mode:
				data = self.stt.GetVoiceInput(show=self.show)
			elif self.cur_mode == self.settings.text_mode:
				data = self.ttt.GetTextInput(show=self.show)
			elif self.cur_mode == self.settings.ask_mode:
				self.AskForMode()
				continue

			return data

	def AskForMode(self):
		self.cur_mode = self.smode.GetMode()
		self.Update()

if __name__ == '__main__':
	i = Input('You: ', details=True)
	
	while True:
		data = i.GetInput()

		if data.lower() == 'quit':
			break
