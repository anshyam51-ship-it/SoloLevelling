import flet as ft
import math
import re

def get_level_from_total_xp(total_xp):
    a = 10
    d = 2
    discriminant = ((2 * a - d) ** 2) - (4 * d * (-2 * total_xp))
    if discriminant < 0:
        return 0
    n = (-(2 * a - d) + math.sqrt(discriminant)) / (2 * d)
    return math.floor(n)

def parse_to_spans(text):
    """Aapke custom terminal symbols (*, #, @, !, $) ko App layout spans me convert karne ke liye function"""
    tokens = re.split(r'([\*_#!$@])', text)
    spans = []
    
    current_bold = False
    current_italic = False
    current_color = ft.Colors.WHITE

    for token in tokens:
        if token == '*':
            current_bold = not current_bold
            continue
        elif token == '_':
            current_italic = not current_italic
            continue
        elif token == '#':
            current_color = ft.Colors.GREEN_ACCENT_400 if current_color == ft.Colors.WHITE else ft.Colors.WHITE
            continue
        elif token == '@':
            current_color = ft.Colors.CYAN_300 if current_color == ft.Colors.WHITE else ft.Colors.WHITE
            continue
        elif token == '!':
            current_color = ft.Colors.RED_400 if current_color == ft.Colors.WHITE else ft.Colors.WHITE
            continue
        elif token == '$':
            current_color = ft.Colors.YELLOW_400 if current_color == ft.Colors.WHITE else ft.Colors.WHITE
            continue
        
        if token:
            spans.append(
                ft.TextSpan(
                    token,
                    style=ft.TextStyle(
                        weight=ft.FontWeight.BOLD if current_bold else ft.FontWeight.NORMAL,
                        italic=current_italic,
                        color=current_color
                    )
                )
            )
    return spans

def main(page: ft.Page):
    page.title = "XP Level Converter"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#121212"

    # UI Components
    title = ft.Text("🎮 XP LEVEL CALCULATOR", size=26, weight=ft.FontWeight.BOLD, color=ft.Colors.CYAN)
    
    result_text = ft.Text(spans=[], size=18, text_align=ft.TextAlign.CENTER)

    # Core Logic Function
    def process_calculation():
        user_val = xp_input.value.strip()
        
        if user_val.lower() == 'quit':
            result_text.spans = parse_to_spans("\n Exiting calculator. Goodbye! 👋")
            page.update()
            return

        try:
            val = int(user_val)
            if val < 0:
                raw_msg = "You are at !less than lvl 0!, what the hell you're doing with your life! *$Get up, Grow more!$* *$Become Better$*"
                result_text.spans = parse_to_spans(raw_msg)
            else:
                lvl = get_level_from_total_xp(val)
                raw_msg = f"🌟 Total XP: @{val}@ -> You are at #*Level {lvl}*#"
                result_text.spans = parse_to_spans(raw_msg)
                
            # SUCCESS: Hide calculate button and show reset button
            calc_button.visible = False
            reset_button.visible = True
                
        except ValueError:
            result_text.spans = parse_to_spans("!*Invalid input!* Please enter an _integer_.")
            # Format invalid hone par bhi option switch kar sakte hain, abhi button toggle on rakha hai
            calc_button.visible = False
            reset_button.visible = True
        
        page.update()

    # Reset Function
    def reset_click(e):
        xp_input.value = ""          # Clear text input field
        result_text.spans = []       # Clear results
        calc_button.visible = True   # Bring back Calculate button
        reset_button.visible = False # Hide Reset button
        page.update()

    def calculate_click(e):
        process_calculation()

    def calculate_submit(e):
        process_calculation()

    # TextField Setup
    xp_input = ft.TextField(
        label="Enter Total XP", 
        text_align=ft.TextAlign.CENTER, 
        width=280,
        keyboard_type=ft.KeyboardType.NUMBER,
        border_color=ft.Colors.CYAN,
        focused_border_color=ft.Colors.GREEN,
        on_submit=calculate_submit
    )

    # Buttons Setup
    calc_button = ft.ElevatedButton(
        "Calculate Level", 
        on_click=calculate_click,
        width=280,
        style=ft.ButtonStyle(bgcolor=ft.Colors.CYAN_700, color=ft.Colors.WHITE)
    )

    reset_button = ft.ElevatedButton(
        "Reset",
        on_click=reset_click,
        width=280,
        visible=False, # Start me hidden rahega
        style=ft.ButtonStyle(bgcolor=ft.Colors.GREY_700, color=ft.Colors.WHITE)
    )

    # Building App Screen
    page.add(
        ft.Container(
            content=ft.Column(
                [
                    title,
                    ft.Container(height=10),
                    xp_input,
                    calc_button,
                    reset_button, # Added row element here
                    ft.Container(height=20),
                    result_text
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            padding=30,
            bgcolor="#1e1e1e",
            border_radius=20,
            shadow=ft.BoxShadow(blur_radius=15, color="#000000")
        )
    )

ft.app(target=main)
