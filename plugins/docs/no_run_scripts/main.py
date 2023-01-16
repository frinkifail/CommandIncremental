import flet as ft

def main(page: ft.Page) -> None:
    page.add(ft.Text("Hello!"))
    
if __name__ == "__main__":
    ft.app(target=main, port=8011, view=ft.FLET_APP_HIDDEN)
