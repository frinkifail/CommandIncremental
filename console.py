# from main import interactableConsole, console_setsiliconval, silicon # wait why wont i just import silicon? # uhhhhhh
from main import interactableConsole
from threading import Thread

consoleThread = Thread(target=interactableConsole)
consoleThread.start()