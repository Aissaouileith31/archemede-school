import flet as ft
import requests
import bcrypt  # Library used for secure password hashing and verification
from app_file.base64image import icons 
import time

# --- CONFIGURATION ---
# URL of the JSON file containing student credentials on GitHub
USERS_URL = "https://raw.githubusercontent.com/Aissaouileith31/school_data3/refs/heads/main/user.json"

def login(page: ft.Page):
    # --- PAGE SETTINGS ---
    page.title = "Archemede school"
    page.bgcolor = "#0F172A"      # Main background (Dark Navy)
    page.padding = 0
    page.theme_mode = ft.ThemeMode.DARK # Forces dark mode theme

    # Standard window sizing for desktop testing
    page.window_width = 450
    page.window_height = 800
    
    # UI Color Palette
    PRIMARY = "#6366F1"  # Indigo color for buttons/branding
    ACCENT = "#2DD4BF"   # Teal color (optional use)

    # --- LOGIN LOGIC ---
    def validate_login(e):
        # 1. Basic validation: Check if fields are empty
        if not user_input.value or not pass_input.value:
            error_text.value = "Veuillez entrer toutes les informations"
            error_text.visible = True
            page.update()
            return

        # 2. UI Feedback: Change button text to a loading spinner
        login_btn.content = ft.ProgressRing(width=20, height=20, color="white", stroke_width=2)
        login_btn.disabled = True
        error_text.visible = False # Hide previous errors
        page.update()

        try:
            # 3. Network Request: Download the user list from GitHub
            response = requests.get(USERS_URL, timeout=5)
            data = response.json()
            students = data.get("students", [])
            
            # 4. Search: Find a student whose 'username' matches the input
            user_data = next((u for u in students if u['username'] == user_input.value), None)
            
            is_valid = False
            if user_data:
                # 5. Security: Verify the password using bcrypt
                # Input password must be encoded to bytes for comparison
                password_bytes = pass_input.value.encode('utf-8')
                hashed_bytes = user_data['mp'].encode('utf-8') # 'mp' is the hashed password in JSON
                
                # Check if the plain text matches the hash
                if bcrypt.checkpw(password_bytes, hashed_bytes):
                    is_valid = True

            if is_valid:
                # 6. Session Management: Save user data locally on the phone/PC
                page.client_storage.set("logged_in", "yes")
                page.client_storage.set("username", user_data['username'])
                page.client_storage.set("user_id", str(user_data['id']))
                
                # Small delay for visual smoothness before navigating
                time.sleep(0.5)
                page.go('/home') # Move to the dashboard
            else:
                # If username not found or password fails
                error_text.value = "Nom d'utilisateur ou mot de passe incorrect"
                error_text.visible = True
            
            reset_button() # Restore button state
        except Exception as ex:
            # Error handling for No Internet or GitHub down
            error_text.value = "Erreur: Vérifiez votre connexion internet"
            error_text.visible = True
            reset_button()
        page.update()

    def reset_button():
        """ Restores the login button from loading spinner to text """
        login_btn.content = ft.Text("Se Connecter", weight="bold")
        login_btn.disabled = False

    # --- UI COMPONENTS ---
    
    # Username Input Field
    user_input = ft.TextField(
        label="Nom d'utilisateur", 
        border_radius=15, 
        bgcolor="black12", 
        border_color="white10", 
        prefix_icon=ft.Icons.PERSON_OUTLINE
    )
    
    # Password Input Field with Visibility Toggle
    pass_input = ft.TextField(
        label="Mot de passe", 
        password=True, 
        can_reveal_password=True, 
        border_radius=15, 
        bgcolor="black12", 
        border_color="white10", 
        prefix_icon=ft.Icons.LOCK_OUTLINE
    )
    
    # Hidden error message text
    error_text = ft.Text("", color="red400", size=12, visible=False)
    
    # Login Button
    login_btn = ft.ElevatedButton(
        content=ft.Text("Se Connecter", weight="bold"), 
        bgcolor=PRIMARY, 
        color="white", 
        width=300, 
        height=50, 
        on_click=validate_login
    )

    # Main Login Card Design
    login_card = ft.Container(
        content=ft.Column([
            # Logo from base64 string
            ft.Image(src_base64=icons[0], width=100, height=100, fit=ft.ImageFit.CONTAIN),   
            
            ft.Text("Connectez-vous", size=32, weight="bold", color="#6366F1"),
            ft.Text("Entrez vos informations", color="white38"),
            
            ft.Divider(height=20, color="transparent"), # Spacer
            
            user_input, 
            pass_input, 
            error_text,
            
            ft.Divider(height=10, color="transparent"), # Spacer
            
            login_btn,

        ], horizontal_alignment="center"),
        padding=40, 
        bgcolor="#1A1A2E",  # Dark card background
        border_radius=30,
        border=ft.Border(ft.BorderSide(1, "white10")), # Subtle border
        expand=True # Fill space
    )

    # Render components to the screen
    page.add(login_card)
