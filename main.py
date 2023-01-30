from typing import Literal
import flet as ft
from flet_toast import ToastV2

VERSION: Literal['2.0'] = "2.0.0"

def app(page: ft.Page) -> None:
    page.title = "CommandIncremental "+VERSION
    page.window_title_bar_hidden = True
    # page.window_title_bar_buttons_hidden = True
    
    #### VAR TESTS
    testnoti = ToastV2("Hello world!", "Test")
    #### END VAR TESTS

    def route_change(route):
        page.views.clear()
        page.views.append(
            ft.View(
                "/",
                [
                    ft.AppBar(title=ft.Text("CommandIncremental "+VERSION)),
                    ft.Text("Hello this is very epic!!!"),
                    ToastV2("Ayo what?"),
                    ToastV2("hmm", "titled"),
                    ft.ElevatedButton('Reveal', on_click=lambda _: testnoti.show()),
                    ft.ElevatedButton('Hide', on_click=lambda _: testnoti.hide()),
                    ft.ElevatedButton('Autohide', on_click=lambda _: testnoti.autorehide()),
                    testnoti
                    # ft.ElevatedButton("Visit Store", on_click=lambda _: page.go("/store")),
                ],
            )
        )
        if page.route == "/store":
            page.views.append(
                ft.View(
                    "/store",
                    [
                        ft.AppBar(title=ft.Text("Store"), bgcolor=ft.colors.SURFACE_VARIANT),
                        ft.ElevatedButton("Go Home", on_click=lambda _: page.go("/")),
                    ],
                )
            )
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)
    # page.views[0].page.overlay.append(ToastV2("hmm", "titled"))
    
if __name__ == "__main__":
    ft.app(target=app)
