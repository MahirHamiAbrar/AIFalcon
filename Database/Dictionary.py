from Falcon2.Skills.DateTime import *
from Falcon2.Skills.CreateFile import *

DT = DateTime()
CRF = File()




dictionary = {
	#these key words have their own responses in AI Database so,
	#no other responses are necessary for now
	"starting" : {'task': " ", 'class': None, 'require_input': False},
	"what's_up" : {'task': " ", 'class': None, 'require_input': False},
	"ask_how_are_you_1" : {'task': " ", 'class': None, 'require_input': False},
	"ask_how_are_you_2" : {'task': " ", 'class': None, 'require_input': False},
	"ask_name" : {'task': " ", 'class': None, 'require_input': False},
	"age_of_ai" : {'task': " ", 'class': None, 'require_input': False},
	"ai_is_cool" : {'task': " ", 'class': None, 'require_input': False},
	"are_you_mad" : {'task': " ", 'class': None, 'require_input': False},
	"clever_ai" : {'task': " ", 'class': None, 'require_input': False},
	"goodbye" : {'task': " ", 'class': None, 'require_input': False},
	"where_ai_lives" : {'task': " ", 'class': None, 'require_input': False},
	"NO_TAG" : {'task': "Sir, please try to be more specific", 'class': None, 'require_input': False},

	#date-time
	"usual_time" : {'task': DT.GetTime12, 'class':DT, 'require_input': False},
	"the_date" : {'task': DT.GetDate, 'class':DT, 'require_input': False},

	#input system
	"enable text input": {'task':"-", 'class':"-", 'require_input': False},
	"enable voice input": {'task':"-", 'class':"-", 'require_input': False},
	"show input options": {'task':"-", 'class':"-", 'require_input': False},

	#output system
	"enable text output": {'task':"-", 'class': "-", 'require_input': False},
	"enable voice output": {'task':"-", 'class': "-", 'require_input': False},

	#AI self training
	"train yourself": {'task': "-", 'class': "-", 'require_input': False},

	#online results
	"wikipedia_search": {'task': "-", 'class': "-", 'require_input': False},

	#launch AI settings
	"launch settings": {'task': "-", 'class': "-", 'require_input': False},

	#sound system access
	"unmute": {'task': "-", 'class': "-", 'require_input': False},
	"mute": {'task': "-", 'class': "-", 'require_input': False}, 

	#shutdown
	"shutdown pc": {'task': "-", 'class': "-", 'require_input': False},

	#create file
	"create_files": {'task': CRF.Create, 'class': CRF, 'require_input': True},

	#temperature
	"room_temp_c": {'task': "-", 'class': "-", 'require_input': False},
	"room_temp_f": {'task': "-", 'class': "-", 'require_input': False},

	#humidity
	"room_humidity": {'task': "-", 'class': "-", 'require_input': False},

	#light density
	"room_light_density": {'task': "-", 'class': "-", 'require_input': False},

	#remote control value
	"ir_value": {'task': "-", 'class': "-", 'require_input': False},

	#relay control
	"relay_1_on": {'task': "-", 'class': "-", 'require_input': False},
	"relay_1_off": {'task': "-", 'class': "-", 'require_input': False},
	"relay_2_on": {'task': "-", 'class': "-", 'require_input': False},
	"relay_2_off": {'task': "-", 'class': "-", 'require_input': False},
}

if __name__ == '__main__':
	print(dictionary['unmute'])
