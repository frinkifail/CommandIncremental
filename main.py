import flet as ft
from threading import Thread
import time
import math
import json

points: float = 0
pointsperspec: float = 0.108
gen1 = {
    "cost": 10,
    "growth": 1.28,
    "amount": 0
}
buymax = False
saveenabled = True

def main(page: ft.Page):
    global buymax
    # buymax = False
    def buygen1(e):
        global points, gen1, pointsperspec
        if points >= gen1["cost"]:
            points -= gen1["cost"]
            gen1["cost"] *= gen1["growth"]
            gen1["amount"] += 1
            pointsperspec += 0.18
            print("[gen/1] bought!")
        else:
            print("[gen/1] not enough points")
        
    def handleSave(e):
        if saveenabled:
            savefile = open("saves/"+savefiletf.value+"/save.json", mode="r+")
            savefile.write("{\"points\": %s}" % points)
            print("[save] saved!")
        else:
            print("[save] failed to save: save is disabled")
    def handleLoad(e):
        global points
        if saveenabled:
            savefile = open("saves/"+savefiletf.value+"/save.json", mode="r+")
            contents = json.load(savefile)
            points = contents["points"]
            print("[save] loaded!")
        else:
            print("[save] failed to load: save is disabled")
    def handleDebugPts(e):
        global points, saveenabled
        if debugpointstf.value != '':
            points = int(debugpointstf.value)
            print(f"[debug] set points to {0}".format(int(debugpointstf.value)))
        else:
            print("[debug] will not set points; debug points text field is invalid")
        saveenabled = False
        print("[save/debug] save has been disabled due to enabling debug mode!")
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
    def handleInfPoints(e):
        global points
        handleDebugPts(None)
        points = 1e+70000000
    fpscounter = ft.Text("FPS: [DISABLED]")
    buymaxbtn = ft.TextButton(f"Buy Max: {buymax}", on_click=handleBuyMax)
    # page.add(buymaxbtn)
    pointscounter = ft.Text(str(points)+" points")
    buygen1button = ft.ElevatedButton(f"Buy Basic Generator ({gen1['amount']}) | Cost: {gen1['cost']}$", on_click=buygen1)
    # page.add(fpscounter, pointscounter, buygen1button)
    savefiletf = ft.TextField(label="Save ID", hint_text="Save ID")
    debugpointstf = ft.TextField(label="Set Points")
    # page.add(ft.Row([ft.ElevatedButton("Save", on_click=handleSave), ft.ElevatedButton("Load", on_click=handleLoad), savefiletf]))
    # page.add(ft.Row([debugpointstf, ft.IconButton(ft.icons.CHECK, on_click=handleDebugPts)]))
    
    def buildApp(approute):
        page.views.clear()
        # if page.route == "/":
        page.views.append(
            ft.View(
                "/", [
                    ft.AppBar(title=ft.Text("CommandIncremental"), center_title=True, actions=[ft.IconButton(ft.icons.SETTINGS, on_click=lambda _: page.go("/settings"))]),
                    pointscounter, buygen1button,
                    ft.Row([ft.ElevatedButton("Save", on_click=handleSave), ft.ElevatedButton("Load", on_click=handleLoad), savefiletf]),
                    ft.Row([debugpointstf, ft.IconButton(ft.icons.CHECK, on_click=handleDebugPts)]),
                    buymaxbtn,
                    # ft.ElevatedButton("Goto Test", on_click=lambda _: page.go("/test"))
                    
                ]
            )
        )
        if page.route == "/test":
            page.views.append(
                ft.View(
                    "/test", [
                        ft.Text("Hello World!")
                    ]
                )
            )
        elif page.route == "/settings":
            page.views.append(
                ft.View(
                    "/settings", [
                        ft.AppBar(title=ft.Text("CommandIncremental | Settings")),
                        ft.TextButton("Infinite Points", on_click=handleInfPoints)
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
        starttime = time.time()
        pointscounter.value = "{:e} points | ".format(points)+str("{:.3f}".format(pointsperspec))+" points per frame"
        buygen1button.text = "Buy Basic Generator ("+"{:e}".format(gen1['amount'])+") | Cost: {:e}$".format(gen1['cost'])
        # fpscounter.value = "FPS: " + str(1.0 / (time.time() - starttime)) # raw clock speed fps # due to reasons
        page.update()
        time.sleep(0.0025) # make the game capped at 12 fps (0.083333333333333328707 sec)
        if buymax is True:
            buygen1(None)

def update():
    while True:
        global points
        points += pointsperspec
        time.sleep(0.1)

if __name__ == "__main__":
    updateThread = Thread(target=update)
    updateThread.start()
    ft.app(target=main, port=8000)
