from typing import Literal
import flet as ft
from flet_toast import ToastV2
from command.advancements import Advancement
from command.generators import GeneratorCard
import os
import time
import logging_v2 as log
from progressbar_v2 import prange

VERSION: Literal['2.0.3'] = "2.0.3"
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
                "body":None
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
            "gen-time":1,
            "materials-display": ft.Text("[LOADING]"),
            "money-display": ft.Text("[LOADING]"), # ok maybe selling silicon is scrapped # ill probably do smth like uhh make pc parts bitcoin mining thing?
            "pc-parts":{},
            # example:
            # "pc-parts": {
                #{
                    #name: "PC #01",
                    #parts: {
                        #"cpu":"SOMERANDOMTHING-0000",
                        #"ram":{"display":"SOMETHING-0000","value":1},
                        #
                    #}
                #}
            #}
            "bmc_data":{None:...}
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
    #### SETTING FUN
    def handle_check_dtc(e):
        if dark_theme_checkbox.value is True:
            page.theme_mode = ft.ThemeMode.DARK
        else:
            page.theme_mode = ft.ThemeMode.LIGHT
        page.update()
    #### END SETTING FUN (very sad)
    #### SETTING VARS
    dark_theme_checkbox = ft.Checkbox(label="Dark Theme", on_change=handle_check_dtc, value=True) # spookers
    #### END SETTING VARS
    #### GEN FUN
    def _0_1_01(_): # buy generator quantux 1 01 # [_0 = buy generator, _1 = quantux 1, _01 = generator 01]
        if data["quantux"]["1"]["money"] >= data["quantux"]["1"]["gen-01"]["cost"]:
            log.info("user has enough")
            data["quantux"]["1"]["money"] -= data["quantux"]["1"]["gen-01"]["cost"]
            data["quantux"]["1"]["gen-01"]["amount"] += 1
            data["quantux"]["1"]["gen-01"]["cost"] *= data["quantux"]["1"]["gen-01"]["growth"]
            data["quantux"]["1"]["gen-01"]["body"].control.tooltip = "Your first generator. The cheapest one infact."
            data["quantux"]["1"]["gen-01"]["body"].value = "Cost: {}".format(data["quantux"]["1"]["gen-01"]["cost"])
            data["quantux"]["1"]["gen-01"]["body"].update_all()
        else:
            log.info("user don't have enough")
        data["quantux"]["1"]["gen-01"]["body"].set_trailing(ft.Text(str(data["quantux"]["1"]["gen-01"]["amount"]), style=ft.TextThemeStyle.BODY_LARGE))
    #### END GEN FUN :((((((
    
    #### GEN VARS
    data["quantux"]["1"]["gen-01"]["body"] = GeneratorCard("Your first generator. The cheapest one infact.", ft.Icon(ft.icons.FACTORY), "Gen SILICA-00", _0_1_01)
    #### END GEN VARS
    
    #### GAME FUN
    def _1_1_0(): # game update data # [_1 = game stuff, _1 = quantux 1, _0 = update displays and data]
        data["quantux"]["1"]["materials-per-gen"] = (data["quantux"]["1"]["gen-01"]["amount"]*data["quantux"]["1"]["gen-01"]["generates"])
        data["quantux"]["1"]["materials-display"].value = "Silicon: {}".format(data["quantux"]["1"]["materials"])
        data["quantux"]["1"]["money-display"].value = "Simulons: {}".format(data["quantux"]["1"]["money"])
        data["quantux"]["1"]["money-display"].update()
        data["quantux"]["1"]["materials-display"].update()
        pass
    def _1_1_1(): # game update data (data (actual data (trust (me))))
        data["quantux"]["1"]["materials"] += data["quantux"]["1"]["materials-per-gen"]
        data["quantux"]["1"]["money"] += data["quantux"]["1"]["money-per-gen"]
        time.sleep(data["quantux"]["1"]["gen-time"])
    #### END GAME FUN (nooooo no more game fun)
    

    def route_change(route):
        page.views.clear()
        page.overlay.clear()
        page.views.append(
            ft.View(
                "/",
                [
                    ft.AppBar(title=ft.Text("CommandIncremental "+VERSION, tooltip="cmd incremental - the game"), actions=[
                        ft.IconButton(ft.icons.EMOJI_EVENTS, on_click=lambda _: page.go("/advancements"), tooltip="advancing in life"),
                        ft.IconButton(ft.icons.UPGRADE, on_click=lambda _: page.go("/upgrades"), tooltip="upgrading life"),
                        ft.IconButton(ft.icons.SETTINGS, on_click=lambda _: page.go("/settings"), tooltip="setting life")
                    ]),
                    # ft.Text("Hello this is very epic!!!"),
                    ft.Text("home page placeholder"),
                    data["quantux"]["1"]["money-display"],
                    data["quantux"]["1"]["materials-display"]
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
        elif page.route.startswith("/upgrades"):
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
            if page.route == "/upgrades/generators":
                page.views.append(
                    ft.View(
                        "/upgrades/generators", [
                            ft.AppBar(title=ft.Text("CommandIncremental | Upgrades -> Generators")),
                            ft.Text("Work In Progress"),
                            data["quantux"]["1"]["gen-01"]["body"]
                        ]
                    )
                )
        elif page.route.startswith("/settings"):
            page.views.append(
                ft.View(
                    "/settings", [
                        ft.AppBar(title=ft.Text("CommandIncremental | Settings")),
                        dark_theme_checkbox
                    ]
                )
            )
            if page.route == "/settings/debug":
                page.views.append(ft.View("/settings/debug"))
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)
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
        if not newcomer_adv.shown or not clicked_adv.shown:
            try:
                newcomer_adv.show()
                clicked_adv.show()
                # data["quantux"]["1"]["gen-01"]["body"].show()
            except Exception as e:
                # log.error(f"ERROR: {e}")
                pass
        if clicked_adv.completed:
            clicked_adv.value = "Click the advancement card."
            clicked_adv.update_text()
        try:
            reload_all_advs(None)
        except:
            pass
        _1_1_0()
        _1_1_1()
        time.sleep(time_delay)
    
    # page.views[0].page.overlay.append(ToastV2("hmm", "titled"))
    
if __name__ == "__main__":
    ft.app(target=app)
