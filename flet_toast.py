import flet as ft

class Toast(ft.UserControl):
    def __init__(self, value: str, title: str | None=None):
        super().__init__()
        self.title: str | None = title
        self.value: str = value
    
    def build(self):
        return ft.Container(ft.Column([
            ft.Text(self.title, style=ft.TextThemeStyle.BODY_LARGE) if self.title else ft.Text(),
            ft.Divider(height=3, thickness=3) if self.title else ft.Text(),
            ft.Text(self.value)
        ]),bgcolor=ft.colors.INDIGO_ACCENT, expand=True)
