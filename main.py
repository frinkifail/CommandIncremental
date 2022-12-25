try:
    from replit import db
except ImportError:
    print("[debug/libraries] unable to import database from replit, assuming running custom server")
import flet as ft
from threading import Thread
import time
# import math
import json
import notificationFlet as ftn
import os

silicon: float = 0
siliconperspec: float = 0.108
maxsilicon: float = 100
maxsiliconcost = 75
siliconmultiplier: float = 1
siliconmultipliercost = 165
gen1 = {
    "cost": 10,
    "growth": 1.28,
    "amount": 0
}
buymax = False
saveenabled = True
updateinterval = 0.0025
version: str = "1.4.6"  # forgor to bump version
# Other shit used in main function
debugsiliconnotiinuse = False
notate = True
legacymodebool = False
silicongenwaittime = 0.1

def main(page: ft.Page):
    global buymax
    page.title = "CommandIncremental"
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = "adaptive"
    page.window_frameless = True
    page.window_maximizable = False
    page.window_width = 800
    page.window_height = 600
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
            print("[gen/1] bought!")
        else:
            print("[gen/1] not enough silicon")

    def handleNewSave(e):
        if saveenabled:
            db["silicon"] = silicon
            db["siliconperspec"] = siliconperspec
            db["gen1"] = gen1
            db["maxsilicon"] = {"max": maxsilicon, "cost": maxsiliconcost}
            print('[save/new] saved!')
        else:
            print('[save/new] cannot save: disabled')

    def handleNewLoad(e):
        global silicon, siliconperspec, gen1, maxsilicon, maxsiliconcost
        if saveenabled:
            silicon = db["silicon"]
            siliconperspec = db["siliconperspec"]
            gen1 = db["gen1"]
            maxsilicon = db["maxsilicon"]["max"]
            maxsiliconcost = db["maxsilicon"]["cost"]
            print('[save/new] loaded!')
        else:
            print('[save/new] cannot load: disabled')

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
                print(f"[debug] set silicon to {0}".format(
                    int(debugsilicontf.value)))
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
                        "[debug/noti] notification currently in use; will not continue until finished")
            else:
                print(
                    "[debug] will not set silicon; debug silicon text field is invalid")
            saveenabled = False
            print("[save/debug] save has been disabled due to enabling debug mode!")
        except Exception:  # ugh it doesn't catch because threads fucking suck
            print("[debug/noti] wow, thats funny, see, the user switched views before i could remove the notification, in conclusion, fuck you")

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
        print("[debug/updateinterval] successfully updated update interval!")

    def handleUpgradeMax(e):
        global maxsilicon, maxsiliconcost, silicon
        if silicon >= maxsiliconcost:
            silicon -= maxsiliconcost
            maxsiliconcost *= 1.41
            maxsilicon *= 1.38
            # ahhhh im so stupid
            upgrades_max.text = f"Max Silicon [{maxsilicon}] | Cost: [{maxsiliconcost}]"
            print("[main/upgrades] bank size upgraded")
        else:
            print("[main/upgrades] not enough silicon!")
            
    def handleUpgradeMultiplier(e):
        global silicon, siliconmultipliercost, siliconmultiplier
        if silicon >= siliconmultipliercost:
            silicon -= siliconmultipliercost
            siliconmultipliercost *= 1.69
            siliconmultiplier += 1.5
            upgrades_siliconmultiplier.text = f"Silicon Multiplier [{siliconmultiplier}] | Cost: [{siliconmultipliercost}]"
            print("[main/upgrades] multiplier upgraded")
        else:
            print("[main/upgrades] not enough silicon!")

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
    upgrades_max = ft.ElevatedButton(
        f"Max Silicon [{maxsilicon}] | Cost: [{maxsiliconcost}]", on_click=handleUpgradeMax, tooltip="Upgrade bank size")
    upgrades_siliconmultiplier = ft.ElevatedButton(f"Silicon Multiplier [{siliconmultiplier}] | Cost: [{siliconmultipliercost}]", on_click=handleUpgradeMultiplier, tooltip=f"Gain more silicon per {silicongenwaittime} seconds")
    legacymode = ft.Checkbox(label="Desktop Mode", on_change=handleLegacyMode)
    windowdragarea = ft.WindowDragArea(ft.Container(ft.Text("Drag the window!", tooltip="you can drag the window here"),
                                       padding=10, alignment=ft.alignment.center, tooltip="drag the window here"), tooltip="lets you drag the window")
    loadbutton = ft.ElevatedButton(
        "Load", on_click=handleNewLoad, tooltip="loads the game according to your save id")
    savebutton = ft.ElevatedButton(
        "Save", on_click=handleNewSave, tooltip="saves the game according to your save id")

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
                        ft.icons.UPGRADE, on_click=lambda _: page.go("/upgrades"), tooltip="Upgrades"), ft.IconButton(ft.icons.BUG_REPORT, on_click=lambda _: page.go("/debug"), tooltip="Some debug utilities")]),
                    # used to be window drag area,
                    # windowdragarea if os.name == "nt" or os.name == "posix" else None,
                    siliconcounter, buygen1button,
                    buymaxbtn,
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
                            upgrades_siliconmultiplier
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
                        ft.Text("1.4.4 | Idk idk how to make desktop mode or something"),
                        ft.Text("1.4.5 | Made scientific notation disabled by default"),
                        ft.Text("1.4.6 | Made new upgrade + i didnt forgor buymax this time")
                    ]
                )
            )
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    # page.go("/")
    page.on_route_change = buildApp
    page.on_view_pop = view_pop
    page.go(page.route)

    while True:
        # global buymax
        # starttime = time.time()
        if notatecheckbox.value:
            notate = True
        else:
            notate = False
        if notate:
            siliconcounter.value = "{:e} silicon | ".format(
                silicon)+str("{:.3f}".format(siliconperspec))+f" silicon per {silicongenwaittime} sec"
            buygen1button.text = "Buy Basic Silicon Factory ("+"{:e}".format(
                gen1['amount'])+") | Cost: {:e}$".format(gen1['cost'])
        else:
            siliconcounter.value = "{} silicon | ".format(
                silicon)+str("{:.3f}".format(siliconperspec))+f" silicon per {silicongenwaittime} sec"
            buygen1button.text = "Buy Basic Silicon Factory ("+"{}".format(
                gen1['amount'])+") | Cost: {}$".format(gen1['cost'])

        # fpscounter.value = "FPS: " + str(1.0 / (time.time() - starttime)) # raw clock speed fps # due to reasons
        page.update()
        # make the game capped at 12 fps (0.083333333333333328707 sec) # nvm its changable # also the default value is now 0.0025
        time.sleep(updateinterval)
        if buymax is True:
            buygen1(None)
            handleUpgradeMax(None)
            handleUpgradeMultiplier(None)
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


def update():
    while True:
        global silicon
        if not silicon > 1e+308:
            if not silicon >= maxsilicon:
                silicon += siliconperspec*siliconmultiplier
            else:
                print("[main/silicon] cannot continue, silicon reached max")
        else:
            print("[debug] invalid silicon value, exiting...")
            quit()
        time.sleep(0.1)


if __name__ == "__main__":
    updateThread = Thread(target=update)
    updateThread.start()
    ft.app(target=main, port=8000, view=ft.WEB_BROWSER)
