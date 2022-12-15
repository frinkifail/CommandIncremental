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

def main(page: ft.Page):
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
            
    fpscounter = ft.Text("FPS: 0")
    pointscounter = ft.Text(str(points)+" points")
    buygen1button = ft.ElevatedButton(f"Buy generator 1 ({gen1['amount']}) | Cost: {gen1['cost']}$", on_click=buygen1)
    page.add(fpscounter, pointscounter, buygen1button)
    savefiletf = ft.TextField(label="Save ID", hint_text="Save ID")
    page.add(ft.ElevatedButton("Save", on_click=handleSave), ft.ElevatedButton("Load", on_click=handleLoad), savefiletf)
    while True:
        starttime = time.time()
        pointscounter.value = str(math.floor(points))+" points | "+str(pointsperspec)+" points per frame"
        buygen1button.text = f"Buy generator 1 ({gen1['amount']}) | Cost: {gen1['cost']}$"
        fpscounter.value = "FPS: " + str(1.0 / (time.time() - starttime)) # raw clock speed fps # due to reasons
        page.update()
        time.sleep(0.083333333333333328707) # make the game capped at 12 fps

def update():
    while True:
        global points
        points += pointsperspec
        time.sleep(0.1)

if __name__ == "__main__":
    updateThread = Thread(target=update)
    updateThread.start()
    ft.app(target=main, port=8000)
