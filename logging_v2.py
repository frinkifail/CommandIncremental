import colorama as cl;
from datetime import datetime;
cl.init(autoreset=True)

now = datetime.now()

level = "INFO"

class BasicConfig:
	def __init__(self, level):
		self.level = level
	def return_cfg(self):
		return [self.level]

def info(*o, ob=None, clr=cl.Fore.GREEN):
	# print(o)
	if not o == (None,):
		for index in o:
			print(f"[{level}] {cl.Fore.BLUE}{now} : {clr}{index}");
	elif ob and o == (None,):
		for index in ob:
			print(f"[{level}] {cl.Fore.BLUE}{now} : {clr}{index}");
	else:
		print("IDK")

def warn(*o, clr=cl.Fore.YELLOW):
	global level
	oldlevel = level
	basic_config(BasicConfig("WARN"))
	info(None, ob=o, clr=clr)
	basic_config(BasicConfig(oldlevel))

def error(*o, clr=cl.Fore.RED):
	global level
	oldlevel = level
	basic_config(BasicConfig("ERROR"))
	info(None, ob=o, clr=clr)
	basic_config(BasicConfig(oldlevel))

def debug(*o, clr=cl.Fore.WHITE+cl.Style.DIM):
	global level
	oldlevel = level
	basic_config(BasicConfig("DEBUG"))
	info(None, ob=o, clr=clr)
	basic_config(BasicConfig(oldlevel))

def basic_config(config: BasicConfig):
	global level
	level = config.return_cfg()[0]

