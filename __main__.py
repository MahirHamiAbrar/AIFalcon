import os
from threading import Thread as T
from Falcon2.Database import path, object_detection_path as od_path

if __name__ == '__main__':
	export_cmd = 'export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/slim'
	export_path = od_path.models_dir

	python_path = '~/Chatbot/bin/python'

	starter_file1 = path.main_dir + "/main/_starter1.py"
	starter_file2 = path.main_dir + "/main/_starter2.py"

	cd_cmd = f"cd {export_path} && {export_cmd} && cd {path.main_dir}/Processor/"

	cmd_1 = f"{cd_cmd} && {python_path} {starter_file1}"
	cmd_2 = f"{cd_cmd} && {python_path} {starter_file2}"

	T(target=os.system, args=(cmd_1, )).start()
	T(target=os.system, args=(cmd_2, )).start()
