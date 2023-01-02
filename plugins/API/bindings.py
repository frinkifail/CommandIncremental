from typing import *
displayunit = "silicon"
displayunit2 = "Silicon"
moneydisplayunit = "§"
moneydisplayunit2 = "§"
class Logger:
    def info(*message: Any) -> NoReturn:
        for i in range(message.__len__()):
            print(f"[Plugins] {message[i]}")
# def setSilicon()
