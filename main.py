import os
from subprocess import Popen
import sys
import notificationFlet as ftn
import json
import time
from threading import Thread
import flet as ft
import random
import logging_v2 as log
try: import keyboard
except: log.error("keyboard gone")
# logging.basicConfig(level=logging.DEBUG)

log.info("[ParentThread/Main => Parent] Server Started!")
try:
    from replit import db
except ImportError as e:
    log.warn("[ParentThread => Imports] unable to import database from replit, assuming running custom server",e)
# import math

sys.path.append("plugins/API")
import bindings
from typing import *

silicon: float = 0 # limit at 1e+308 :cry:
siliconperspec: float = 0.108
maxsilicon: float = 15
maxsiliconcost: float = 10
siliconmultiplier: float = 1
siliconmultipliercost: float = 365
displaysiliconunit: str = bindings.displayunit
displaysiliconunit2: str = bindings.displayunit2

money: int = 10
moneyperspec: int = 0
moneymultiplier: int = 1
displaymoneyunit: str = bindings.moneydisplayunit
displaymoneyunit2: str = bindings.moneydisplayunit2

gen1 = {
    "cost": 10,
    "growth": 1.28,
    "amount": 0
}
buymax: bool = False
saveenabled: bool = True
updateinterval: float = 0.0025
version: str = "1.8"  # forgor to bump version
# Other shit used in main function
debugsiliconnotiinuse: bool = False
notate: bool = True
legacymodebool: bool = False
silicongenwaittime: float = 0.8
silicongenwaittimecost: float = 550
consolepage: str = "main"
console_setsiliconval: None = None
console_lastcmd: str = ""
pluginscriptfiles = []
pluginwantstoaddpage: bool = False
pluginwantstoaddpage_content: None = None
plugins = []
pluginnames = []
plugindescs = []
pluginvers = []

signed_up: bool = False
force_allow_no_login: bool = True
logged_in: bool = False
key: str = ""

quitall = False

documentation_open: bool = False # Documentation open in this server session?

houses: list[dict] = [{"base_cost":1200, "growth":random.randint(300, 2800)}]


class Advancement(ft.UserControl):
    def __init__(self, title: str, description: str, icon: ft.Icon) -> None:
        super().__init__()
        self.title: str = title
        self.desc: str = description
        self.icon: ft.Icon = icon
        self.completed: bool = False
        self.checkmark: ft.Icon = ft.Icon(ft.icons.CHECK, color=ft.colors.GREEN_ACCENT)
        self.already_completed: bool = False
        self.maincontainer = ft.Container(ft.Column([ft.Row([self.icon, ft.Text(self.title, style=ft.TextThemeStyle.HEADLINE_SMALL)]), ft.Text(self.desc, style=ft.TextThemeStyle.LABEL_LARGE)]))
    def build(self):
        return self.maincontainer
    def if_completed(self):
        if self.completed:
            if not self.already_completed: self.maincontainer.content.controls[0].controls.append(self.checkmark)
            self.already_completed = True
        else:
            try: self.maincontainer.content.controls[0].controls.remove(self.checkmark)
            except: log.warn("[ParentThread/Advancement => Remove] Couldn't remove checkmark!")
    def complete(self): self.completed = True
    def uncomplete(self): self.completed = False

def quitAll():
    global quitall
    if quitall:
        quitall = False
        log.info("[ParentThread/QuitAll => Main] Switched quitall to False")
    else:
        quitall = True
        log.info("[ParentThread/QuitAll => Main] Switched quitall to True")
        

def setSilicon(count: float):
    global silicon
    log.debug(f"[ParentThread/PluginHelper => SetSilicon] Old Silicon Count: {silicon}")
    silicon = count
    log.info("[ParentThread/PluginHelper => SetSilicon] Set silicon done!")
    log.debug(f"[ParentThread/PluginHelper => SetSilicon] New Silicon Count: {silicon}")


def addToPage(content):
    global pluginwantstoaddpage_content, pluginwantstoaddpage
    pluginwantstoaddpage = True
    pluginwantstoaddpage_content = content
    log.info(f"[ParentThread/PluginHelper => AddContentToPage] Added {content}!")  # nooooooooooo idk how to make thissss


def loadPlugins():
    # global pluginscriptfiles
    def executePlugins():
        global displaysiliconunit2, displaysiliconunit
        for i in range(pluginscriptfiles.__len__()):
            exec(open(pluginscriptfiles[i], 'r').read())
            # print(bindings.displayunit)
            displaysiliconunit = bindings.displayunit
            displaysiliconunit2 = bindings.displayunit2
            # pluginThread = Thread(target=)

    os.chdir("./plugins")
    global plugins
    plugins = os.listdir(".")
    # plugins = oldplugins.remove("API")
    plugins.remove("API")
    scriptfiles = []
    # print(["Hi", "API"].remove("API"))
    log.info("[ParentThread/PluginLoader => PluginChecker] Available plugins: " + str(plugins))
    
    for i in range(plugins.__len__()):
        try:
            os.chdir(plugins[i])
        except:
            os.chdir("..")
            os.chdir(plugins[i])
        metadata = open("./meta.json")
        parsed_metadata = json.load(metadata)
        if parsed_metadata["enabled"]:
            if os.path.exists("meta.json"):
                pluginnames.append(parsed_metadata["name"])
                plugindescs.append(parsed_metadata["desc"])
                pluginvers.append(parsed_metadata["version"])
                if parsed_metadata["enabled"]:
                    if os.path.exists("scripts"):
                        global pluginscriptfiles
                        os.chdir("scripts")
                        # pluginscriptfiles = []
                        pluginscriptfiles = os.listdir(".")
                        executePlugins()
                    else:
                        log.warn(
                            "[ParentThread/PluginLoader => ScriptChecker] No scripts available, loading only metadata")
        else:
            log.info("[ParentThread/PluginLoader => MetaChecker] Plugin disabled in meta, not counting")
        os.chdir("..")

available_names: list[str] = [
    "Hello World",
    "Unwelcomed",
    "Welcomed?",
    "Weirdly",
    "Pocosticks"
]

def main(page: ft.Page) -> NoReturn:
    global buymax
    page.title = "CommandIncremental"
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.window_frameless = True
    page.window_maximizable = False
    page.window_width = 800
    page.window_height = 600

    # Other Variables
    # debugsiliconnotiinuse = False
    # fuckerinas it doesn't work!
    # buymax = False
    def handleBuyHouse(e) -> None:
        global money
        houses[0]["growth"] = random.randint(300, 2800)
        bc: int = houses[0]["base_cost"]
        gr: int = houses[0]["growth"]
        bc += gr
        if money < bc:
            money -= bc
            houses.append({"name":random.choice(available_names), "cost":bc, "generatable":random.randint(50,2900)})
            

    def buygen1(e) -> None:
        global money, gen1, siliconperspec
        if money >= gen1["cost"]:
            money -= gen1["cost"]
            # page.client_storage.set("silicon", page.client_storage.get("silicon")-gen1["cost"])
            gen1["cost"] *= gen1["growth"]
            gen1["amount"] += 1
            siliconperspec += 0.18
            adv_firstgen.complete()
            if adv_firstgen.already_completed:
                pass
            else:
                adv_gainnoti[3](None)
            log.info("[MainThread/Generators => 1] bought!")
        else:
            log.info("[MainThread/Generators => 1] not enough silicon")
            
    def handleSellSilicon(e):
        global silicon, money
        if silicon < 1:
            log.info("[MainThread/HandleSellSilicon => If?] Not enough!")
        elif silicon > 1:
            for i in range(silicon.__floor__()):
                if silicon > 1: silicon -= 1; money += 0.7
                else: log.warn("[MainThread/HandleSellSilicon => If?] Enough but also not?"); continue
                

    def handleNewSave(e) -> None:
        global key
        if saveenabled:
            
            db[key]["silicon"] = silicon
            db[key]["siliconperspec"] = siliconperspec
            db[key]["gen1"] = gen1
            db[key]["maxsilicon"] = {"max": maxsilicon, "cost": maxsiliconcost}
            db[key]["silicongwt"] = silicongenwaittime
            db[key]["silicongwt_c"] = silicongenwaittimecost
            db[key]["siliconmul"] = siliconmultiplier
            db[key]["siliconmul_c"] = siliconmultipliercost
            log.info('[MainThread/Handler => Save] Statistics Saved!')
        else:
            log.warn(
                '[MainThread/Handler => Save] Failed to save: Saving/Loading is disabled')

    def handleNewLoad(e):
        global silicon, siliconperspec, gen1, maxsilicon, maxsiliconcost, silicongenwaittime, silicongenwaittimecost, siliconmultiplier, siliconmultipliercost, key
        if saveenabled:
            silicon = db[key]["silicon"]
            siliconperspec = db[key]["siliconperspec"]
            gen1 = db[key]["gen1"]
            maxsilicon = db[key]["maxsilicon"]["max"]
            maxsiliconcost = db[key]["maxsilicon"]["cost"]
            silicongenwaittime = db[key]["silicongwt"]
            silicongenwaittimecost = db[key]["silicongwt_c"]
            siliconmultiplier = db[key]["siliconmul"]
            siliconmultipliercost = db[key]["siliconmul_c"]
            log.info('[MainThread/Handler => Load] Statistics Loaded!')
        else:
            log.warn(
                '[MainThread/Handler => Load] Failed to load: Saving/Loading is disabled')

    def handleDebugPts(e):
        global silicon, saveenabled, debugsiliconnotiinuse
        try:
            if debugsilicontf.value != '':
                silicon = int(debugsilicontf.value)
                log.info(
                    f"[MainThread/Debug => SetSilicon] Set Silicon Count to {0}".format(int(debugsilicontf.value)))
                if not debugsiliconnotiinuse:
                    debugsiliconnotiinuse = True
                    page.views[1].controls.append(debugsiliconnoti[0])
                    page.views[1].update()
                    debugsiliconnoti[2](None)
                    time.sleep(1)
                    debugsiliconnoti[3](None)
                    time.sleep(1)
                    page.views[1].controls.pop()
                    debugsiliconnotiinuse = False
                else:
                    log.warn(
                        "[MainThread/Debug => Notifications] Notification Animation is playing, won't play "
                        "overlapping animation")
            else:
                log.warn(
                    "[MainThread/Debug => SetSilicon] Set Silicon Text Field's value is invalid, won't set to that...")
            saveenabled = False
            log.info(
                "[MainThread/Handler => SaveHandle] Disabled saving, debug silicon handle is called")
        except Exception:  # ugh it doesn't catch because threads fucking suck
            log.warn(
                "[MainThread/Debug => Notification] wow, thats funny, see, the user switched views before i could "
                "remove the notification, in conclusion, fuck you")

    def handleBuyMax(e):
        global buymax
        if buymax is False:
            buymax = True
            buymaxbtn.text = f"Buy Max: {buymax}"
            page.update()
        else:
            buymax = False
            buymaxbtn.text = f"Buy Max: {buymax}"
            page.update()

    def handleInfSilicon(e):
        global silicon
        handleDebugPts(None)
        silicon = 1e+306  # ._.

    def handleUpdateInterval(e):
        global updateinterval
        updateinterval = float(updateintervaltf.value)
        log.info("[MainThread/Handler => Updater] Changed update interval!")

    def handleUpgradeMax(e):
        global maxsilicon, maxsiliconcost, money
        if money >= maxsiliconcost:
            money -= maxsiliconcost
            maxsiliconcost *= 1.41
            maxsilicon *= 1.38
            # ahhhh im so stupid
            upgrades_max.text = f"Max Silicon [{maxsilicon}] | Cost: [{maxsiliconcost}]"
            log.info("[MainThread/Upgrades => MaxSilicon] Upgraded this upgrade!")
        else:
            log.info(
                "[MainThread/Upgrades => MaxSilicon] Not enough silicon to upgrade this!")

    def handleUpgradeMultiplier(e):
        global money, siliconmultipliercost, siliconmultiplier
        if money >= siliconmultipliercost:
            money -= siliconmultipliercost
            siliconmultipliercost *= 1.69
            siliconmultiplier += 1.5
            upgrades_siliconmultiplier.text = f"Silicon Multiplier [{siliconmultiplier}] | Cost: [{siliconmultipliercost}]"
            upgrades_siliconmultiplier.tooltip = f"Gain more silicon per {silicongenwaittime} seconds"
            log.info("[MainThread/Upgrades => Multiplier] Upgraded this upgrade!")
        else:
            log.info(
                "[MainThread/Upgrades => Multiplier] Not enough silicon to upgrade this!")

    def handleUpgradeGenWaitTime(e):
        global money, silicongenwaittime, silicongenwaittimecost
        if silicongenwaittime > 0.02:
            if money >= silicongenwaittimecost:
                money -= silicongenwaittimecost
                silicongenwaittimecost *= 1.80
                silicongenwaittime -= 0.01
                upgrades_waittime.text = f"Generation Time [{silicongenwaittime}] | Cost: [{silicongenwaittimecost}]"
                log.info("[MainThread/Upgrades => WaitTime] Upgraded this upgrade!")
            else:
                log.info(
                    "[MainThread/Upgrades => WaitTime] Not enough silicon to upgrade this!")
        else:
            log.info("[MainThread/Upgrades => WaitTime] Reached Max Upgrade!")

    def handleDarkThemeChange(e):
        if darktheme.value:
            page.theme_mode = ft.ThemeMode.DARK
        else:
            page.theme_mode = ft.ThemeMode.LIGHT

    # fuck this idk how to make it work # ok, maybe i know how it works, but im just too lazy
    def handleLegacyMode(e):
        global legacymodebool
        if legacymode.value:
            page.views[0].appbar = ft.AppBar(
                title=ft.Text(f"CommandIncremental Legacy {version}", tooltip="the game but desktop"),
                center_title=True,
                actions=[ft.IconButton(ft.icons.SETTINGS, on_click=lambda _: page.go("/settings"), tooltip="Settings"),
                         ft.IconButton(
                             ft.icons.UPGRADE, on_click=lambda _: page.go("/upgrades"), tooltip="Upgrades"),
                         ft.IconButton(ft.icons.BUG_REPORT, on_click=lambda _: page.go("/debug"),
                                       tooltip="Some debug utilities"),
                         ft.IconButton(ft.icons.CLOSE, icon_color=ft.colors.RED,
                                       on_click=lambda _: page.window_close())])
            page.views[0].controls.append(windowdragarea)
            page.views[0].update()
            legacymodebool = True
        else:
            page.views[0].appbar = ft.AppBar(title=ft.Text(f"CommandIncremental Web {version}", tooltip="the game"),
                                             center_title=True,
                                             actions=[ft.IconButton(ft.icons.SETTINGS, on_click=lambda _: page.go(
                                                 "/settings"), tooltip="Settings"), ft.IconButton(ft.icons.UPGRADE,
                                                                                                  on_click=lambda
                                                                                                      _: page.go(
                                                                                                      "/upgrades"),
                                                                                                  tooltip="Upgrades"),
                                                      ft.IconButton(ft.icons.BUG_REPORT, # what happened here lmao
                                                                    on_click=lambda _: page.go("/debug"),
                                                                    tooltip="Some debug utilities")])
            page.views[0].controls.remove(windowdragarea)
            page.views[0].update()
            legacymodebool = False

    def handleManualBoost(e):
        global silicon, siliconmultiplier, siliconperspec
        silicon += siliconperspec * siliconmultiplier

    def view1add(content: ft.Control):
        page.views[1].controls.append(content)
        page.views[1].update()

    def handleConsoleCommand(e, cmd=None):
        global silicon, console_lastcmd
        # if console_lastcmd == "lastcmd":
        # pass
        # console_lastcmd = "get-silicon"
        # ctbv = "get-silicon"
        # else:
        if consoleTextBox.value:
            if not cmd:
                ctbv = consoleTextBox.value
            else:
                ctbv = cmd
        else:
            ctbv = "lastcmd"
        ctbv = ctbv.lower()
        if ctbv.startswith("set-silicon ") or ctbv.startswith("ss "):
            try:
                ssv = float(ctbv[11:])
            except:
                ssv = float(ctbv[3:])
            # if isinstance(ssv, float):
            silicon = ssv
            page.views[1].controls.append(ft.Text("[Main/Console => SetSilicon] Done!"))
            console_lastcmd = ctbv
        elif ctbv == "kill":
            page.views[1].controls.append(ft.Text("[Main/Console => KillWindow] Killing all..."))
            page.views[1].update()
            if os.name == "nt":
                os.system("taskkill /f /im python.exe")
                os.system("taskkill /f /im python3.exe")
            else:
                os.system("killall python3")
                os.system("pkill python3")
            console_lastcmd = ctbv
        elif ctbv == "quit":
            view1add(ft.Text("[Main/Console => Quit] Quitting all..."))
            quitAll()
        elif ctbv == "get-silicon" or ctbv == "gs":
            page.views[1].controls.append(ft.Text(f"[Main/Console => GetSilicon] Silicon Count Is: {silicon}"))
            page.views[1].update()
            console_lastcmd = ctbv
        elif ctbv == "lastcmd" or ctbv == "" or ctbv == "lc":
            #
            # consoleTextBox.value = ""
            # ctbv = console_lastcmd
            # ctbv = cmd
            handleConsoleCommand(None, console_lastcmd)  # idk why "" doesn't work :skull: # oh wait fuck it clears it uhhh
        elif ctbv == "test" or ctbv == "t":
            view1add(ft.Text("Working!"))
            console_lastcmd = ctbv
        elif ctbv == "get-displayunit":
            global displaysiliconunit2, displaysiliconunit
            view1add(ft.Text(displaysiliconunit))
            view1add(ft.Text(displaysiliconunit2))
        # if not consoleTextBox.value:
        # handleConsoleCommand(None, console_lastcmd)

        # if not console_lastcmd == "lastcmd":
        # else:
        # console_lastcmd = "get-silicon"
        consoleTextBox.value = ""

    # page.views[1].update() # no idea how to make this work lmfao # faulty line 😡 # old line, ignore pls
    # fpscounter = ft.Text("FPS: [DISABLED]")
    buymaxbtn = ft.TextButton(
        f"Buy Max: {buymax}", on_click=handleBuyMax, tooltip="buy factories until you're outta silicons")
    # page.add(buymaxbtn)
    siliconcounter = ft.Text(str(silicon) + " silicon",
                             tooltip="silicon counter yuh")
    buygen1button = ft.ElevatedButton(
        f"Buy Basic anferiog i fucking forgor ({gen1['amount']}) | Cost: {gen1['cost']}$", on_click=buygen1,
        tooltip="buy them **basic** generators")
    # page.add(fpscounter, siliconcounter, buygen1button)
    savefiletf = ft.TextField(
        label="Save ID", tooltip="enter your save id here")
    debugsilicontf = ft.TextField(
        label="Set Silicons",
        tooltip="set your silicon to specific value (debugging purposes + saving will be disabled)")
    updateintervaltf = ft.TextField(label="Update Interval", shift_enter=True, on_submit=handleUpdateInterval,
                                    width=200,
                                    tooltip="sets your update interval (doesn't make you generate silicon faster ._.)")
    overflowwarn = ftn.createNoti(
        None, "Warning!", "Silicons are overflowing! Update thread has stopped!")
    debugsiliconnoti = ftn.createNoti(None, "Debug", "Changed silicon amount!")
    notatecheckbox = ft.Checkbox(label="Scientific Notation")
    # notatecheckbox.value = True
    darktheme = ft.Checkbox(label="Dark Theme")
    darktheme.value = True
    darktheme.on_change = handleDarkThemeChange
    # UPGRADES
    upgrades_max = ft.ElevatedButton(
        f"Max Silicon [{maxsilicon}] | Cost: [{maxsiliconcost}]",
        on_click=handleUpgradeMax, tooltip="Upgrade bank size"
    )
    upgrades_siliconmultiplier = ft.ElevatedButton(
        f"Silicon Multiplier [{siliconmultiplier}] | Cost: [{siliconmultipliercost}]",
        on_click=handleUpgradeMultiplier,
        tooltip=f"Gain more silicon per {silicongenwaittime} seconds"
    )
    upgrades_waittime = ft.ElevatedButton(
        f"Generation Time [{silicongenwaittime}] | Cost: [{silicongenwaittimecost}]",
        on_click=handleUpgradeGenWaitTime,
        tooltip="Wait shorter time to generate silicon"
    )
    # END UPGRADE
    # GAME UTILS
    manualboost = ft.FloatingActionButton(
        icon=ft.icons.ADD, on_click=handleManualBoost)
    moneydisplay = ft.Text(tooltip="money display")
    # END GAME UTILS
    legacymode = ft.Checkbox(label="Desktop Mode", on_change=handleLegacyMode)
    windowdragarea = ft.WindowDragArea(ft.Container(ft.Text("Drag the window!", tooltip="you can drag the window here"),
                                                    padding=10, alignment=ft.alignment.center,
                                                    tooltip="drag the window here"), tooltip="lets you drag the window")
    loadbutton = ft.ElevatedButton(
        "Load", on_click=handleNewLoad, tooltip="loads the game according to your save id")
    savebutton = ft.ElevatedButton(
        "Save", on_click=handleNewSave, tooltip="saves the game according to your save id")

    consoleTextBox = ft.TextField(label="Insert Command", shift_enter=True, on_submit=handleConsoleCommand)
    
    ############## ADVANCEMENTS #################
    adv_newcomer = Advancement("Newcomer", "Play the game.", ft.Icon(ft.icons.PLAY_ARROW))
    adv_firstgen = Advancement("First Generator", "Buy your first generator.", ft.Icon(ft.icons.FACTORY))
    
    adv_gainnoti = ftn.createNoti(None, "Advancing!", "You gained an advancement! Check it out in the Advancements tab!")
    ############ END ADVANCEMENTS ###############
    
    ############ LOGIN #################
    def handleLogin(e):
        global signed_up, logged_in, key
        if log_key_tf.value:
            if log_password_tf.value == db[log_key_tf.value]["password"]:
                log.info("Correct password!")
                if not signed_up: signed_up = True
                if not logged_in: logged_in = True
                key = log_key_tf.value
    def handleSignup(e) -> None:
        global signed_up
        if log_key_tf.value:
            if log_password_tf.value:
                log.debug("[MainThread/Login/Signup => Signuper] Signup function triggered (All the values are filled)")
                try:
                    if db[log_key_tf.value]: log.warn("[MainThread/Login/Signup => AlreadyRegistered] Cannot continue!"); view1add(ft.Text("Failed to signup: Invalid key")); return;
                except:
                    pass
                db[log_key_tf.value] = {}
                db[log_key_tf.value]["key"] = log_key_tf.value
                db[log_key_tf.value]["password"] = log_password_tf.value
                if not signed_up: signed_up = True; log.debug("[MainThread/Login/Signup => SignupChanger] Changed signed_up! ({})".format(signed_up))
    log_key_tf: ft.TextField = ft.TextField(label="Key")
    log_password_tf: ft.TextField = ft.TextField(label="Password", password=True)
    log_done_btn: ft.IconButton = ft.IconButton(ft.icons.CHECK, on_click=handleLogin)
    log_signup_btn: ft.IconButton = ft.IconButton(ft.icons.CHECK, on_click=handleSignup)
    ############ END LOGIN #################

    # notatecheckbox.value page.add(ft.Row([ft.ElevatedButton("Save", on_click=handleSave), ft.ElevatedButton("Load",
    # on_click=handleLoad), savefiletf])) page.add(ft.Row([debugsilicontf, ft.IconButton(ft.icons.CHECK,
    # on_click=handleDebugPts)]))

    def buildApp(approute):
        global saveenabled
        page.views.clear()
        # if page.route == "/":
        if not logged_in:
            saveenabled = False
        page.views.append(
            ft.View(
                "/", [
                    ft.AppBar(title=ft.Text(f"CommandIncremental {version}", tooltip="the game"), center_title=True,
                              actions=[ft.IconButton(ft.icons.SETTINGS, on_click=lambda _: page.go("/settings"),
                                                     tooltip="Settings"), ft.IconButton(
                                  ft.icons.UPGRADE, on_click=lambda _: page.go("/upgrades"), tooltip="Upgrades"),
                                       ft.IconButton(ft.icons.BUG_REPORT, on_click=lambda _: page.go("/debug"),
                                                     tooltip="Some debug utilities"),
                                       ft.IconButton(ft.icons.ABC, on_click=lambda _: page.go("/advancements"),
                                                     tooltip="Advancements")]),
                    ft.Text("Not logged in!", tooltip="log in to get rid of this message", text_align=ft.TextAlign.CENTER, style=ft.TextThemeStyle.BODY_LARGE) if not logged_in else ft.Text(),
                    # used to be window drag area,
                    # windowdragarea if os.name == "nt" or os.name == "posix" else None,
                    siliconcounter, moneydisplay, buygen1button,
                    buymaxbtn,
                    adv_gainnoti[0],
                    ft.FloatingActionButton("Sell", icon=ft.icons.MONEY, on_click=handleSellSilicon)
                    # ft.ElevatedButton("Goto Test", on_click=lambda _: page.go("/test"))
                ],
            floating_action_button=manualboost)
        )
        if page.route == "/test":
            page.views.append(
                ft.View(
                    "/test", [
                        ft.Text("Hello World!",
                                tooltip="Testing Page | Why are you here?")
                    ]
                )
            )
        elif page.route == "/settings":
            page.views.append(
                ft.View(
                    "/settings", [
                        ft.AppBar(title=ft.Text(
                            "CommandIncremental | Settings")),
                        updateintervaltf,
                        ft.Row([
                            savebutton,
                            loadbutton,
                            savefiletf if legacymodebool else ft.Text(
                                "Save ID is disabled")
                        ]),
                        notatecheckbox,
                        darktheme,
                        # legacymode ft.TextButton("Infinite Silicon", on_click=handleInfSilicon, tooltip="crashes
                        # the game") # tooltip used to be "gives you infinite silicon (for debugging purposes +
                        # saving *will* be disabled)" # i moved it
                    ]
                )
            )
        elif page.route == "/login": # :scream:
            page.views.append(
                ft.View("/login",[
                    ft.Text("CommandIncremental | Login", style=ft.TextThemeStyle.DISPLAY_SMALL),
                    log_key_tf,
                    log_password_tf,
                    ft.Row([log_done_btn, ft.OutlinedButton("Start!", on_click=lambda _: page.go("/"))])
                ])
            )
        elif page.route == "/signup":
            page.views.append(
                ft.View(
                    "/signup", [
                        ft.Text("CommandIncremental | Signup", style=ft.TextThemeStyle.DISPLAY_SMALL),
                        log_key_tf,
                        log_password_tf,
                        ft.Row([log_signup_btn,
                        ft.OutlinedButton("To Login", on_click=lambda _: page.go("/login"))])
                    ]
                )
            )
        elif page.route == "/upgrades":
            page.views.append(
                ft.View(
                    "/upgrades", [
                        ft.AppBar(title=ft.Text(
                            "CommandIncremental | Upgrades")),
                        ft.Column([
                            ft.Divider(height=3, thickness=3),
                            upgrades_max,
                            ft.Divider(height=3, thickness=3),
                            upgrades_siliconmultiplier,
                            ft.Divider(height=3, thickness=3),
                            upgrades_waittime
                        ])
                    ]
                )
            )
        elif page.route == "/advancements":
            adv_newcomer.complete()
            page.views.append(
                ft.View(
                    "/advancements", [
                        ft.AppBar(title=ft.Text("CommandIncremental | Advancements")),
                        adv_newcomer,
                        adv_firstgen,
                    ]
                )
            )
            adv_newcomer.if_completed()
            adv_firstgen.if_completed()
        elif page.route == "/debug":
            global documentation_open
            if not documentation_open: Popen(["python3.9","docs/engine/loader.py"])
            else: log.warn("[MainThread/Debug => Documentation] Documentation already open (Server)!")
            documentation_open = True
            page.scroll = ft.ScrollMode.ALWAYS
            page.views.append(
                ft.View(
                    "/debug", [
                        ft.AppBar(title=ft.Text(
                            "CommandIncremental | Debug Utilities"), actions=[ft.IconButton(ft.icons.BUILD, on_click=lambda _: page.go("/plugins"),
                                                     tooltip="Installed Plugins"),ft.IconButton(ft.icons.CODE, on_click=lambda _: page.go("/console"),
                                                     tooltip="In-app Console")]),
                        ft.Row([debugsilicontf, ft.IconButton(
                            ft.icons.CHECK, on_click=handleDebugPts, tooltip="get yo silicons!!")]),
                        ft.TextButton("Infinite Silicon", on_click=handleInfSilicon,
                                      tooltip="gives you basically infinite silicon (for debugging purposes + saving "
                                              "*will* be disabled)"),
                        ft.Text("Changelog:",
                                style=ft.TextThemeStyle.HEADLINE_MEDIUM, tooltip="yo, what's good?"),
                        ft.Text("1.2.7 | Added changelog to track stuff"),
                        ft.Text(
                            "1.2.7.1 | Minor spelling mistake *earth collapsing*"),
                        ft.Text(
                            "1.2.7.2 | Fixed debug silicon notification not showing"),
                        ft.Text(
                            "1.2.7.3 | Ok, the notification is slow, but it works alright?"),
                        ft.Text(
                            "1.2.7.4 | Forgot to make the buymax buy the upgrade :skull:"),
                        ft.Text("1.2.7.5 | ong it crashes; i fixed it"),
                        ft.Text("1.2.8 | Made scientific notation optional"),
                        ft.Text("1.2.9 | Upgrade Max actually works now"),
                        ft.Text("1.3 | Saving overhaul"),
                        ft.Text("1.4 | Saving overhaul.... again..."),
                        ft.Text(
                            "1.4.1 | Dark Theme is now optional (I know the scary people)"),
                        ft.Text(
                            "1.4.2 | Save File Text Field is now completely useless due to Replit!"),
                        ft.Text(
                            "1.4.3 | Remove Window Drag Area cus this is turning into a browser game"),
                        ft.Text(
                            "1.4.3.1 | I forgot to remove the quit button too"),
                        ft.Text(
                            "1.4.4 | Idk idk how to make desktop mode or something"),
                        ft.Text(
                            "1.4.5 | Made scientific notation disabled by default"),
                        ft.Text(
                            "1.4.6 | Made new upgrade + i didnt forgor buymax this time"),
                        ft.Text(
                            "1.5 | New upgrade, saves more data, includes buy max handle for new upgrade, and more "
                            "things i forgot!"),
                        ft.Text("1.5.1 | Updated debug messages"),
                        ft.Text("1.5.2 | Added console that almost worked"),
                        ft.Text("1.5.3 | Added console inside the app"),
                        ft.Text("1.6.1 | Metadata support + bug fixes (you couldn't load multiple plugins)"),
                        ft.Text("1.7 | i forgot to write the changelogs for 1.6.2 so shut up,"),
                        ft.Text("1.7 | in 1.7, i made a login screen and in 1.6.2 i made an advancements system so dont complain i didnt make a changelog for it"),
                        ft.Text("1.7.1 | stuff n more for login"),
                        ft.Text("1.7.2 | SIGNUP?????????? WOW NEVER EXPECTED!!!"),
                        ft.Text("1.7.3 | uhh yeah proper signup that works and yes now SHUTTTTTTTTTT"),
                        ft.Text("1.7.4 | placeholder is very attention catchy!!"),
                        ft.Text("1.7.5 | I completely forgot what i did in this update lmao"),
                        ft.Text("1.7.6 | Fix not being able to signup"),
                        ft.Text("1.7.7 | Fix not being able to signup again..."),
                        ft.Text("1.8 | Advancements + Documentation"),
                        ft.Text("1.8 | Please don't complain that I keep forgetting to bump the version!")
                        # ft.FletApp("http://localhost:8011")
                    ]
                )
            )
            page.views[1].scroll = ft.ScrollMode.ADAPTIVE
        elif page.route == "/console":
            page.views.append(ft.View(
                "/console", [
                    ft.AppBar(title=ft.Text("CommandIncremental | Console")),
                    ft.Row([consoleTextBox, ft.IconButton(ft.icons.START, on_click=handleConsoleCommand)])
                ]
            ))
        elif page.route == "/plugins":
            global plugins, pluginvers, pluginnames, plugindescs
            plugincol = ft.Column()
            for i in range(pluginnames.__len__()):
                plugincol.controls.append(
                    ft.Text(pluginnames[i], style=ft.TextThemeStyle.HEADLINE_MEDIUM))
                plugincol.controls.append(ft.Text(plugindescs[i], style=ft.TextThemeStyle.BODY_MEDIUM))
                plugincol.controls.append(ft.Text(pluginvers[i], style=ft.TextThemeStyle.LABEL_SMALL))
                plugincol.controls.append(ft.Divider(height=3, thickness=3))

            page.views.append(ft.View(
                "/plugins", [
                    ft.AppBar(title=ft.Text("CommandIncremental | Installed/Loaded Plugins")),
                    plugincol
                ]
            ))
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    # page.go("/")
    page.on_route_change = buildApp
    page.on_view_pop = view_pop
    if signed_up:
        page.go("/login")
        log.debug("[MainThread/PageGo => SignedUpChecker] Detected is signed up!")
    elif not signed_up:
        page.go("/signup")
        log.debug("[MainThread/PageGo => SignedUpChecker] Detected not signed up!")
    elif logged_in:
        page.go("/")
        log.debug("[MainThread/PageGo => SignedUpChecker] Detected logged in!")
    else:
        log.debug("[MainThread/PageGo => SignedUpChecker] Detected signed up is unknown!")

    global pluginwantstoaddpage, pluginwantstoaddpage_content, quitall
    while True:
        if quitall:
            quit()
        # global buymax
        # starttime = time.time()
        if notatecheckbox.value:
            notate = True
        else:
            notate = False
        if notate:
            siliconcounter.value = "{:e} {0} | ".format(
                silicon, displaysiliconunit) + str(
                "{:e.3f}".format(siliconperspec)) + f" {displaysiliconunit} per {silicongenwaittime} sec"
            buygen1button.text = "Buy Basic {0} Factory (" + "{:e}".format(
                gen1['amount'], displaysiliconunit2) + ") | Cost: {:e}§".format(gen1['cost'])
            moneydisplay.value = "{:e} {0} | ".format(money, displaymoneyunit) + str(
                "{:e.3f}".format(moneyperspec)) + f" {displaymoneyunit} per {silicongenwaittime} sec"
        else:
            siliconcounter.value = "{} {} | ".format(
                silicon, displaysiliconunit) + str(
                "{:.3f}".format(siliconperspec)) + f" {displaysiliconunit} per {silicongenwaittime} sec"
            buygen1button.text = "Buy Basic {} Factory (".format(displaysiliconunit2) + "{}".format(
                gen1['amount']) + ") | Cost: {}§".format(gen1['cost'])
            moneydisplay.value = "{0} {1} | ".format(money, displaymoneyunit) + str(
                "{:.3f}".format(moneyperspec)) + f" {displaymoneyunit} per {silicongenwaittime} sec"

        # fpscounter.value = "FPS: " + str(1.0 / (time.time() - starttime)) # raw clock speed fps # due to reasons
        page.update()
        # make the game capped at 12 fps (0.083333333333333328707 sec) # nvm its changable # also the default value
        # is now 0.0025
        time.sleep(updateinterval)
        if buymax is True:
            buygen1(None)
            handleUpgradeMax(None)
            handleUpgradeMultiplier(None)
            handleUpgradeGenWaitTime(None)
        if silicon > 1e+308:
            page.views[0].controls.append(overflowwarn[0])
            page.views[0].update()
            overflowwarn[2](None)
            # time.sleep(0.001)
            time.sleep(0.001)
            overflowwarn[3](None)
            time.sleep(1)
            page.views[0].controls.pop()
            time.sleep(0.25)
            page.window_close()
            quit()
        # print(f"[MainThread/PluginHelper => PrintPluginWantsToAddPage] {pluginwantstoaddpage} | {
        # pluginwantstoaddpage_content}")
        if pluginwantstoaddpage:
            page.views[0].controls.append(pluginwantstoaddpage_content)
            page.views[0].update()
            time.sleep(0.1)
            pluginwantstoaddpage = False
            log.debug("[MainThread/PluginHelper => AddContentToPage] Plugin wants to add page!")
        # page.client_storage.set("silicon", silicon)


def update():
    while True:
        global silicon, maxsilicon, console_setsiliconval, money
        if not silicon > 1e+308:
            if not silicon >= maxsilicon:
                # if not console_setsiliconval:
                silicon += siliconperspec * siliconmultiplier
                money += moneyperspec
                # else: silicon = console_setsiliconval console_setsiliconval = None # workaround cus console thread
                # can't set due to being in a different process; simulating it's own main enviroment no actually fuck
                # this
            else:
                #print(
                #    "[UpdateThread/Update] Cannot Add Silicon, Reached Maximum Bank Capacity")
                # SILENT
                pass
        else:
            log.warn(
                "[UpdateThread/Update => InvalidChecker] Silicon value is infinite, either you cheated, or you beat "
                "the game")
            quit()
        time.sleep(silicongenwaittime)


def interactableConsole():
    global silicon, consolepage
    try:
        while True:
            print(f"Console | [{consolepage}]")
            page_action = input(":")
            if page_action.startswith("switchpage "):
                switchpage = page_action[11:]
                # print(switchpage)
                if switchpage == "main":
                    log.debug("[Console/Main => SwitchPage] Switched page to Main")
                    consolepage = "main"
            elif page_action.startswith("set-silicon ") and consolepage == "main":
                setsilicon = float(page_action[12:])
                # console_setsiliconval = setsilicon
                silicon = setsilicon
            elif page_action == "get-silicon":
                log.info(
                    f"[Console/Main => GetSilicon] Current Silicon Count: {silicon}")
            elif page_action == "kill":
                log.error(
                    "[Console/Main => KillWindow] Killing all..."
                )
                if os.name == "nt":
                    os.system("taskkill /f /im python.exe")
                    os.system("taskkill /f /im python3.exe")

                else:
                    os.system("killall python3")
                    os.system("pkill python3")

    except Exception as e:
        log.error(f"ERROR: {e}")
        input()
    silicon = 0


if __name__ == "__main__":
    try: keyboard.add_hotkey("q", quitAll)
    except Exception: log.error("[ParentThread => Imports] couldn't import keyboard, assuming not rooted on linux!")
    updateThread = Thread(target=update)
    updateThread.start()
    loadPlugins()
    # if os.name == "nt":
    #     os.system("python .\console.py")
    # else:
    #     os.system("python3 ./console.py")
    # consoleThread = Thread(target=interactableConsole)
    # consoleThread.start()
    # appThread = Thread(target=lambda: ft.app(target=main, port=8000, view=ft.WEB_BROWSER))
    # appThread.start()
    if os.name == "posix":
        ft.app(target=main, port=8000, view=ft.FLET_APP, route_url_strategy="path", assets_dir="assets")
    else:
        ft.app(target=main, port=8000, view=ft.WEB_BROWSER, route_url_strategy="path", assets_dir="assets")
