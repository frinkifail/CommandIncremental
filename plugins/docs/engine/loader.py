import flet as ft
from subprocess import Popen

def main(page: ft.Page):
    page.title = "CommandDocs | Home"
    pa = lambda control: page.add(control)
    pt = lambda text, style: ft.Text(text, style=style)
    tts = ft.TextThemeStyle
    
    

    def route_change(route):
        page.views.clear()
        page.views.append(
            ft.View(
                "/",
                [
                    ft.AppBar(title=ft.Text("CommandDocs | Home")),
                    ft.Text("The official documentation for CommandIncremental", style=tts.BODY_LARGE),
                    # ft.FilledTonalButton("Goto Docs -> Base Game -> Starting out", on_click=lambda _: Popen(["flet","docs/src/docs/base/starting.py","--web","--port","8110"]))
                ],
            )
        )
        if page.route == "/src":
            page.views.append(ft.View("/src",[ft.Text("/src/docs/base/page")]))
        elif page.route == "/src/docs":
            page.views.append(ft.View("/src/docs",[ft.Text("docs/base")]))
        elif page.route == "/src/docs/base":
            page.views.append(ft.View("/src/docs/base",[
                ft.AppBar(title=ft.Text("CommandDocs | Base Game")),
                ft.Text("Available pages", style=tts.BODY_LARGE),
                ft.Text("Starting out - src.docs.base:starting")
            ])),
        elif page.route == "/src/docs/base/starting":
            page.views.append(ft.View("/src/docs/base/starting",[
                ft.AppBar(title=ft.Text("CommandDocs | Base Game -> Starting out")),
                pt("Starting out", tts.TITLE_LARGE),
                pt("Basic Elements Of The Game", tts.TITLE_MEDIUM),
                pt("Starting out, you have 10$ and no silicon at all. To start, just buy a generator to start mining some silicon.", tts.BODY_LARGE),
                pt("You can use that generated silicon to sell for money, and then just buy some more generators with that money, and the cycle repeats.", tts.BODY_LARGE),
                pt("The pages", tts.TITLE_LARGE),
                pt("You've probably seen by now, but if you're literally blind, there's an app bar on top of the screen, and there's action buttons, which when on clicked, cycle between pages of the game", tts.BODY_LARGE),
                pt("The Settings", tts.TITLE_LARGE),
                pt("The settings, a place where you configure stuff, of course, you've probably clicked it already before you even read this documentation.", tts.BODY_LARGE),
                pt("There, you can configure the update interval (which doesn't really make you generate silicon/money faster since that's in another thread). This thing controls how fast should the game update (tick). This is kind of like being able to control the TPS of a Minecraft Server.", tts.BODY_LARGE),
                pt("The Upgrades", tts.TITLE_LARGE),
                pt("The upgrades, this is where you upgrade things... You may have noticed that the generated silicon is not going above a specific limit, and that's because there's actually an upgrade to make the limit higher. This is called the Max Silicon upgrade.", tts.BODY_LARGE),
                pt("There is another upgrade called \"Silicon Multiplier\" which multiplies your gains (only silicon).", tts.BODY_LARGE),
                pt("Then, there is the last upgrade.... for now. This upgrade is called the Generation Time upgrade, which controls how fast should the silicon/money should be generated.", tts.BODY_LARGE),
                pt("So uhh, a little techical thing here. This upgrade only applies to the `update` thread. Which means, this doesn't actually make the game tick faster, only the gaining silicon part (this variable is used to control how fast the `time.sleep` in the `update` thread is.)", tts.BODY_MEDIUM),
            ]))
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

# Port Format
# 8000 = Main (Game)
# 81xx = CommandDocs
# 8110 = CommandDocs Section 1 , index 0
# 8111 = CommandDocs Section 1 , index 1
# 8100 = CommandDocs Home (here)

# Note: named src doc files do not count in the release as the doc files are completely different files (flet apps)

# Actually, you know what?
# It's too resource demanding

ft.app(target=main, port=8100)
