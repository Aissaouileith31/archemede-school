import flet as ft
import requests
import time
import random
import threading
from plyer import notification
import os
# --- CONFIGURATION ---
MESSAGES_URL = "https://raw.githubusercontent.com/Aissaouileith31/school_data3/refs/heads/main/messege.json"
CRENAU_URL = "https://raw.githubusercontent.com/Aissaouileith31/school_data3/refs/heads/main/crenau.json"
# For the user info, you can also fetch this from GitHub if you like


def home(page: ft.Page):
    user_name = page.client_storage.get("username") or "User"
    user_id = page.client_storage.get("user_id") or "0000"
    page.title = "Archemede Dashboard"
    page.window.width = 400
    page.window.height = 700
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0F172A"
    
    PRIMARY = "#6366F1"
    def logout(e):
        page.client_storage.clear() # Deletes all login info
        page.go("/")

    # --- DATA FETCHING LOGIC ---
# Change these lines in your code:
    messages_list = ft.Column(spacing=10, scroll=ft.ScrollMode.ADAPTIVE, expand=True)
    crenau_list = ft.Column(spacing=10, scroll=ft.ScrollMode.ADAPTIVE, expand=True)
    # --- DRAWER BUTTON FUNCTIONS ---
    def handle_drawer_change(e):
        index = e.control.selected_index
        if index == 2: # Help Button (Show a popup)
            page.open(ft.AlertDialog(title=ft.Text("Besoin d'aide?"), content=ft.Text("Contactez l'administration au: 0555-XXX-XXX")))
        elif index == 3: # Website Button
            page.launch_url("https://votre-ecole.com")
        elif index == 4: # Map Button
            # This opens the school location on Google Maps
            page.launch_url("https://www.google.com/maps/search/?api=1&query=35.1234, -1.2345")
        
        page.update()

    page.drawer = ft.NavigationDrawer(
        on_change=handle_drawer_change,
        controls=[
            ft.Container(height=12),
            ft.Text("  Menu Scolaire", size=20, weight="bold"),
            ft.Divider(),
            

            # Index 1
            ft.NavigationDrawerDestination(
                icon=ft.Icons.TRANSLATE,
                label="Changer la Langue",
            ),
            ft.Divider(),
            # Index 2
            ft.NavigationDrawerDestination(
                icon=ft.Icons.HELP_OUTLINE,
                label="Aide & Support",
            ),
            # Index 3
            ft.NavigationDrawerDestination(
                icon=ft.Icons.LANGUAGE,
                label="Site Web de l'école",
            ),
            # Index 4
            ft.NavigationDrawerDestination(
                icon=ft.Icons.MAP_OUTLINED,
                label="Localisation (Maps)",
            ),
        ],
    )
    def open_sidebar(e):
        page.drawer.open = True
        page.update()
    
    def send_system_notify(title, msg):
        try:
            notification.notify(
                title=title,
                message=msg,
                app_name="Archemede school",
                ticker="Nouveau message de l'école !", # Text that crawls across the top
                timeout=10
            )
        except Exception as e:
            print(f"Notification Error: {e}")
    def fetch_data(e=None):
        cache_buster = f"{int(time.time())}{random.randint(100, 999)}"

    # 2. Tell the server: "Do not give me old data!"
        headers = {
        "Cache-Control": "no-cache, no-store, must-revalidate",
        "Pragma": "no-cache",
        "Expires": "0"
        }
        
        # Reset lists and show loading
        for l in [messages_list, crenau_list]:
            l.controls.clear()
            l.controls.append(ft.ProgressBar(color=PRIMARY))
        page.update()

        try:
            # Fetch the messages from GitHub
            msg_res = requests.get(f"{MESSAGES_URL}?nocache={cache_buster}",headers=headers, timeout=5).json()
            messages_list.controls.clear()
            
            for item in reversed(msg_res):
                # EDIT: Check if the receiver matches the logged-in user
                # We check "receiver" or "resiver_user" based on your JSON keys
                if item.get("receiver") == user_name:
                    messages_list.controls.append(
                        ft.Container(
                            content=ft.ListTile(title=ft.Text(f'adminsrateur le: {item["date"]}'), subtitle=ft.Text(f'type: {item['type_de_message']}\n{item['message']}')),
                            bgcolor="white10", border_radius=10
                        )
                    )
            
            crenau_res = requests.get(f"{CRENAU_URL}?nocache={cache_buster}",headers=headers, timeout=5).json()
            crenau_list.controls.clear()
            for item in crenau_res:
                if item.get("resiver_user") == user_name:

                    crenau_list.controls.append(
                        ft.Container(
                            content=ft.ListTile(title=ft.Text(f'crenau: {item['matier']} inscri le {item['date_de_iscription']}'), subtitle=ft.Text(f'jour du crenau: {item['jour']}\ntemp:\n  debu: {item['debu']}\n  fin: {item['fin']}\nnbr de cour rest: {item['nbr_cour']}\nexpire: {item['expire']}')),
                            bgcolor="white10", border_radius=10
                        )
                    )
        except:
            pass # Handle errors silently for this demo
        page.update()

    def monitor_notifications():
        last_count = -1 
        while True:
            try:
                # Add a small random delay so we don't spam GitHub
                cache_buster = f"{time.time()}"
                res = requests.get(f"{MESSAGES_URL}?v={cache_buster}", timeout=10).json()
                
                # Filter messages for this user
                user_msgs = [m for m in res if m.get("receiver") == user_name]
                current_count = len(user_msgs)

                if last_count != -1 and current_count > last_count:
                    # A NEW MESSAGE ARRIVED!
                    new_msg_data = user_msgs[-1]
                    send_system_notify(
                        "Archemede: " + new_msg_data.get("type_de_message", "Avis"),
                        new_msg_data.get("message", "Nouveau message reçu")
                    )
                    # Refresh the app UI if it's open
                    try:
                        fetch_data()
                    except:
                        pass
                
                last_count = current_count
            except Exception as e:
                print(f"Checking error: {e}")
            
            # Check every 60 seconds
            time.sleep(60)

    # Start the thread
    t = threading.Thread(target=monitor_notifications, daemon=True)
    t.start()
    # 1. User Info Tab (Profile Card)
    user_tab = ft.Container(
        content=ft.Column([
            ft.Row([
                # 1. The Menu Button
                ft.IconButton(
                    icon=ft.Icons.MENU, 
                    icon_color=PRIMARY, 
                    on_click=open_sidebar,
                ),
                # 2. Centered Text (using expand=True and textAlign="center")
                ft.Text(
                    "Mon Profile", 
                    size=28, 
                    weight="bold", 
                    expand=True, 
                    text_align=ft.TextAlign.CENTER
                ),
                # 3. Empty spacer to push text to the middle
                ft.Container(width=40) 
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Container(
                content=ft.Column([
                    ft.CircleAvatar(content=ft.Icon(ft.Icons.PERSON, size=40), radius=40, bgcolor=PRIMARY),
                    ft.Text(user_name, size=22, weight="bold"),
                    ft.Text(f"ID: {user_id}", color="white54"),
                    ft.Divider(height=20, color="white10"),
                    # Visual Barcode Representation
                    ft.Text("BARCODE", size=10, weight="bold", color=PRIMARY),
                    ft.Image(
                        src=f"https://bwipjs-api.metafloor.com/?bcid=code128&text={user_id}&scale=3&rotate=N&includetext&barcolor=ffffff",
                        width=120,
                        height=120,
                    ),
                ], horizontal_alignment="center"),
                bgcolor="#1E293B",
                padding=30,
                border_radius=25,
                alignment=ft.alignment.center,
                border=ft.Border(ft.BorderSide(1, "white10"))
            ),
            ft.ElevatedButton("deconecter", color="red400", icon=ft.Icons.LOGOUT,on_click=logout)
        ], horizontal_alignment="center", spacing=20),
        padding=20
    )

    # 2. Messages Tab
    msg_tab = ft.Container(
        content=ft.Column([
            ft.Row([ft.Text("Messages", size=24, weight="bold"), 
                    ft.IconButton(ft.Icons.REFRESH, on_click=fetch_data)], alignment="spaceBetween"),
            messages_list
        ]), padding=20
    )

    # 3. Crenau Tab
    crenau_tab = ft.Container(
        content=ft.Column([
            ft.Row([ft.Text("Crenau", size=24, weight="bold"), 
                    ft.IconButton(ft.Icons.REFRESH, on_click=fetch_data)], alignment="spaceBetween"),
            crenau_list
        ]), padding=20
    )

    # --- MAIN TABS ---
    tabs = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[
            ft.Tab(text="Profile", icon=ft.Icons.PERSON_ROUNDED, content=user_tab),
            ft.Tab(text="Messages", icon=ft.Icons.EMAIL_ROUNDED, content=msg_tab),
            ft.Tab(text="Crenau", icon=ft.Icons.CALENDAR_MONTH_ROUNDED, content=crenau_tab),
        ],
        expand=1,
    )

    page.add(tabs)
    fetch_data() # Initial load

