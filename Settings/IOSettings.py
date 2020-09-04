import json

from Falcon2.Database import path
from Falcon2.System.IO_Style import *
from Falcon2.Features.FileManager import *

class IOSettings():
	def __init__(self):
		self.settings_path = path.io_settings_path

		self.input_settings = 'input-settings'
		self.output_settings = 'output-settings'

		self.std_output = 'std-output'
		self.cur_output = 'cur-output'

		self.std_input = 'std-input'
		self.cur_input = 'cur-input'

		self.default_settings = {"input-settings": {
							        "std-input": "TEXT",
							        "cur-input": "TEXT"
							    },
							    "output-settings": {
							        "std-output": "VOICE",
							        "cur-output": "VOICE"
							    }
							}

	def Load(self, setting, ALL=False):
		while True:
			try:
				settings = ReadFile(self.settings_path)
				settings = json.loads(settings)

				if ALL:
					return settings
				
				return settings[setting]
			
			except json.JSONDecodeError as e:
				print_error(e, __name__+"Load()")
				continue

	def Return(self, setting, type, mode, indent=4):
		work_done = False

		while True:
			try:
				settings = ReadFile(self.settings_path)
				settings = json.loads(settings)

				selected_settings = settings[setting]
				selected_settings[type] = mode

				settings[setting] = selected_settings

				with open(self.settings_path, 'w') as file:
					json.dump(settings, file, indent=indent)

				work_done = True

			except json.JSONDecodeError as e:
				print_error(e, __name__+"Return()")
				continue

			if work_done:
				break

	def RestoreDefault(self):
		work_done = False
		
		while True:
			try:
				with open(self.settings_path, 'w') as file:
					json.dump(self.default_settings, file, indent=4)

				work_done = True

			except json.JSONDecodeError as e:
				print_error(e, __name__+"RestoreDefault()")
				continue

			if work_done:
				break

if __name__ == '__main__':
	settings = IOSettings()
	#settings.Return('output-settings', 'cur-output', 'TEXT', 5)
	#print(settings.Load('input-settings'))
	settings.RestoreDefault()