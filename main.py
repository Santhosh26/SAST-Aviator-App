#!/usr/bin/env python3
"""
SAST Aviator Desktop Application
Main entry point for the application - Fixed version
"""

import flet as ft
import logging
import sys
import os
from pathlib import Path
from config.config_manager import ConfigManager
from ui.setup_tab import SetupTab
from ui.audit_tab import AuditTab
from utils.constants import COLORS
from utils.logger import setup_logger

# Set up logging
logger = setup_logger(__name__)


class SASTAviatorApp:
    """Main application class"""
    
    def __init__(self):
        self.config_manager = ConfigManager()
        self.setup_tab = None
        self.audit_tab = None
        logger.info("SAST Aviator App initialized")
    
    def main(self, page: ft.Page):
        """Main application entry point"""
        logger.info("Starting SAST Aviator application")
        
        # Configure page
        page.title = "Opentext SAST Aviator Application"
        page.window_width = 1200
        page.window_height = 800
        page.window_min_width = 800
        page.window_min_height = 600
        page.theme_mode = ft.ThemeMode.LIGHT
        page.padding = 0
        
        # CRITICAL: Remove scroll from page level to prevent infinite scrolling
        page.scroll = None  # Use None instead of HIDDEN to completely disable
        
        # Custom theme with OpenText colors
        page.theme = ft.Theme(
            color_scheme_seed=COLORS['electric_blue'],
            use_material3=True
        )
        
        logger.debug("Page configuration completed")
        
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
                ft.IconButton(
                    icon=ft.Icons.SETTINGS,
                    icon_color=COLORS['white'],
                    tooltip="Settings",
                    on_click=lambda _: logger.info("Settings clicked")
                )
            ], alignment=ft.MainAxisAlignment.START),
            bgcolor=COLORS['electric_blue'],
            padding=ft.padding.symmetric(horizontal=20, vertical=15),
            height=60
        )
        
        # Create tabs with proper content handling
        tabs = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=[
                ft.Tab(
                    text="Setup & Configuration",
                    icon=ft.Icons.SETTINGS,
                    # Tab content needs to be wrapped to ensure proper scrolling
                    content=ft.Container(
                        content=self.setup_tab.build(),
                        expand=True,
                        padding=0,
                        clip_behavior=ft.ClipBehavior.ANTI_ALIAS
                    )
                ),
                ft.Tab(
                    text="Audit Operations",
                    icon=ft.Icons.ASSESSMENT,
                    content=ft.Container(
                        content=self.audit_tab.build(),
                        expand=True,
                        padding=0,
                        clip_behavior=ft.ClipBehavior.ANTI_ALIAS
                    )
                )
            ],
            tab_alignment=ft.TabAlignment.CENTER,
            expand=True,
            height=None  # Let content determine height
        )
        
        # Create main container that fills the entire window
        main_container = ft.Column(
            [
                header,
                tabs  # Tabs directly without container wrapper
            ],
            spacing=0,
            expand=True  # Critical for expand chain
        )
        
        # Clear the page and add main container
        page.controls.clear()
        page.add(main_container)
        page.update()
        
        # Load existing mappings
        self.audit_tab._refresh_mappings_table()
        
        logger.info("Application UI loaded successfully")


def main():
    """Application entry point with single instance check"""
    try:
        # Set up single instance for packaged app
        if getattr(sys, 'frozen', False):
            # Running as packaged executable
            import tempfile
            lock_file = Path(tempfile.gettempdir()) / "sast_aviator.lock"
            
            # Check if lock file exists and is recent
            if lock_file.exists():
                # Check if file is less than 5 seconds old
                import time
                if time.time() - lock_file.stat().st_mtime < 5:
                    logger.warning("Another instance is already running")
                    sys.exit(0)
            
            # Create/update lock file
            lock_file.touch()
            logger.info(f"Lock file created at {lock_file}")
        
        app = SASTAviatorApp()
        ft.app(
            target=app.main, 
            assets_dir="assets" if os.path.exists("assets") else None,
            view=ft.AppView.FLET_APP  # Ensure proper app view
        )
        
    except Exception as e:
        logger.error(f"Application failed to start: {str(e)}", exc_info=True)
        raise
    finally:
        # Clean up lock file if running as executable
        if getattr(sys, 'frozen', False) and 'lock_file' in locals():
            try:
                lock_file.unlink(missing_ok=True)
                logger.info("Lock file removed")
            except:
                pass


if __name__ == "__main__":
    main()