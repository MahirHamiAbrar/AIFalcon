from Falcon2.IO.ttt import *
from Falcon2.IO._input_ import *
from Falcon2.System.IO_Style import *

class File():
	def __init__(self):
		self.fileName = ''
		self.fileLocation = ''
		self.writeData = ''

		self.input = Input('FILE CREATOR: ', show=False)
		self.ttt = TTT(None)
	
	def Create(self):
		self.ttt.Show_Output('What is the file name?\n')
		self.fileName = self.input.GetInput()
		self.ttt.Show_Output('file location? \n')
		self.fileLocation = self.input.GetInput()
		self.ttt.Show_Output('what do you want to write? \n')
		self.writeData = self.input.GetInput()

		if self.fileName.startswith('/') or self.fileLocation.endswith('/'):
			path = self.fileLocation + self.fileName
		else:
			path = self.fileLocation + '/' + self.fileName

		try:
			with open(path, 'w') as file:
				file.write(str(self.writeData))
			print_success('Creating {} was successful!'.format(self.fileName), 
				__name__)
		except Exception as e:
			print_error(e, __name__+'.Create()')


if __name__ == '__main__':
	file = File()
	file.Create()