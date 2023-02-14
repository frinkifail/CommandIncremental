import os
import flet as ft
from main import data
import logging_v2 as log

bmc_data_1: dict = data["quantux"]["1"]["bmc_data"]

def bmf_app(page: ft.Page):
    log.info("Data:",data)
    page.title = "Bitcoin Miner"
    page.scroll = ft.ScrollMode.ADAPTIVE
    if os.name == "nt":
        page.window_title_bar_hidden = True
    else:
        page.window_frameless = True
    
