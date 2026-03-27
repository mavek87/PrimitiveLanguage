import flet as ft
from modules.ui.ui import LinguaPrimitivaApp


def main(page: ft.Page):
    LinguaPrimitivaApp(page)


if __name__ == "__main__":
    ft.app(target=main)
