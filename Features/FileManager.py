#read files
def ReadFile(file_name, mode='r'):
	if mode not in ['r', 'rb', 'r+']:
		raise KeyError(f"Selected mode '{mode}' was not valid for this function.")
	with open(str(file_name), mode) as file:
		return file.read()

#write in files
def WriteFile(file_name, file_data, mode='w'):
	if mode not in ['w', 'wb', 'w+', 'a', 'ab']:
		raise KeyError(f"Selected mode '{mode}' was not valid for this function.")
	with open(str(file_name), mode) as file:
		file.write(str(file_data))

#copy the inside data from one file to another
def CopyFile(file_from, file_to, write_mode='w', read_mode='r'):
	if write_mode not in ['a', 'w', 'w+', 'wb', 'ab']:
		raise KeyError(f"Selected write_mode-> '{mode}' was not valid for this function.")

	if read_mode not in ['r', 'rb', 'r+']:
		raise KeyError(f"Selected read_mode-> '{mode}' was not valid for this function.")
	
	with open(file_from, read_mode) as file_f:
		with open(file_to, write_mode) as file_t:
			file_t.write(file_f.read())

if __name__ == '__main__':
	pass