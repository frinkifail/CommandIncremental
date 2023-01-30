import flet as ft

# im not lazy i promise you
class Advancement(ft.UserControl):
    def __init__(self, value: str, icon: ft.Icon, title: str=None, onclick=lambda _: None):
        super().__init__()
        self.title: str | None = title
        self.value: str = value
        self.on_click = onclick
        self.icon = icon
        self.completed = False
        self.control = ft.Card(
            content=ft.Container(
                content=ft.ListTile(
                            leading=self.icon,
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
    # def autorehide(self):
    #     self.show()
    #     time.sleep(2)
    #     self.hide()
    def complete(self):
        self.completed = True
        print(f"completed called in {self.title}/{self.value}")
    def uncomplete(self):
        self.completed = False
        print(f"uncompleted called in {self.title}/{self.value}")
    def check_if_completed(self):
        if self.completed:
            print(self.control.content)
            print(self.control.content.content)
            self.control.content.content.trailing = ft.Icon(ft.icons.CHECK, color=ft.colors.GREEN_ACCENT)
            # self.control.update()
            print(f'{self.title}/{self.value} is completed')
        else:
            print(self.control.content)
            print(self.control.content.content)
            self.control.content.content.trailing = ft.Icon(ft.icons.CLOSE, color=ft.colors.RED_ACCENT)
            # self.control.update()
            print(f'{self.title}/{self.value} is not completed')
    def build(self):
        return self.control
