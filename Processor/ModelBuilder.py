import nltk

from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

import json
import pickle
import random
import numpy as np

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD

from Falcon.Features.FileManager import WriteFile
from Falcon.Database import path

#/home/mahirhamiabrar/Chatbot/lib/python3.6/site-packages/Falcon/chat/database.json

class ModelBuilder():
	def __init__(self):
		self.words = []
		self.classes = []
		self.documents = []
		self.ignore_words = ['?', '!']
		
		self.data_file = open(path.main_database_path).read()
		self.reply_confidence = path.reply_conf_path
		self.intents = json.loads(self.data_file)

		self.train_x = None
		self.train_y = None
		self.model = None

	def PrepareWords(self):
		try:
			for intent in self.intents['intents']:
				for pattern in intent['patterns']:
					w = nltk.word_tokenize(pattern)
					self.words.extend(w)

					self.documents.append((w, intent['tag']))

					if intent['tag'] not in self.classes:
						self.classes.append(intent['tag'])

			self.words = [
			lemmatizer.lemmatize(w.lower()) for w in self.words if w not in self.ignore_words]
			self.words = sorted(list(self.words))

			self.classes = sorted(list(set(self.classes)))

			print(len(self.documents), "documents")
			print(len(self.classes), "classes", self.classes)
			print(len(self.words), "unique lemmatized words" , self.words)

			pickle.dump(self.words, open(path.main_train_words_path, 'wb'))
			pickle.dump(self.classes, open(path.main_train_classes_path, 'wb'))
		except Exception as e:
			print(f"[ERROR from {__name__}.PrepareWords()]: {e}")
	def Create_Train_Data(self):
		try:
			training = []
			output_empty = [0] * len(self.classes)

			for doc in self.documents:
				bag = []
				pattern_words = doc[0]
				pattern_words = [lemmatizer.lemmatize(word.lower()) for word in pattern_words]

				for w in self.words:
					bag.append(1) if w in pattern_words else bag.append(0)

				output_row = list(output_empty)
				output_row[self.classes.index(doc[1])] = 1

				training.append([bag, output_row])

			random.shuffle(training)
			training = np.array(training)

			self.train_x = list(training[:, 0])
			self.train_y = list(training[:, 1])

			print('\ntraining data created.\n')
		except Exception as e:
			print(f"[ERROR from {__name__}.Create_Train_Data()]: {e}")

	def Create_Model(self):
		try:
			self.model = Sequential()
			self.model.add(Dense(128, input_shape=(len(self.train_x[0]), ), activation='relu'))
			self.model.add(Dropout(0.5))
			self.model.add(Dense(64, activation='relu'))
			self.model.add(Dropout(0.5))
			self.model.add(Dense(len(self.train_y[0]), activation='softmax'))

			print('\nmodel created\n')
		except Exception as e:
			print(f"[ERROR from {__name__}.Create_Model()]: {e}")

	def Train_Model(self, epochs=1200, batch_size=5):
		try:
			sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
			self.model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

			hist = self.model.fit(np.array(self.train_x), np.array(self.train_y), epochs=epochs, 
				batch_size=batch_size, verbose=1)
			self.model.save(path.main_chat_model, hist)

			print("\nmodel training complete.\n")
		except Exception as e:
			print(f"[ERROR from {__name__}.Train_Model()]: {e}")

	def AutoBuildModel(self, train=True, epochs=2000, batch_size=5):
		try:
			self.PrepareWords()
			self.Create_Train_Data()
			self.Create_Model()
			if train:
				self.Train_Model(epochs=epochs, batch_size=batch_size)
		except Exception as e:
			print(f"[ERROR from {__name__}.AutoBuildModel()]: {e}")

def main():
	n = input('\n\nWant to modify Training? (Y/n): ')

	if str(n) in ['Y', 'y']:
		print('\nHow many epochs?')
		ep = int(input())

		print('How long batch size?')
		bs = int(input())

		print('Ok, epochs: {0} and batch size: {1}'.format(ep, bs))
	else:
		ep = 2000
		bs = 5

	
	model = ModelBuilder()
	model.AutoBuildModel(True, ep, bs)

	while True:
		n = input('\n\nWhat should be the minimum confidence for AI reply? : ')
		s = input('Are you sure to set it at {0}? (Y/n): '.format(n))

		if str(s) in ['Y', 'y', 'yes', 'Yes', 'YES']:
			WriteFile(model.reply_confidence, str(n), mode='w')
			print("All Done.")
			break
		else:
			continue

if __name__ == '__main__':
	main()