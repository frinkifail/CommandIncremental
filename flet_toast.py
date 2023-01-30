import flet as ft

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
    def __init__(self, value: str, title: str=None):
        super().__init__()
        self.title: str | None = title
        self.value: str = value
    
    def build(self):
        return ft.Card(
            content=ft.Container(
                content=ft.ListTile(
                            # leading=ft.Icon(ft.icons.ALBUM),
                            title=ft.Text(self.title) if self.title else ft.Text(self.value),
                            subtitle=ft.Text(self.value) if self.title else None,
                        ),
                # width=400,
                padding=10,
                expand=True,
            )
        )
