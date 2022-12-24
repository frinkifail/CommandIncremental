import flet as ft
from threading import Thread
import time
# import math
import json
import notificationFlet as ftn

silicon: float = 0
siliconperspec: float = 0.108
maxsilicon: float = 100
maxsiliconcost = 75
gen1 = {
    "cost": 10,
    "growth": 1.28,
    "amount": 0
}
buymax = False
saveenabled = True
updateinterval = 0.0025
version: str = "1.2.9" # forgor to bump version
# Other shit used in main function
debugsiliconnotiinuse = False
notate = True

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
        
    def handleSave(e):
        if saveenabled:
            savefile = open("saves/"+savefiletf.value+"/save.json", mode="r+")
            savefile.write("{\"silicon\": %s, \"siliconperspec\": %s, \"gen1\": %s}" % (silicon, siliconperspec, gen1))
            print("[save] saved!")
        else:
            print("[save] failed to save: save is disabled")
    def handleLoad(e):
        global silicon
        if saveenabled:
            savefile = open("saves/"+savefiletf.value+"/save.json", mode="r+")
            contents = json.load(savefile)
            silicon = contents["silicon"]
            print("[save] loaded!")
        else:
            print("[save] failed to load: save is disabled")
    def handleDebugPts(e):
        global silicon, saveenabled, debugsiliconnotiinuse
        try:
            if debugsilicontf.value != '':
                silicon = int(debugsilicontf.value)
                print(f"[debug] set silicon to {0}".format(int(debugsilicontf.value)))
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
                    print("[debug/noti] notification currently in use; will not continue until finished")
            else:
                print("[debug] will not set silicon; debug silicon text field is invalid")
            saveenabled = False
            print("[save/debug] save has been disabled due to enabling debug mode!")
        except Exception: # ugh it doesn't catch because threads fucking suck
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
        silicon = 1e+306 # ._.
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
            upgrades_max.text = f"Max Silicon [{maxsilicon}] | Cost: [{maxsiliconcost}]" # ahhhh im so stupid
            print("[main/upgrades] bank size upgraded")
        else:
            print("[main/upgrades] not enough silicon!")
        # page.views[1].update() # no idea how to make this work lmfao # faulty line 😡
    fpscounter = ft.Text("FPS: [DISABLED]")
    buymaxbtn = ft.TextButton(f"Buy Max: {buymax}", on_click=handleBuyMax, tooltip="buy factories until you're outta silicons")
    # page.add(buymaxbtn)
    siliconcounter = ft.Text(str(silicon)+" silicon", tooltip="silicon counter yuh")
    buygen1button = ft.ElevatedButton(f"Buy Basic anferiog i fucking forgor ({gen1['amount']}) | Cost: {gen1['cost']}$", on_click=buygen1, tooltip="buy them **basic** generators")
    # page.add(fpscounter, siliconcounter, buygen1button)
    savefiletf = ft.TextField(label="Save ID", tooltip="enter your save id here")
    debugsilicontf = ft.TextField(label="Set Silicons", tooltip="set your silicon to specific value (debugging purposes + saving will be disabled)")
    updateintervaltf = ft.TextField(label="Update Interval", shift_enter=True, on_submit=handleUpdateInterval, width=200, tooltip="sets your update interval (doesn't make you generate silicon faster ._.)")
    overflowwarn = ftn.createNoti(None, "Warning!", "Silicons are overflowing! Update thread has stopped!")
    debugsiliconnoti = ftn.createNoti(None, "Debug", "Changed silicon amount!")
    notatecheckbox = ft.Checkbox(label="Scientific Notation")
    notatecheckbox.value = True
    upgrades_max = ft.ElevatedButton(f"Max Silicon [{maxsilicon}] | Cost: [{maxsiliconcost}]", on_click=handleUpgradeMax, tooltip="Upgrade bank size")
    # notatecheckbox.value
    # page.add(ft.Row([ft.ElevatedButton("Save", on_click=handleSave), ft.ElevatedButton("Load", on_click=handleLoad), savefiletf]))
    # page.add(ft.Row([debugsilicontf, ft.IconButton(ft.icons.CHECK, on_click=handleDebugPts)]))
    
    def buildApp(approute):
        page.views.clear()
        # if page.route == "/":
        page.views.append(
            ft.View(
                "/", [
                    ft.AppBar(title=ft.Text(f"CommandIncremental {version}", tooltip="the game"), center_title=True, actions=[ft.IconButton(ft.icons.SETTINGS, on_click=lambda _: page.go("/settings"), tooltip="Settings"), ft.IconButton(ft.icons.UPGRADE, on_click=lambda _: page.go("/upgrades"), tooltip="Upgrades"), ft.IconButton(ft.icons.BUG_REPORT, on_click=lambda _: page.go("/debug"), tooltip="Some debug utilities"), ft.IconButton(ft.icons.CLOSE, on_click=lambda _: page.window_close(), icon_color=ft.colors.RED, tooltip="Quit Game")]),
                    ft.WindowDragArea(ft.Container(ft.Text("Drag the window!", tooltip="you can drag the window here"), padding=10, alignment=ft.alignment.center, tooltip="drag the window here"), tooltip="lets you drag the window"),
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
                        ft.Text("Hello World!", tooltip="Testing Page | Why are you here?")
                    ]
                )
            )
        elif page.route == "/settings":
            page.views.append(
                ft.View(
                    "/settings", [
                        ft.AppBar(title=ft.Text("CommandIncremental | Settings")),
                        updateintervaltf,
                        ft.Row([
                            ft.ElevatedButton("Save", on_click=handleSave, tooltip="saves the game according to your save id"),
                            ft.ElevatedButton("Load", on_click=handleLoad, tooltip="loads the game according to your save id"),
                            savefiletf
                        ]),
                        notatecheckbox
                        # ft.TextButton("Infinite Silicon", on_click=handleInfSilicon, tooltip="crashes the game") # tooltip used to be "gives you infinite silicon (for debugging purposes + saving *will* be disabled)"
                    ]
                )
            )
        elif page.route == "/upgrades":
            page.views.append(
                ft.View(
                    "/upgrades", [
                        ft.AppBar(title=ft.Text("CommandIncremental | Upgrades")),
                        ft.Column([
                            ft.Divider(height=3, thickness=3),
                            upgrades_max
                        ])
                    ]
                )
            )
        elif page.route == "/debug":
            page.views.append(
                ft.View(
                    "/debug", [
                        ft.AppBar(title=ft.Text("CommandIncremental | Debug Utilities")),
                        ft.Row([debugsilicontf, ft.IconButton(ft.icons.CHECK, on_click=handleDebugPts)]),
                        ft.TextButton("Infinite Silicon", on_click=handleInfSilicon, tooltip="gives you basically infinite silicon (for debugging purposes + saving *will* be disabled)"),
                        ft.Text("Changelog:", style=ft.TextThemeStyle.HEADLINE_MEDIUM),
                        ft.Text("1.2.7 | Added changelog to track stuff"),
                        ft.Text("1.2.7.1 | Minor spelling mistake *earth collapsing*"),
                        ft.Text("1.2.7.2 | Fixed debug silicon notification not showing"),
                        ft.Text("1.2.7.3 | Ok, the notification is slow, but it works alright?"),
                        ft.Text("1.2.7.4 | Forgot to make the buymax buy the upgrade :skull:"),
                        ft.Text("1.2.7.5 | ong it crashes; i fixed it"),
                        ft.Text("1.2.8 | Made scientific notation optional"),
                        ft.Text("1.2.9 | Upgrade Max actually works now")
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
            siliconcounter.value = "{:e} silicon | ".format(silicon)+str("{:.3f}".format(siliconperspec))+" silicon per 0.1 sec"
            buygen1button.text = "Buy Basic Silicon Factory ("+"{:e}".format(gen1['amount'])+") | Cost: {:e}$".format(gen1['cost'])
        else:
            siliconcounter.value = "{} silicon | ".format(silicon)+str("{:.3f}".format(siliconperspec))+" silicon per 0.1 sec"
            buygen1button.text = "Buy Basic Silicon Factory ("+"{}".format(gen1['amount'])+") | Cost: {}$".format(gen1['cost'])
        
        # fpscounter.value = "FPS: " + str(1.0 / (time.time() - starttime)) # raw clock speed fps # due to reasons
        page.update()
        time.sleep(updateinterval) # make the game capped at 12 fps (0.083333333333333328707 sec) # nvm its changable # also the default value is now 0.0025
        if buymax is True:
            buygen1(None)
            handleUpgradeMax(None)
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
                silicon += siliconperspec
            else:
                print("[main/silicon] cannot continue, silicon reached max")
        else:
            print("[debug] invalid silicon value, exiting...")
            quit()
        time.sleep(0.1)

if __name__ == "__main__":
    updateThread = Thread(target=update)
    updateThread.start()
    ft.app(target=main, port=8000)
