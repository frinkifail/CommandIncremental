from typing import Literal
import flet as ft
from flet_toast import ToastV2
from command.advancements import Advancement
import os
import time
import logging_v2 as log

VERSION: Literal['2.0'] = "2.0.0"
time_delay: float = 0.25

def app(page: ft.Page) -> None:
    page.title = "CommandIncremental "+VERSION
    page.scroll = ft.ScrollMode.ADAPTIVE
    if os.name == "nt":
        page.window_title_bar_hidden = True
    else:
        page.window_frameless = True
    # page.window_title_bar_buttons_hidden = True
    
    #### FUN TESTS
    def complete_testadv(_):
        testadv.complete()
        # print("complete")
        log.debug("complete")
    def reload_all_advs(_):
        testadv.check_if_completed()
        testadv.update()
        log.debug("successfully reloaded all advancements")
    #### END FUN TEST (sad)
    
    #### VAR TESTS
    testnoti = ToastV2("Hello world!", "Test", lambda _: print("Hello World!"))
    testadv = Advancement("Play the game.", ft.Icon(ft.icons.PLAY_ARROW), "Newcomer", complete_testadv)
    # time.sleep(1)
    #### END VAR TESTS

    def route_change(route):
        page.views.clear()
        page.views.append(
            ft.View(
                "/",
                [
                    ft.AppBar(title=ft.Text("CommandIncremental "+VERSION)),
                    ft.Text("Hello this is very epic!!!"),
                    ToastV2("Ayo what?"),
                    ToastV2("hmm", "titled"),
                    ft.ElevatedButton('Reveal', on_click=lambda _: testnoti.show()),
                    ft.ElevatedButton('Hide', on_click=lambda _: testnoti.hide()),
                    ft.ElevatedButton('Autohide', on_click=lambda _: testnoti.autorehide()),
                    testnoti,
                    testadv,
                    ft.FilledTonalButton("reload all advs", on_click=reload_all_advs),
                    # ft.ElevatedButton("Visit Store", on_click=lambda _: page.go("/store")),
                ],
            )
        )
        # testadv.show()
        if page.route == "/new_stuff":
            page.views.append(
                ft.View(
                    "/new_stuff",
                    [
                        ft.AppBar(title=ft.Text("CommandIncremental | New Stuff")),
                        ft.Text("wher is my new content???")
                        # ft.ElevatedButton("Go Home", on_click=lambda _: page.go("/")),
                    ],
                )
            )
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)
    testadv.show()
    # testadv.check_if_completed()
    while True:
        # testadv.update()
        # try:
        #     testadv.check_if_completed()
        # except Exception as e:
        #     # print("opp- error")
        #     # log.error(f"ERROR : {e}")
        #     pass
        time.sleep(time_delay)
    
    # page.views[0].page.overlay.append(ToastV2("hmm", "titled"))
    
if __name__ == "__main__":
    ft.app(target=app)
