from Falcon2.IO.tts import *
from Falcon2.IO.ttt import *
from Falcon2.IO.oSettings import *
from Falcon2.System.IO_Style import *

from threading import Thread

class Output():
	def __init__(self, title, auto_launch=True):
		self.title = title

		self.running = True

		self.data = {}
		self.processed = []
		self.unprocessed = []

		self.tts = TTS(self.title)
		self.ttt = TTT(self.title)
		self.settings = oSettings()

		self.settings.RestoreDefault()

		self.std_mode = self.settings.GetMode('std')
		self.cur_mode = self.settings.GetMode('cur')

		if auto_launch:
			Thread(target=self.Process).start()
			print_info("Auto Launched output process --> CHECK", __name__)
		else:
			print_info("Output Process should start manually.", __name__)

		self.ConfirmStartUp()

	def ConfirmStartUp(self):
		print_info("Output system has started.", __name__)

	def SetTitle(self, title):
		self.title = str(title)
		self.ttt.SetTitle(title)
		self.tts.SetTitle(title)

	def Return(self, value, id):
		self.data[id] = value
		self.unprocessed.append(id)

	def Deactivate(self):
		self.running = False

	def Update(self):
		self.std_mode = self.settings.GetMode('std')
		self.cur_mode = self.settings.GetMode('cur')

	def Process(self):
		while self.running:
			for _id in self.unprocessed:
				self.ReturnOutput(self.data[_id])
				self.processed.append(_id)

			for _id2 in self.processed:
				if _id2 in self.unprocessed:
					index = self.unprocessed.index(_id2)
					del(self.unprocessed[index])

	def ReturnOutput(self, value):
		self.Update()

		if self.cur_mode == self.settings.text_mode:
			self.ttt.Show_Output(value, show_title=True)
		
		elif self.cur_mode == self.settings.voice_mode:
			self.tts.Speak(value, show=True)
		
		else:
			print_error('Invalid Output operation found! {}'.format(self.cur_mode), __name__+".ReleaseOutput()")
			self.settings.RestoreDefault()

if __name__ == '__main__':
	out = Output('AI: ')

	id = 1

	while True:
		n = str(input('You: '))
		out.Return(n, id)

		if n.lower() == 'quit':
			out.Deactivate()
			break

		id += 1