import random

from threading import Thread

from Falcon2.IO._input_ import *
from Falcon2.IO._output_ import *

from Falcon2.main.Properties import *
from Falcon2.System.IO_Style import *

from Falcon2.Processor.PredictModel import *
from Falcon2.Networks.Socket_Client import Client

from Falcon2.Database import path
from Falcon2.Database.Dictionary import dictionary

class Processor():
	def __init__(self, input_title='You: ', output_title='AI: '):
		self.input_title = input_title
		self.output_title = output_title

		self.input = Input(self.input_title, details=True)
		self.output = Output(self.output_title, auto_launch=True)

		self.model = Predict()
		self.client = Client("Processor-MAIN", PORT=LOCAL_PORT)
		self.client.Start()

		self.task_id = 0
		self.hangup_id = None

		self.data = {}
		self.tagset = {}

		self.p_inputs = []    #processed inputs
		self.np_inputs = []   #not processed inputs

		self.dictionary = dictionary

		self.InitiateTags()
		self.ConfirmStartUp()

	def Activate(self, auto_deactivate=False):
		while True:
			try:
				if self.hangup_id is None:
					msg = self.input.GetInput()

					if auto_deactivate and str(msg).lower() == 'quit':
						self.Deactivate()
						break

					if msg is not None and msg != '':
						self.Process(msg)

			except Exception as e:
				print_error(e, __name__+".Activate()")

	def ConfirmStartUp(self):
		print_info("Processor has started.", __name__)

	def CreateDataset(self, task_id, usr_data, ai_data, dict_data):
		try:
			if str(usr_data) in self.dictionary.keys():
				builtin = True
			else:
				builtin = False

			dataType = self.Explore(dict_data['task'])

			self.data[task_id] = {  'user_data': str(usr_data),
									'ai_data': ai_data['data'],
									'prob': ai_data['prob'],
									'tag': ai_data['tag'],
									'input': dict_data['input'],
									'task': dict_data['task'],
									'class': dict_data['class'],
									'builtin': builtin,
									'type': dataType,
									'status': True,
									'final_response': None
								  }
		except Exception as e:
			print_error(e, __name__+".Activate()")

	def Deactivate(self):
		while True:
			if self.output.unprocessed == []:
				self.output.Deactivate()
				self.client.Send("true", 'quit')
				self.client.Stop()
				break

	def Explore(self, task):
		if callable(task):
			to_do = 'CALL'
		elif type(task) in [str, int, float]:
			to_do = 'STRING_DATA'
		elif type(task) == type(None):
			to_do = 'None_Type'
		else:
			to_do = None

		return to_do

	def ExecetuProcess(self, task_id):
		try:
			data = self.data[task_id]

			if data['status'] is True:
				if data['builtin'] is True:
					task_type = data['type']

					if task_type == 'CALL':
						try:
							cur_data = data['task'](data['user_data'])
						except TypeError:
							cur_data = data['task']()

						if cur_data is not None:
							output_data = str(cur_data)
						else:
							output_data = ' '

					elif task_type == 'None_Type':
						output_data = 'Done.'

					else:
						output_data = data['ai_data']

				else:
					response = data['ai_data']
					task = data['task']

					task_type = data['type']

					if task_type == 'CALL':

						try:
							cur_data = data['task'](data['user_data'])
						except TypeError:
							cur_data = data['task']()

						if cur_data is not None:
							output_data = str(cur_data)
						else:
							output_data = ' '

					elif task_type == 'None_Type':

						if response is None:
							output_data = 'Done.'
						else:
							output_data = ''

					else:
						output_data = task

					response += output_data
					output_data = response

				self.data[task_id]['status'] = False

				if float(self.data[task_id]['prob']) > 0.901:
					self.data[task_id]['final_response'] = output_data
					self.output.Return(output_data, task_id)
					with open(path.conf_data_path, 'a') as file:
						file.write("\n"+str([data['user_data'],
											data['tag'], data['prob']]))
				else:
					#output_data = random.choice(
					#dictionary['access_unknown_command'])

					output_data = self.GetEnsureTag(self.data[task_id]['tag'])

					self.data[task_id]['final_response'] = output_data
					self.output.Return(output_data, task_id)

					with open(path.less_conf_data_path, 'a') as file:
						file.write("\n"+str([data['user_data'],
											data['tag'], data['prob']]))

				self.hangup_id = None

		except Exception as e:
			print_error(e, __name__+".Activate()")

	def GetAIResponse(self, msg):
		res, prob = self.model.GetResponse(str(msg))
		tag = self.model.GetTag()

		return {'data': res, 'prob': prob, 'tag': tag}

	def GetDictionaryResponse(self, tag):
		try:
			res = self.dictionary[tag]

			Task, Class, InputR = res['task'], res['class'], res['require_input']

			return {'task': Task, 'class': Class, 'input': InputR}
		except Exception as e:
			print_error(e, __name__+".Activate()")

	def GetEnsureTag(self, tag):
		reply = self.model.intents['intents'][self.tagset[tag]]['ensure_tag']
		return random.choice(reply)

	def InitiateTags(self):
		database_intents = self.model.intents['intents']

		for pos, intents in enumerate(database_intents):
			self.tagset[intents['tag']] = pos

	def Process(self, msg):
		messages = self.ProcessInput(msg)

		for message in messages:
			ai_data = self.GetAIResponse(message)
			dict_data = self.GetDictionaryResponse(ai_data['tag'])

			Thread(target=self.CreateDataset, args=(self.task_id,
				message, ai_data, dict_data)).start()

			self.np_inputs.append(self.task_id)

			if dict_data['input'] is True:
				self.hangup_id = self.task_id

			#self.StartProcess()
			Thread(target=self.StartProcess).start()

			self.task_id += 1

	def ProcessInput(self, input_data):
		input_data = str(input_data) + ' and'
		input_data = input_data.split(' and')

		del(input_data[len(input_data)-1])
		return input_data

	def StartProcess(self):
		try:
			if self.data != {}:

				for u_id in self.np_inputs:
					Thread(target=self.ExecetuProcess, args=(u_id, )).start()
					self.p_inputs.append(u_id)

				for p_id in self.p_inputs:
					if p_id in self.np_inputs:
						del(self.np_inputs[self.np_inputs.index(p_id)])
		except Exception as e:
			print_error(e, __name__+".Activate()")

if __name__ == '__main__':
	processor = Processor()
	processor.Activate(auto_deactivate=True)
