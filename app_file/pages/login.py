import flet as ft
import requests
import bcrypt# Added for password verification
from app_file.base64image import icons 
import time

# --- CONFIGURATION ---
USERS_URL = "https://raw.githubusercontent.com/Aissaouileith31/school_data3/refs/heads/main/user.json"

def login(page: ft.Page):
    page.title = "Archemede school"
    page.bgcolor = "#0F172A"
    page.padding = 0
    page.window_width = 450
    page.window_height = 800
    
    PRIMARY = "#6366F1"
    ACCENT = "#2DD4BF"





    def validate_login(e):
        if not user_input.value or not pass_input.value:
            error_text.value = "entre tout les information"
            error_text.visible = True
            page.update()
            return

        login_btn.content = ft.ProgressRing(width=20, height=20, color="white", stroke_width=2)
        login_btn.disabled = True
        error_text.visible = False
        page.update()

        try:
            response = requests.get(USERS_URL, timeout=5)
            data = response.json()
            students = data.get("students", [])
            
            # 1. Find user by username first
            user_data = next((u for u in students if u['username'] == user_input.value), None)
            
            # 2. If user exists, verify the hashed password (mp)
            is_valid = False
            if user_data:
                # bcrypt requires bytes, so we encode the input and the stored hash
                password_bytes = pass_input.value.encode('utf-8')
                hashed_bytes = user_data['mp'].encode('utf-8')
                
                if bcrypt.checkpw(password_bytes, hashed_bytes):
                    is_valid = True

            if is_valid:
                # SAVE SESSION DATA SO HOME_PAGE CAN USE IT
                page.client_storage.set("logged_in", "yes")
                page.client_storage.set("username", user_data['username'])
                page.client_storage.set("user_id", str(user_data['id']))
                time.sleep(0.5)
                page.go('/home')
            else:
                error_text.value = "nom de utilisateur ou mot de pass incorect"
                error_text.visible = True
            
            reset_button()
        except Exception as ex:
            error_text.value = "error: verifier votre connection"
            error_text.visible = True
            reset_button()
        page.update()

    def reset_button():
        login_btn.content = ft.Text("Conecter", weight="bold")
        login_btn.disabled = False

    # --- UI COMPONENTS ---
    user_input = ft.TextField(label="nom de utilisateur", border_radius=15, bgcolor="black12", border_color="white10", prefix_icon=ft.Icons.PERSON_OUTLINE)
    pass_input = ft.TextField(label="mot de pass", password=True, can_reveal_password=True, border_radius=15, bgcolor="black12", border_color="white10", prefix_icon=ft.Icons.LOCK_OUTLINE)
    error_text = ft.Text("", color="red400", size=12, visible=False)
    login_btn = ft.ElevatedButton(content=ft.Text("conecter", weight="bold"), bgcolor=PRIMARY, color="white", width=300, height=50, on_click=validate_login)

    login_card = ft.Container(
        content=ft.Column([
            ft.Image(src_base64=icons[0],width=100,height=100,fit=ft.ImageFit.CONTAIN,),   
            ft.Text("Conecter vous", size=32, weight="bold", color="#6366F1"),
            ft.Text("Entere votre information", color="white38",),
            ft.Divider(height=20, color="transparent"),
            user_input, pass_input, error_text,
            ft.Divider(height=10, color="transparent"),
            login_btn,

        ], horizontal_alignment="center"),
        padding=40, bgcolor="#1A1A2E", border_radius=30,
        border=ft.Border(ft.BorderSide(1, "white10")),
        expand=True
    )

    page.add(login_card,

            )
    

