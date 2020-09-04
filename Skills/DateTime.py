import datetime
import calendar
import random

MONTHS={1: 'January', 2: 'Feburary', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
		7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 
		12: 'December'}

class DateTime():
	def __init__(self):
		self.now = datetime.datetime.now()
		self.hr = self.hour()
		self.min = self.minute()
		self.sec = self.second()

		self.time = ''
		self.date = ''

	def hour(self):
		return str(self.now.hour)

	def minute(self):
		return str(self.now.minute)

	def second(self):
		return str(self.now.second)

	def Time(self):
		self.time = datetime.datetime.time(self.now)
		return self.time

	def Date(self):
		self.date = datetime.datetime.date(self.now)
		return self.date

	def GetAny(self, get='year'):
		d = {'year':0, 'month':1, 'month_day':2, 'hour':3, 'minute':4, 'second':5,
			 'week_day':6, 'year_day':7, 'is_dst':8}
		return datetime.datetime.timetuple(self.now)[d[get]]

	def GetDate(self):
		self.Date()
		date = str(self.date).split('-')
		
		year = date[0]
		month = MONTHS[int(date[1])]
		day = int(date[2])

		ans = [f"{month} {day} {year}", f"{month} {day}th {year}", 
				f"{day} {month} {year}", f"{day}th {month} {year}"]
		return random.choice(ans)

	def GetTime24(self):
		h = self.now.hour
		m = self.now.minute
		return str(h) + ' ' + str(m)

	def GetTime12(self):
		h = self.now.hour - 12
		m = self.now.minute
		return str(h) + ' ' + str(m)

if __name__ == '__main__':
	from Falcon2.IO.tts import *

	tts = TTS(None)
	d = DateTime()

	date = d.GetDate()
	tts.Speak(date)
