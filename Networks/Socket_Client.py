import sys
import socket
import errno

from threading import Thread as T
from Falcon2.System.IO_Style import *

class Client():
	def __init__(self, name, IP=None, PORT=None):
		self.running = True

		self.HEADER_LENGTH = 10

		if IP is not None:
			self.IP = str(IP)
			print_warning('The IP Address of server and client must be same. Or else you won\'t receive any message.', __name__)
		else:
			self.IP = '127.0.0.1'

		if PORT is not None:
			self.PORT = int(PORT)
			print_warning('The PORT number of the Server and client must be the same. Or else you won\'t receive any message.', __name__)
		else:
			self.PORT = 9797

		self.client_name = name
		MESSAGE = None

		self.received_msg = {}

	def Connect(self):
		try:
			self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

			self.client_socket.connect((self.IP, self.PORT))

			self.client_socket.setblocking(False)

			self.username = self.client_name.encode('utf-8')
			self.username_header = f"{len(self.username):<{self.HEADER_LENGTH}}".encode('utf-8')
			self.client_socket.send(self.username_header + self.username)
		except Exception as e:
			print_error(e, __name__+".Connect()")

	def GetMessage(self):
		while self.running:
			try:
				self.username_header = self.client_socket.recv(self.HEADER_LENGTH)

				if not len(self.username_header):
				    print('Connection closed by the server')
				    sys.exit()

				username_length = int(self.username_header.decode('utf-8').strip())

				self.username = self.client_socket.recv(username_length).decode('utf-8')

				message_header = self.client_socket.recv(self.HEADER_LENGTH)
				message_length = int(message_header.decode('utf-8').strip())
				MESSAGE = self.client_socket.recv(message_length).decode('utf-8')

				#print(f'{self.username} > {MESSAGE}')
				self.received_msg[self.username] = MESSAGE

				MESSAGE = None

			except IOError as e:
				if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
				    #print('Reading error: {}'.format(str(e)))
				    print_error(e, __name__ + ".GetMessage()")
				    sys.exit()

			except Exception as e:
				#print('Reading error: '.format(str(e)))
				print_error(e, __name__ + ".GetMessage()")
				sys.exit()

	def Send(self, MESSAGE, ID):
		try:
			#MESSAGE = str(input('text: '))

			if MESSAGE:
				MESSAGE = {'data': MESSAGE, 'id': ID}
				MESSAGE = str(MESSAGE).encode('utf-8')
				#message_header = ''.encode('utf-8')
				message_header = f"{len(MESSAGE):<{self.HEADER_LENGTH}}".encode('utf-8')
				self.client_socket.send(message_header + MESSAGE)
				print(f"\n\nSENT: {message_header + MESSAGE}")

		except Exception as e:
			print_error(e, __name__ + ".Send()")

	def Receive(self, id):
		while self.running:
			try:
				if id in self.received_msg.keys():
					data = self.received_msg[id]
					del(self.received_msg[id])
					return eval(data)
			except Exception as e:
				print_error(e, __name__+".Receive()")

	def Start(self):
		self.Connect()
		T(target=self.GetMessage).start()
		#T(target=self.Work).start()

	def Stop(self):
		self.running = False

if __name__ == '__main__':
	c = Client(__name__, PORT=10496)
	c.Start()

	for i in range(3):
		c.Send(input(' $ '), i)

	print(c.Receive('__main__')['data'])
	c.Stop()