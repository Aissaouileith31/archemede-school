import flet as ft
from app_file.pages.login import login
from app_file.pages.home_page import home

# main.py
def main_location(page: ft.Page):
    def route_change(e):
        page.clean()
        
        # Check login status
        is_logged_in = page.client_storage.get("logged_in") == "yes"

        if page.route == "/":
            if is_logged_in:
                return page.go("/home")
            login(page)

        elif page.route == "/home":
            if not is_logged_in:
                return page.go("/")
            home(page) # Call without 'username' as home(page) gets it from storage

        else:
            page.add(ft.Text("404: Not Found"))

    page.on_route_change = route_change
    page.go(page.route)
ft.app(target=main_location, assets_dir="assets/")
