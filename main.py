#!/usr/bin/env python3
"""
SAST Aviator Desktop Application
Main entry point for the application
"""

import flet as ft
from config.config_manager import ConfigManager
from ui.setup_tab import SetupTab
from ui.audit_tab import AuditTab
from utils.constants import COLORS


class SASTAviatorApp:
    """Main application class"""
    
    def __init__(self):
        self.config_manager = ConfigManager()
        self.setup_tab = None
        self.audit_tab = None
    
    def main(self, page: ft.Page):
        """Main application entry point"""
        # Configure page
        page.title = "Opentext SAST Aviator Application"
        page.window_width = 1200
        page.window_height = 800
        page.window_min_width = 800
        page.window_min_height = 600
        page.theme_mode = ft.ThemeMode.LIGHT
        page.padding = 0
        
        # Ensure the entire page is scrollable
        page.scroll = ft.ScrollMode.AUTO
        
        # Custom theme with OpenText colors
        page.theme = ft.Theme(
            color_scheme_seed=COLORS['electric_blue'],
            use_material3=True
        )
        
        # Initialize tabs
        self.setup_tab = SetupTab(page, self.config_manager)
        self.audit_tab = AuditTab(page, self.config_manager)
        
        # Create header
        header = ft.Container(
            content=ft.Row([
                ft.Icon(name=ft.Icons.SECURITY, color=COLORS['white'], size=30),
                ft.Text(
                    "Opentext SAST Aviator Application",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=COLORS['white']
                ),
                ft.Container(expand=True),  # Spacer
                ft.Image(
                    src="images/icon.png",
                    width=50,
                    height=50,
                    fit=ft.ImageFit.CONTAIN
                )
            ], alignment=ft.MainAxisAlignment.START),
            bgcolor=COLORS['electric_blue'],
            padding=ft.padding.symmetric(horizontal=20, vertical=15),
            height=60
        )
        
        # Create tabs with proper scrolling
        tabs = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=[
                ft.Tab(
                    text="Setup & Configuration",
                    icon=ft.Icons.SETTINGS,
                    content=ft.Container(
                        content=self.setup_tab.build(),
                        expand=True
                    )
                ),
                ft.Tab(
                    text="Audit Operations",
                    icon=ft.Icons.ASSESSMENT,
                    content=ft.Container(
                        content=self.audit_tab.build(),
                        expand=True
                    )
                )
            ],
            tab_alignment=ft.TabAlignment.CENTER,
            expand=True,
            height=page.window_height - 100  # Account for header height
        )
        
        # Create main container with fixed header and scrollable content
        main_container = ft.Column(
            [
                header,
                ft.Container(
                    content=tabs,
                    expand=True,
                    padding=0
                )
            ],
            spacing=0,
            expand=True,
            scroll=ft.ScrollMode.HIDDEN  # The tabs handle their own scrolling
        )
        
        page.add(main_container)
        
        # Load existing mappings
        self.audit_tab._refresh_mappings_table()


def main():
    """Application entry point"""
    app = SASTAviatorApp()
    ft.app(target=app.main, assets_dir="assets")


if __name__ == "__main__":
    main()