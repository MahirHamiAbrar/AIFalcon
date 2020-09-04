from Falcon2.Processor.ModelBuilder import *
from Falcon2.System.IO_Style import *
from Falcon2.Database import path
from tensorflow.keras.models import load_model

import random
import pickle
import json

import numpy as np

#print(path.this_dir)

class Predict():
	def __init__(self):
		self.a = ModelBuilder()
		self.a.AutoBuildModel(False)

		self.model = load_model('/home/mahirhamiabrar/Chatbot/lib/python3.6/site-packages/Falcon/Models//chatbot_model.h5')

		self.intents = json.loads(open(path.main_database_path).read())
		self.words = pickle.load(open(path.main_train_words_path, 'rb'))
		self.classes = pickle.load(open(path.main_train_classes_path, 'rb'))

		self.tag = ''

	def clean_up_sentence(self, sentence):
		try:
			sentence_words = nltk.word_tokenize(sentence)
			sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
			return sentence_words
		except Exception as e:
			print_error(e, str(__name__)+".clean_up_sentence()")

	def bow(self, sentence, words, show_details=True):
		try:
			sentence_words = self.clean_up_sentence(sentence)

			bag = [0] * len(words)

			for s in sentence_words:
				for i, w in enumerate(words):
					if w == s:
						bag[i] = 1
						if show_details:
							print('\nfound in bag: %s' % w)
			return (np.array(bag))
		except Exception as e:
			print_error(e, str(__name__)+".bow()")

	def predict_class(self, sentence, model):
		try:
			p = self.bow(sentence, self.words, show_details=False)
			res = self.model.predict(np.array([p]))[0]

			ERROR_THRESHOLD = 0.25

			results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

			results.sort(key=lambda x: x[1], reverse=True)
			return_list = []

			for r in results:
				return_list.append({"intent": self.classes[r[0]], 'probability': str(r[1])})
			return return_list
		except Exception as e:
			print_error(e, str(__name__)+".predict_class()")

	def getResponse(self, ints, database_json):
		try:
			#print(f"[FROM] {__name__} : ints:", ints)
			tag = ints[0]['intent']
			list_of_intents = database_json['intents']

			for i in list_of_intents:
				if i['tag'] == tag:
					result = random.choice(i['responses'])
					self.tag = i['tag']
					break
			return result
		except Exception as e:
			print_error(e, str(__name__)+".getResponse()")

	def GetResponse(self, msg):  #to get AI response
		try:
			ints = self.predict_class(msg, self.model)
			res = self.getResponse(ints, self.intents)
			#print('INTS:', ints, '\nRES:', res)
			return res, ints[0]['probability']
		except Exception as e:
			print_error(e, str(__name__)+".GetResponse()")

	def GetTag(self):
		try:
			return self.tag
		except Exception as e:
			print_error(e, str(__name__)+".GetTag()")

if __name__ == '__main__':
	question = "how are you?"
	f = Predict()
	r = f.GetResponse(question)
	print("\n\nQuestion:", question, "\n   AI:", r)