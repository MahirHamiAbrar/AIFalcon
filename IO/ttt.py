from Falcon2.System.IO_Style import *

class TTT():
	def __init__(self, title):
		self.title = title

	def SetTitle(self, title):
		self.title = title

	def GetTextInput(self, show=False):
		data = input(cprint(f"{self.title}", ('i', 'b'), color="green", 
			_return=True) + colors.ITALIC + colors.BOLD)

		if data != '' and data != None:
			if show:
				self.Show_Output(data, True)
			return data
		return ''

	def Show_Output(self, data, show_title=False, start='\n'):
		if show_title:
			cprint(f"{self.title}{data}", ('b', 'i', 'clear'), color='cyan', start=start)
		else:
			cprint(f"{data}", ('b', 'i', 'clear'), color='cyan', start=start)


if __name__ == "__main__":
	ttt = TTT('You: ')

	text = ttt.GetTextInput(show=False)

	if text:
		ttt.Show_Output(text, True)
	else:
		text = 'nothing'
		ttt.Show_Output(text, True)