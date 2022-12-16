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
        savefile = open("saves/"+savefiletf.value+"/save.json", mode="r+")
        savefile.write("{\"points\": %s}" % points)
        print("[save] saved!")
    def handleLoad(e):
        global points
        savefile = open("saves/"+savefiletf.value+"/save.json", mode="r+")
        contents = json.load(savefile)
        points = contents["points"]
        print("[save] loaded!")
    def handleDebugPts(e):
        global points
        points = int(debugpointstf.value)
        print(f"[debug] set points to {0}".format(points))
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
    fpscounter = ft.Text("FPS: 0")
    buymaxbtn = ft.TextButton(f"Buy Max: {buymax}", on_click=handleBuyMax)
    page.add(buymaxbtn)
    pointscounter = ft.Text(str(points)+" points")
    buygen1button = ft.ElevatedButton(f"Buy Basic Generator ({gen1['amount']}) | Cost: {gen1['cost']}$", on_click=buygen1)
    page.add(fpscounter, pointscounter, buygen1button)
    savefiletf = ft.TextField(label="Save ID", hint_text="Save ID")
    debugpointstf = ft.TextField(label="Set Points")
    page.add(ft.Row([ft.ElevatedButton("Save", on_click=handleSave), ft.ElevatedButton("Load", on_click=handleLoad), savefiletf]))
    page.add(debugpointstf, ft.IconButton(ft.icons.CHECK, on_click=handleDebugPts))
    while True:
        # global buymax
        starttime = time.time()
        pointscounter.value = "{:e} points | ".format(points)+str("{:.3f}".format(pointsperspec))+" points per frame"
        buygen1button.text = "Buy Basic Generator ("+"{:e}".format(gen1['amount'])+") | Cost: {:e}$".format(gen1['cost'])
        fpscounter.value = "FPS: " + str(1.0 / (time.time() - starttime)) # raw clock speed fps # due to reasons
        page.update()
        time.sleep(0.083333333333333328707) # make the game capped at 12 fps
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
