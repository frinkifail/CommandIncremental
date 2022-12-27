import os
import sys
import notificationFlet as ftn
import json
import time
from threading import Thread
import flet as ft
import math
print("[ParentThread/Main => Parent] Server Started!")
try:
    from replit import db
except ImportError:
    print("[ParentThread => Imports] unable to import database from replit, assuming running custom server")
# import math

sys.path.append("plugins/API")
import bindings
from typing import *

silicon: float = 10
siliconperspec: float = 0.108
maxsilicon: float = 15
maxsiliconcost = 10
siliconmultiplier: float = 1
siliconmultipliercost = 365
displaysiliconunit = bindings.displayunit
displaysiliconunit2 = bindings.displayunit2
gen1 = {
    "cost": 10,
    "growth": 1.28,
    "amount": 0
}
buymax = False
saveenabled = True
updateinterval = 0.0025
version: str = "1.6"  # forgor to bump version
# Other shit used in main function
debugsiliconnotiinuse = False
notate = True
legacymodebool = False
silicongenwaittime = 0.8
silicongenwaittimecost = 550
consolepage = "main"
console_setsiliconval = None
console_lastcmd = ""
pluginscriptfiles = []
pluginwantstoaddpage = False
pluginwantstoaddpage_content = None

def setSilicon(count: float):
    global silicon
    print(f"[ParentThread/PluginHelper => SetSilicon] Old Silicon Count: {silicon}")
    silicon = count
    print("[ParentThread/PluginHelper => SetSilicon] Set silicon done!")
    print(f"[ParentThread/PluginHelper => SetSilicon] New Silicon Count: {silicon}")
    
def addToPage(content):
    global pluginwantstoaddpage_content, pluginwantstoaddpage
    pluginwantstoaddpage = True
    pluginwantstoaddpage_content = content
    print(f"[ParentThread/PluginHelper => AddContentToPage] Added {content}!")

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
    plugins = os.listdir(".")
    # plugins = oldplugins.remove("API")
    plugins.remove("API")
    scriptfiles = []
    # print(["Hi", "API"].remove("API"))
    print("[ParentThread/PluginLoader => PluginChecker] Available plugins: "+str(plugins))
    for i in range(plugins.__len__()):
        os.chdir(plugins[i])
        if os.path.exists("scripts"):
            global pluginscriptfiles
            os.chdir("scripts")
            # pluginscriptfiles = []
            pluginscriptfiles = os.listdir(".")
            executePlugins()

def main(page: ft.Page):
    global buymax
    page.title = "CommandIncremental"
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = "adaptive"
    page.window_frameless = True
    page.window_maximizable = False
    page.window_width = 800
    page.window_height = 600
    page.tooltip = ft.Tooltip(gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.Alignment(0.8, 1),
                colors=[
                    "0xff1f005c",
                    "0xff5b0060",
                    "0xff870160",
                    "0xffac255e",
                    "0xffca485c",
                    "0xffe16b5c",
                    "0xfff39060",
                    "0xffffb56b",
                ]))
    # Other Variables
    # debugsiliconnotiinuse = False
    # fuckerinas it doesn't work!
    # buymax = False

    def buygen1(e):
        global silicon, gen1, siliconperspec
        if silicon >= gen1["cost"]:
            silicon -= gen1["cost"]
            gen1["cost"] *= gen1["growth"]
            gen1["amount"] += 1
            siliconperspec += 0.18
            print("[MainThread/Generators => 1] bought!")
        else:
            print("[MainThread/Generators => 1] not enough silicon")

    def handleNewSave(e):
        if saveenabled:
            db["silicon"] = silicon
            db["siliconperspec"] = siliconperspec
            db["gen1"] = gen1
            db["maxsilicon"] = {"max": maxsilicon, "cost": maxsiliconcost}
            db["silicongwt"] = silicongenwaittime
            db["silicongwt_c"] = silicongenwaittimecost
            db["siliconmul"] = siliconmultiplier
            db["siliconmul_c"] = siliconmultipliercost
            print('[MainThread/Handler => Save] Statistics Saved!')
        else:
            print(
                '[MainThread/Handler => Save] Failed to save: Saving/Loading is disabled')

    def handleNewLoad(e):
        global silicon, siliconperspec, gen1, maxsilicon, maxsiliconcost, silicongenwaittime, silicongenwaittimecost, siliconmultiplier, siliconmultipliercost
        if saveenabled:
            silicon = db["silicon"]
            siliconperspec = db["siliconperspec"]
            gen1 = db["gen1"]
            maxsilicon = db["maxsilicon"]["max"]
            maxsiliconcost = db["maxsilicon"]["cost"]
            silicongenwaittime = db["silicongwt"]
            silicongenwaittimecost = db["silicongwt_c"]
            siliconmultiplier = db["siliconmul"]
            siliconmultipliercost = db["siliconmul_c"]
            print('[MainThread/Handler => Load] Statistics Loaded!')
        else:
            print(
                '[MainThread/Handler => Load] Failed to load: Saving/Loading is disabled')

    def handleSave(e):
        if saveenabled:
            try:
                savefile = open("saves/"+savefiletf.value +
                                "/save.json", mode="r+")
            except:
                try:
                    os.mkdir("saves/"+savefiletf.value)
                    newsavefile = open(
                        "saves/"+savefiletf.value+"/save.json", mode='x')
                    newsavefile.close()
                    savefile = open("saves/"+savefiletf.value +
                                    "/save.json", mode="r+")
                except Exception as e:
                    print(f"[save] failed to save: {e}")
            savefile.truncate(0)
            savefile.write("{\"silicon\": %s, \"siliconperspec\": %s, \"gen1\": {\"cost\": %s, \"amount\": %s}, \"maxsilicon\": %s, \"maxsilicon_cost\": %s}" % (
                silicon, siliconperspec, gen1["cost"], gen1["amount"], maxsilicon, maxsiliconcost))
            print("[save] saved!")
        else:
            print("[save] failed to save: save is disabled")

    def handleLoad(e):
        global silicon, siliconperspec, gen1, maxsilicon, maxsiliconcost
        if saveenabled:
            savefile = open("saves/"+savefiletf.value+"/save.json", mode="r+")
            contents = json.load(savefile)
            silicon = contents["silicon"]
            siliconperspec = contents["siliconperspec"]
            gen1.update(
                {"cost": contents["gen1"]["cost"], "amount": contents["gen1"]["amount"]})
            print("[save] loaded!")
        else:
            print("[save] failed to load: save is disabled")

    def handleDebugPts(e):
        global silicon, saveenabled, debugsiliconnotiinuse
        try:
            if debugsilicontf.value != '':
                silicon = int(debugsilicontf.value)
                print(
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
                    print(
                        "[MainThread/Debug => Notifications] Notification Animation is playing, won't play overlapping animation")
            else:
                print(
                    "[MainThread/Debug => SetSilicon] Set Silicon Text Field's value is invalid, won't set to that...")
            saveenabled = False
            print(
                "[MainThread/Handler => SaveHandle] Disabled saving, debug silicon handle is called")
        except Exception:  # ugh it doesn't catch because threads fucking suck
            print("[MainThread/Debug => Notification] wow, thats funny, see, the user switched views before i could remove the notification, in conclusion, fuck you")

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
        print("[MainThread/Handler => Updater] Changed update interval!")

    def handleUpgradeMax(e):
        global maxsilicon, maxsiliconcost, silicon
        if silicon >= maxsiliconcost:
            silicon -= maxsiliconcost
            maxsiliconcost *= 1.41
            maxsilicon *= 1.38
            # ahhhh im so stupid
            upgrades_max.text = f"Max Silicon [{maxsilicon}] | Cost: [{maxsiliconcost}]"
            print("[MainThread/Upgrades => MaxSilicon] Upgraded this upgrade!")
        else:
            print(
                "[MainThread/Upgrades => MaxSilicon] Not enough silicon to upgrade this!")

    def handleUpgradeMultiplier(e):
        global silicon, siliconmultipliercost, siliconmultiplier
        if silicon >= siliconmultipliercost:
            silicon -= siliconmultipliercost
            siliconmultipliercost *= 1.69
            siliconmultiplier += 1.5
            upgrades_siliconmultiplier.text = f"Silicon Multiplier [{siliconmultiplier}] | Cost: [{siliconmultipliercost}]"
            upgrades_siliconmultiplier.tooltip = f"Gain more silicon per {silicongenwaittime} seconds"
            print("[MainThread/Upgrades => Multiplier] Upgraded this upgrade!")
        else:
            print(
                "[MainThread/Upgrades => Multiplier] Not enough silicon to upgrade this!")

    def handleUpgradeGenWaitTime(e):
        global silicon, silicongenwaittime, silicongenwaittimecost
        if silicongenwaittime > 0.02:
            if silicon >= silicongenwaittimecost:
                silicon -= silicongenwaittimecost
                silicongenwaittimecost *= 1.80
                silicongenwaittime -= 0.01
                upgrades_waittime.text = f"Generation Time [{silicongenwaittime}] | Cost: [{silicongenwaittimecost}]"
                print("[MainThread/Upgrades => WaitTime] Upgraded this upgrade!")
            else:
                print(
                    "[MainThread/Upgrades => WaitTime] Not enough silicon to upgrade this!")
        else:
            print("[MainThread/Upgrades => WaitTime] Reached Max Upgrade!")

    def handleDarkThemeChange(e):
        if darktheme.value:
            page.theme_mode = ft.ThemeMode.DARK
        else:
            page.theme_mode = ft.ThemeMode.LIGHT

    # fuck this idk how to make it work # ok, maybe i know how it works, but im just too lazy
    def handleLegacyMode(e):
        global legacymodebool
        if legacymode.value:
            page.views[0].appbar = ft.AppBar(title=ft.Text(f"CommandIncremental Legacy {version}", tooltip="the game but desktop"), center_title=True, actions=[ft.IconButton(ft.icons.SETTINGS, on_click=lambda _: page.go("/settings"), tooltip="Settings"), ft.IconButton(
                ft.icons.UPGRADE, on_click=lambda _: page.go("/upgrades"), tooltip="Upgrades"), ft.IconButton(ft.icons.BUG_REPORT, on_click=lambda _: page.go("/debug"), tooltip="Some debug utilities"), ft.IconButton(ft.icons.CLOSE, icon_color=ft.colors.RED, on_click=lambda _: page.window_close())])
            page.views[0].controls.append(windowdragarea)
            page.views[0].update()
            legacymodebool = True
        else:
            page.views[0].appbar = ft.AppBar(title=ft.Text(f"CommandIncremental Web {version}", tooltip="the game"), center_title=True, actions=[ft.IconButton(ft.icons.SETTINGS, on_click=lambda _: page.go(
                "/settings"), tooltip="Settings"), ft.IconButton(ft.icons.UPGRADE, on_click=lambda _: page.go("/upgrades"), tooltip="Upgrades"), ft.IconButton(ft.icons.BUG_REPORT, on_click=lambda _: page.go("/debug"), tooltip="Some debug utilities")])
            page.views[0].controls.remove(windowdragarea)
            page.views[0].update()
            legacymodebool = False

    def handleManualBoost(e):
        global silicon, siliconmultiplier, siliconperspec
        silicon += siliconperspec*siliconmultiplier
        
    def view1add(content):
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
        elif ctbv == "get-silicon" or ctbv == "gs":
            page.views[1].controls.append(ft.Text(f"[Main/Console => GetSilicon] Silicon Count Is: {silicon}"))
            page.views[1].update()
            console_lastcmd = ctbv
        elif ctbv == "lastcmd" or ctbv == "" or ctbv == "lc":
            #
            # consoleTextBox.value = ""
            # ctbv = console_lastcmd
            # ctbv = cmd
            handleConsoleCommand(None, console_lastcmd) # idk why "" doesn't work :skull:
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
    fpscounter = ft.Text("FPS: [DISABLED]")
    buymaxbtn = ft.TextButton(
        f"Buy Max: {buymax}", on_click=handleBuyMax, tooltip="buy factories until you're outta silicons")
    # page.add(buymaxbtn)
    siliconcounter = ft.Text(str(silicon)+" silicon",
                             tooltip="silicon counter yuh")
    buygen1button = ft.ElevatedButton(
        f"Buy Basic anferiog i fucking forgor ({gen1['amount']}) | Cost: {gen1['cost']}$", on_click=buygen1, tooltip="buy them **basic** generators")
    # page.add(fpscounter, siliconcounter, buygen1button)
    savefiletf = ft.TextField(
        label="Save ID", tooltip="enter your save id here")
    debugsilicontf = ft.TextField(
        label="Set Silicons", tooltip="set your silicon to specific value (debugging purposes + saving will be disabled)")
    updateintervaltf = ft.TextField(label="Update Interval", shift_enter=True, on_submit=handleUpdateInterval,
                                    width=200, tooltip="sets your update interval (doesn't make you generate silicon faster ._.)")
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
    # END GAME UTILS
    legacymode = ft.Checkbox(label="Desktop Mode", on_change=handleLegacyMode)
    windowdragarea = ft.WindowDragArea(ft.Container(ft.Text("Drag the window!", tooltip="you can drag the window here"),
                                       padding=10, alignment=ft.alignment.center, tooltip="drag the window here"), tooltip="lets you drag the window")
    loadbutton = ft.ElevatedButton(
        "Load", on_click=handleNewLoad, tooltip="loads the game according to your save id")
    savebutton = ft.ElevatedButton(
        "Save", on_click=handleNewSave, tooltip="saves the game according to your save id")

    consoleTextBox = ft.TextField(label="Insert Command", shift_enter=True, on_submit=handleConsoleCommand)

    # notatecheckbox.value
    # page.add(ft.Row([ft.ElevatedButton("Save", on_click=handleSave), ft.ElevatedButton("Load", on_click=handleLoad), savefiletf]))
    # page.add(ft.Row([debugsilicontf, ft.IconButton(ft.icons.CHECK, on_click=handleDebugPts)]))

    def buildApp(approute):
        page.views.clear()
        # if page.route == "/":
        page.views.append(
            ft.View(
                "/", [
                    ft.AppBar(title=ft.Text(f"CommandIncremental {version}", tooltip="the game"), center_title=True, actions=[ft.IconButton(ft.icons.SETTINGS, on_click=lambda _: page.go("/settings"), tooltip="Settings"), ft.IconButton(
                        ft.icons.UPGRADE, on_click=lambda _: page.go("/upgrades"), tooltip="Upgrades"), ft.IconButton(ft.icons.BUG_REPORT, on_click=lambda _: page.go("/debug"), tooltip="Some debug utilities"), ft.IconButton(ft.icons.CODE, on_click=lambda _: page.go("/console"), tooltip="In-app Console")]),
                    # used to be window drag area,
                    # windowdragarea if os.name == "nt" or os.name == "posix" else None,
                    siliconcounter, buygen1button,
                    buymaxbtn,
                    manualboost
                    # ft.ElevatedButton("Goto Test", on_click=lambda _: page.go("/test"))

                ]
            )
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
                        # legacymode
                        # ft.TextButton("Infinite Silicon", on_click=handleInfSilicon, tooltip="crashes the game") # tooltip used to be "gives you infinite silicon (for debugging purposes + saving *will* be disabled)" # i moved it
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
        elif page.route == "/debug":
            page.views.append(
                ft.View(
                    "/debug", [
                        ft.AppBar(title=ft.Text(
                            "CommandIncremental | Debug Utilities")),
                        ft.Row([debugsilicontf, ft.IconButton(
                            ft.icons.CHECK, on_click=handleDebugPts)]),
                        ft.TextButton("Infinite Silicon", on_click=handleInfSilicon,
                                      tooltip="gives you basically infinite silicon (for debugging purposes + saving *will* be disabled)"),
                        ft.Text("Changelog:",
                                style=ft.TextThemeStyle.HEADLINE_MEDIUM),
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
                            "1.5 | New upgrade, saves more data, includes buy max handle for new upgrade, and more things i forgot!"),
                        ft.Text("1.5.1 | Updated debug messages"),
                        ft.Text("1.5.2 | Added console that almost worked"),
                        ft.Text("1.5.3 | Added console inside the app"),
                        ft.Text("1.6 | Kinda plugin support or smth idk")
                    ]
                )
            )
        elif page.route == "/console":
            page.views.append(ft.View(
                "/console", [
                    ft.AppBar(title=ft.Text("CommandIncremental | Console")),
                    ft.Row([consoleTextBox, ft.IconButton(ft.icons.START, on_click=handleConsoleCommand)])
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
    page.go(page.route)

    global pluginwantstoaddpage, pluginwantstoaddpage_content
    while True:
        # global buymax
        # starttime = time.time()
        if notatecheckbox.value:
            notate = True
        else:
            notate = False
        if notate:
            siliconcounter.value = "{:e} {0} | ".format(
                silicon, displaysiliconunit)+str("{:.3f}".format(siliconperspec))+f" {displaysiliconunit} per {silicongenwaittime} sec"
            buygen1button.text = "Buy Basic {0} Factory ("+"{:e}".format(
                gen1['amount'], displaysiliconunit2)+") | Cost: {:e}$".format(gen1['cost'])
        else:
            siliconcounter.value = "{} {} | ".format(
                silicon, displaysiliconunit)+str("{:.3f}".format(siliconperspec))+f" {displaysiliconunit} per {silicongenwaittime} sec"
            buygen1button.text = "Buy Basic {} Factory (".format(displaysiliconunit2)+"{}".format(
                gen1['amount'])+") | Cost: {}$".format(gen1['cost'])

        # fpscounter.value = "FPS: " + str(1.0 / (time.time() - starttime)) # raw clock speed fps # due to reasons
        page.update()
        # make the game capped at 12 fps (0.083333333333333328707 sec) # nvm its changable # also the default value is now 0.0025
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
        # print(f"[MainThread/PluginHelper => PrintPluginWantsToAddPage] {pluginwantstoaddpage} | {pluginwantstoaddpage_content}")
        if pluginwantstoaddpage:
            page.views[0].controls.append(pluginwantstoaddpage_content)
            page.views[0].update()
            time.sleep(0.1)
            pluginwantstoaddpage = False
            print("[MainThread/PluginHelper => AddContentToPage] Plugin wants to add page!")


def update():
    while True:
        global silicon, maxsilicon, console_setsiliconval
        if not silicon > 1e+308:
            if not silicon >= maxsilicon:
                # if not console_setsiliconval:
                silicon += siliconperspec*siliconmultiplier
                # else:
                    # silicon = console_setsiliconval
                    # console_setsiliconval = None # workaround cus console thread can't set due to being in a different process; simulating it's own main enviroment
                # no actually fuck this
            else:
                print(
                    "[UpdateThread/Update] Cannot Add Silicon, Reached Maximum Bank Capacity")
        else:
            print("[UpdateThread/Update => InvalidChecker] Silicon value is infinite, either you cheated, or you beat the game")
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
                    print("[Console/Main => SwitchPage] Switched page to Main")
                    consolepage = "main"
            elif page_action.startswith("set-silicon ") and consolepage == "main":
                setsilicon = float(page_action[12:])
                # console_setsiliconval = setsilicon
                silicon = setsilicon
            elif page_action == "get-silicon":
                print(
                    f"[Console/Main => GetSilicon] Current Silicon Count: {silicon}")
            elif page_action == "kill":
                print(
                    "[Console/Main => KillWindow] Killing all..."
                )
                if os.name == "nt":
                    os.system("taskkill /f /im python.exe")
                    os.system("taskkill /f /im python3.exe")
                    
                else:
                    os.system("killall python3")
                    os.system("pkill python3")

    except Exception as e:
        print(f"ERROR: {e}")
        input()


if __name__ == "__main__":
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
    ft.app(target=main, port=8000, view=ft.WEB_BROWSER, route_url_strategy="path")
