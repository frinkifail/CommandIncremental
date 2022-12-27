# import os
# os.chdir("../../API")
import sys
sys.path.append("../../API")
import bindings
sys.path.pop()
sys.path.append("../../..")
from main import setSilicon, addToPage
import flet as ft
import time
# def main():
# print("hello world")
bindings.Logger.info("Test Plugin Loaded!")
bindings.displayunit = "test"
bindings.displayunit2 = "Test"
setSilicon(10000)
time.sleep(5)
addToPage(ft.Text("Hello!"))
