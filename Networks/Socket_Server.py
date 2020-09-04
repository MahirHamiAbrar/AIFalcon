import sys
import socket
import select
from threading import Thread

from Falcon2.System.IO_Style import *

class Server():
	def __init__(self, IP, PORT, auto_quit=False, show=False):
		self.HEADER_LENGTH = 10

		self.show = show
		self.auto_quit = auto_quit

		if IP is not None:
			self.IP = str(IP)
		else:
			self.IP = '127.0.0.1'
		print_warning('Setteled IP Address to: {}'.format(self.IP), __name__)

		if PORT is not None:
			self.PORT = int(PORT)
		else:
			self.PORT = 9797
		print_warning('Setteled PORT to: {}'.format(self.PORT), __name__)

		self.clients = {}
		self.running = True

		self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.server_socket.bind((self.IP, self.PORT))
		self.server_socket.listen()

		self.sockets_list = [self.server_socket]

	def Stop(self):
		self.running = False

	def receive_message(self, client_socket):
		try:
			message_header = client_socket.recv(self.HEADER_LENGTH)

			if not len(message_header):
			    return False

			message_length = int(message_header.decode('utf-8').strip())

			return {'header': message_header, 'data': client_socket.recv(message_length)}

		except:
			return False

	def SendMessage(self, msg):
		print(f'\n {msg}')

	def HandleServer(self):
		while self.running:
			read_sockets, _, exception_sockets = select.select(self.sockets_list, [], self.sockets_list)

			for notified_socket in read_sockets:

				if notified_socket == self.server_socket:
					client_socket, client_address = self.server_socket.accept()
					user = self.receive_message(client_socket)

					if user is False:
						continue

					self.sockets_list.append(client_socket)
					self.clients[client_socket] = user

					#self.SendMessage('Accepted new connection from {}:{}, username: {}'.format(*client_address, user['data'].decode('utf-8')))
					active = user['data'].decode('utf-8')
				else:
					message = self.receive_message(notified_socket)

					if message is False:
						inactive = self.clients[notified_socket]['data'].decode('utf-8')

						self.sockets_list.remove(notified_socket)

						del self.clients[notified_socket]
						continue

					user = self.clients[notified_socket]

					if self.auto_quit:
						if user['data'] == 'Processor-MAIN':
							msg = message["data"].decode("utf-8")
							msg = eval(msg)

							if msg['id'] == 'quit' and msg['data'] == 'true':
								self.running = False

					if self.show:
						self.SendMessage(f'{user["data"].decode("utf-8")}>> {message["data"].decode("utf-8")}')

					for client_socket in self.clients:

						if client_socket != notified_socket:
							client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])

			for notified_socket in exception_sockets:
				self.sockets_list.remove(notified_socket)
				del self.clients[notified_socket]

	def Start(self):
		Thread(target=self.HandleServer).satrt()

if __name__ == '__main__':
	s = Server(None, 10496)
	s.Start()
