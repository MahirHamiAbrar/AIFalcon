import os

class colors:
	GRAY = '\033[90m'
	RED = "\033[91m"
	GREEN = "\033[92m"
	YELLOW = "\033[93m"
	BLUE = "\033[94m"
	PURPLE = "\033[95m"
	CYAN = "\033[96m"
	DEFAULT = "\033[0m"
	CLEAR = '\033[K'

	BOLD = '\033[1m'
	LIGHT = '\033[2m'
	ITALIC = '\033[3m'
	UNDERLINE = '\033[4m'
	BLINK = '\033[5m'
	WHAT = '\033[6m'
	SELECT = '\033[7m'
	INVISIBLE = '\033[8m'
	DELETE = '\033[9m'

_styles_ = {
		#colors
		'default': colors.DEFAULT, 'gray': colors.GRAY, 'red': colors.RED,
		'green': colors.GREEN, 'yellow': colors.YELLOW, 'blue': colors.BLUE,
		'purple': colors.PURPLE, 'cyan': colors.CYAN, 'clear': colors.CLEAR,

		#font styles
		'b': colors.BOLD, 'l': colors.LIGHT, 'i': colors.ITALIC,
		'u': colors.UNDERLINE, 'bl': colors.BLINK, 'w': colors.WHAT,
		's': colors.SELECT, 'iv': colors.INVISIBLE, 'd': colors.DELETE
		}

#clear the console
def clear_console():
	os.system('clear')

def remove_dots(text):
	return text
	#return text.replace('.', '/')

#print errors only
def print_error(error, name, start='\n', end='\n'):
	print(f"\n{colors.BOLD}{colors.RED}[ERROR FROM {remove_dots(name)}]: {error}.{colors.DEFAULT}\n")

#print warnings only
def print_warning(message, name, start='\n', end='\n'):
	print(f"\n{colors.BOLD}{colors.YELLOW}[WARNING FROM {remove_dots(name)}]: {message}.{colors.DEFAULT}\n")

def print_success(message, name):
	print(f"\n{_styles_['b']}{_styles_['green']}[SUCCESS FROM {remove_dots(name)}]: {message}{_styles_['default']}\n")

def print_info(info, name):
	print(f"\n{_styles_['i']}{_styles_['b']}{_styles_['purple']}[INFO FROM {remove_dots(name)}]: {info}{_styles_['default']}\n")

#customize print
def cprint(msg, *style, color='default', start='\r', end='\n',
	clear_all=False, _return=False):
	styles = f"{start}{_styles_[color]}"

	if style != ():
		for s in style:
			for _s in s:
				styles += f'{_styles_[_s]}'

	if clear_all:
		clear_console()

	styles += f"{msg}{_styles_['default']}"

	if _return:
		return styles

	print(styles, end=end)


if __name__ == '__main__':
	cprint('THIS IS A STYLISH TEXT!', ('l', 'i', 'u', 'bl'),
		color='purple', clear_all=True)
"""
import time as t
	print(colors.CYAN + "WAIT FOR THE COLORFUL TEXT!!!", end='\r')
	t.sleep(3)
	print(colors.CLEAR, end='\r')
	print(colors.GRAY+"HER" + colors.RED + "E IS" + colors.YELLOW +
		" YOU" + colors.BLUE + "R CO" + colors.PURPLE + "LOR" + colors.GREEN + "FUL"
		+ colors.CYAN + " TEX" + colors.DEFAULT + "T!!!")
	print_error("rbdjnzjn", __name__)
"""
