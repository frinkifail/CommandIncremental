import flet as ft
import time

def createNoti(e, title, content):
    notification_base = ft.Container(ft.Column([ft.Row([ft.Text("  "+title+"\t       ", weight=ft.FontWeight.BOLD, font_family="Noto Sans"), ft.IconButton(ft.icons.CHECK, on_click=lambda _: hideNoti(None))]), ft.Divider(height=5, thickness=1), ft.Text("  "+content)]), bgcolor=ft.colors.BLUE_GREY_900, width=200, border_radius=4, offset=ft.transform.Offset(-2, 0), animate_offset=ft.animation.Animation(300))
    def revealNoti(e):
        notification_base.offset = ft.transform.Offset(0, 0)
        notification_base.update()
    def hideNoti(e):
        notification_base.offset = ft.transform.Offset(-2, 0)
        notification_base.update()
    def tickNoti(e):
        revealNoti(None)
        time.sleep(1.75)
        hideNoti(None)
    return [notification_base, revealNoti, hideNoti, tickNoti]
