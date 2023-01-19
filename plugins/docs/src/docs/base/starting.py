# import flet as ft

# def main(page: ft.Page):
#     pa = lambda control: page.add(control)
#     pt = lambda text, style: pa(ft.Text(text, style=style))
#     tts = ft.TextThemeStyle
    
#     pt("Starting out", tts.TITLE_LARGE)
#     pt("Basic Elements Of The Game", tts.TITLE_MEDIUM)
#     pt("Starting out, you have 10$ and no silicon at all. To start, just buy a generator to start mining some silicon.", tts.BODY_LARGE)
#     pt("You can use that generated silicon to sell for money, and then just buy some more generators with that money, and the cycle repeats.", tts.BODY_LARGE)
#     pt("The pages", tts.TITLE_LARGE)
#     pt("You've probably seen by now, but if you're literally blind, there's an app bar on top of the screen, and there's action buttons, which when on clicked, cycle between pages of the game", tts.BODY_LARGE)
#     pt("The Settings", tts.TITLE_LARGE)
#     pt("The settings, a place where you configure stuff, of course, you've probably clicked it already before you even read this documentation.", tts.BODY_LARGE)
#     pt("There, you can configure the update interval (which doesn't really make you generate silicon/money faster since that's in another thread). This thing controls how fast should the game update (tick). This is kind of like being able to control the TPS of a Minecraft Server.", tts.BODY_LARGE)
#     pt("The Upgrades", tts.TITLE_LARGE)
#     pt("The upgrades, this is where you upgrade things... You may have noticed that the generated silicon is not going above a specific limit, and that's because there's actually an upgrade to make the limit higher. This is called the Max Silicon upgrade.", tts.BODY_LARGE)
#     pt("There is another upgrade called \"Silicon Multiplier\" which multiplies your gains (only silicon).")
#     pt("Then, there is the last upgrade.... for now. This upgrade is called the Generation Time upgrade, which controls how fast should the silicon/money should be generated.", tts.BODY_LARGE)
#     pt("So uhh, a little techical thing here. This upgrade only applies to the `update` thread. Which means, this doesn't actually make the game tick faster, only the gaining silicon part (this variable is used to control how fast the `time.sleep` in the `update` thread is.)", tts.BODY_MEDIUM)
    
    

# ft.app("CommandDocs | Base Game -> Starting out", port=8110)
