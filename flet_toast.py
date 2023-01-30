import flet as ft
import time

class Toast(ft.UserControl):
    def __init__(self, value: str, title: str=None):
        super().__init__()
        self.title: str | None = title
        self.value: str = value
    
    def build(self):
        return ft.Container(ft.Column([
            ft.Text(self.title, style=ft.TextThemeStyle.BODY_LARGE) if self.title else ft.Divider(height=0, thickness=0),
            ft.Divider(height=3, thickness=3) if self.title else ft.Divider(height=0, thickness=0),
            ft.Text(self.value)
        ]),bgcolor=ft.colors.SURFACE_VARIANT, expand=True, border_radius=4, alignment=ft.alignment.bottom_center)
        
class ToastV2(ft.UserControl):
    def __init__(self, value: str, title: str=None, onclick=lambda _: None):
        super().__init__()
        self.title: str | None = title
        self.value: str = value
        self.on_click = onclick
        self.control = ft.Card(
            content=ft.Container(
                content=ft.ListTile(
                            # leading=ft.Icon(ft.icons.ALBUM),
                            title=ft.Text(self.title) if self.title else ft.Text(self.value),
                            subtitle=ft.Text(self.value) if self.title else None,
                        ),
                width=400,
                padding=10,
                expand=True,
                on_click=self.on_click
            ),
            offset=ft.transform.Offset(-2, 0),
            animate_offset=ft.animation.Animation(1000),
        )
    def show(self):
        self.control.offset = ft.transform.Offset(0, 0)
        self.control.update()
    def hide(self):
        self.control.offset = ft.transform.Offset(-2,0)
        self.control.update()
    def autorehide(self):
        self.show()
        time.sleep(2)
        self.hide()
    
    def build(self):
        return self.control