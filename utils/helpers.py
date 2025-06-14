"""Helper functions for the application"""

from datetime import datetime
import flet as ft


def update_status(status_text: ft.Text, message: str, color: str, page: ft.Page):
    """Update status message with timestamp"""
    status_text.value = f"[{datetime.now().strftime('%H:%M:%S')}] {message}"
    status_text.color = color
    page.update()


def create_section_container(title: str, content: list, color: str, bg_color: str) -> ft.Container:
    """Create a styled section container"""
    return ft.Container(
        content=ft.Column([
            ft.Text(title, size=18, weight=ft.FontWeight.BOLD, color=color),
            *content
        ]),
        bgcolor=bg_color,
        padding=15,
        border_radius=8
    )


def create_button(text: str, on_click, bgcolor: str, color: str, width: int = None) -> ft.ElevatedButton:
    """Create a styled button"""
    return ft.ElevatedButton(
        text,
        on_click=on_click,
        bgcolor=bgcolor,
        color=color,
        width=width
    )


def show_error_dialog(page: ft.Page, title: str, message: str):
    """Show an error dialog"""
    dlg = ft.AlertDialog(
        title=ft.Text(title),
        content=ft.Text(message),
        actions=[
            ft.TextButton("OK", on_click=lambda e: close_dialog(page, dlg))
        ]
    )
    page.dialog = dlg
    dlg.open = True
    page.update()


def close_dialog(page: ft.Page, dialog: ft.AlertDialog):
    """Close a dialog"""
    dialog.open = False
    page.update()