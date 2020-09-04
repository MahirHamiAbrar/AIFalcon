import os
from pathlib import Path

#get this file's parent dir
this_dir = os.path.abspath('__init__.py')
#get the path of "Falcon" file
main_dir = str(Path(this_dir).parent.parent)

class path:
	#get this file's parent dir
	this_dir = os.path.abspath('__init__.py')
	#get the path of "Falcon" file
	main_dir = str(Path(this_dir).parent.parent)
	#`Database` directory and inside files
	dir_database = main_dir + '/Database/'

	#........
	#`basement` directory and inside files
	basement_dir = dir_database + 'basement/'
	#...
	main_database_path = basement_dir + 'main_database.json'

	#`conversation` directory and inside files
	conversation_dir = dir_database + 'conversation/'
	#...
	conf_data_path = conversation_dir + "/Confident_Commands.txt"
	less_conf_data_path = conversation_dir + "/Less_Confident_Commands.txt"
	reply_conf_path = conversation_dir + "/reply_confidence.ai"

	#`train_data` directory and inside files
	train_data_dir = dir_database + 'train_data'
	#...
	main_train_classes_path = train_data_dir + "/classes.pkl"
	main_train_words_path = train_data_dir + "/words.pkl"

	#`UART_Protocol` directory and inside files
	uart_protocol_dir = dir_database + 'UART_Protocol'
	#...
	uart_database_path = uart_protocol_dir + "/UART_Database.json"

	#settings directory
	dir_settings = main_dir + "/Settings/"

	io_settings_path = dir_settings + "IOSettings.json"

class object_detection_path:
	this_dir = main_dir + '/Object_Detection'

	ckpt_dir = this_dir + '/ckpt-models'
	ssd_mobile_net_path = ckpt_dir + '/ssd_mobilenet_v1_coco_2018_01_28/'

	api_dir = this_dir + '/api'
	models_dir = api_dir + '/models/research/'

	

if __name__ == '__main__':
	print(object_detection_path.ssd_mobile_net_path)