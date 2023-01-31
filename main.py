from typing import Literal
import flet as ft
from flet_toast import ToastV2
from command.advancements import Advancement
from command.generators import GeneratorCard
import os
import time
import logging_v2 as log
from progressbar_v2 import prange

VERSION: Literal['2.0.2'] = "2.0.2"
time_delay: float = 0.25

data = {
    "quantux":{
        "1":{
            "materials":0, # silicon âฺüึgุhี
            "gen-01":{
                "amount":0, # ok incase i forgor this uses money and not materials
                "cost":10,  # ^ put that since im dumb and will forgor
                "growth":1.08, # yeah im dumb since i put that in the wrong line
                "generates":0.1,
                "body":GeneratorCard("Your first generator. The cheapest one infact.", ft.icons.FACTORY, "Gen SILICA-00")
            },
            "materials-per-gen":0,
            "money":10,
            "money-per-gen":0,
            "houses":[], # example:
            # "houses":[
                #{
                    #name: "RANDOMLY GENERATED",
                    #generating: 69,
                    #happyratio: 420 # max from 0-100 floating number but not now
                #}
            #]
            "gen-time":1
        }
    }
}

def app(page: ft.Page) -> None:
    page.title = "CommandIncremental "+VERSION
    page.scroll = ft.ScrollMode.ADAPTIVE
    if os.name == "nt":
        page.window_title_bar_hidden = True
    else:
        page.window_frameless = True
    # page.window_title_bar_buttons_hidden = True
    
    #### ADV FUN
    def reload_all_advs(_):
        newcomer_adv.check_if_completed()
        newcomer_adv.update()
        clicked_adv.check_if_completed()
        clicked_adv.update()
    #### END ADV FUN
    
    #### FUN TESTS
    # def complete_testadv(_):
    #     newcomer_adv.complete()
    #     # print("complete")
    #     log.debug("complete")
    
        # log.debug("successfully reloaded all advancements")
    #### END FUN TEST (sad)
    
    #### VAR TESTS
    testnoti = ToastV2("Hello world!", "Test", lambda _: print("Hello World!"))
    
    # time.sleep(1)
    #### END VAR TESTS
    #### ADV VARS
    newcomer_adv = Advancement("Play the game.", ft.Icon(ft.icons.PLAY_ARROW), "Newcomer")
    clicked_adv = Advancement("???", ft.Icon(ft.icons.MOUSE), "Clicker game?", onclick=lambda _: clicked_adv.complete())
    #### END ADV VARS
    #### GAME VARS
    
    #### END GAME VARS
    #### GEN VARS
    
    #### END GEN VARS

    def route_change(route):
        page.views.clear()
        page.overlay.clear()
        page.views.append(
            ft.View(
                "/",
                [
                    ft.AppBar(title=ft.Text("CommandIncremental "+VERSION, tooltip="cmd incremental - the game"), actions=[
                        ft.IconButton(ft.icons.EMOJI_EVENTS, on_click=lambda _: page.go("/advancements"), tooltip="advancing in life"),
                        ft.IconButton(ft.icons.UPGRADE, on_click=lambda _: page.go("/upgrades"), tooltip="upgrading life")
                    ]),
                    # ft.Text("Hello this is very epic!!!"),
                    ft.Text("home page placeholder"),
                    # ToastV2("Ayo what?"),
                    # ToastV2("hmm", "titled"),
                    # ft.ElevatedButton('Reveal', on_click=lambda _: testnoti.show()),
                    # ft.ElevatedButton('Hide', on_click=lambda _: testnoti.hide()),
                    # ft.ElevatedButton('Autohide', on_click=lambda _: testnoti.autorehide()),
                    # testnoti,
                    # ft.ElevatedButton("Summon Progressbar", on_click=lambda _: prange(100, 0, 1, None, "summoned progressbar from flet", None))
                    # ft.FilledTonalButton("reload all advs", on_click=reload_all_advs),
                    # ft.ElevatedButton("Visit Store", on_click=lambda _: page.go("/store")),
                ]
            )
        )
        page.overlay.append(testnoti)
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
        elif page.route == "/advancements":
            page.views.append(
                ft.View(
                    "/advancements", [
                        ft.AppBar(title=ft.Text("CommandIncremental | Advancements", tooltip="advancing in life")),
                        ft.Row([newcomer_adv,
                        clicked_adv])
                    ]
                )
            )
        elif page.route == "/upgrades":
            page.views.append(
                ft.View(
                    "/upgrades", [
                        ft.AppBar(title=ft.Text("CommandIncremental | Upgrades"), actions=[
                            ft.IconButton(ft.icons.FACTORY, on_click=lambda _: page.go("/upgrades/generators"), tooltip="generators")
                        ]),
                        ft.Text("Work In Progress")
                    ]
                )
            )
            pass
        elif page.route == "/upgrades/generators":
            page.views.append(
                ft.View(
                    "/upgrades/generators", [
                        ft.AppBar(title=ft.Text("CommandIncremental | Upgrades -> Generators")),
                        ft.Text("Work In Progress"),
                        data["quantux"]["1"]["gen-01"]["body"]
                    ]
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
    
    while not newcomer_adv.shown or not clicked_adv.shown:
        try:
            newcomer_adv.show()
            clicked_adv.show()
        except:
            pass
    while not newcomer_adv.completed:
        newcomer_adv.complete()
    # testadv.check_if_completed()
    while True:
        # testadv.update()
        # try:
        #     testadv.check_if_completed()
        # except Exception as e:
        #     # print("opp- error")
        #     # log.error(f"ERROR : {e}")
        #     pass
        if clicked_adv.completed:
            clicked_adv.value = "Click the advancement card."
            clicked_adv.update_text()
        try:
            reload_all_advs(None)
        except:
            pass
        time.sleep(time_delay)
    
    # page.views[0].page.overlay.append(ToastV2("hmm", "titled"))
    
if __name__ == "__main__":
    ft.app(target=app)
