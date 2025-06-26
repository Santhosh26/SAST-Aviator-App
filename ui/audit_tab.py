"""Audit Operations Tab UI with enhanced features"""

import flet as ft
import threading
from datetime import datetime
from pathlib import Path
from typing import List

from config.config_manager import ConfigManager
from services.ssc_service import SSCService
from services.aviator_service import AviatorService
from utils.constants import COLORS
from utils.validators import Validators
from utils.helpers import update_status, create_section_container, create_button
from utils.logger import setup_logger

# Set up logging
logger = setup_logger(__name__)


class AuditTab:
    """Audit Operations Tab (Steps 5-9) with enhanced features"""
    
    def __init__(self, page: ft.Page, config_manager: ConfigManager):
        self.page = page
        self.config = config_manager
        self.container = None
        
        # Individual status texts for each section
        self.ssc_status = ft.Text("", color=COLORS['dark_gray'])
        self.aviator_status = ft.Text("", color=COLORS['dark_gray'])
        self.app_mgmt_status = ft.Text("", color=COLORS['dark_gray'])
        self.audit_status = ft.Text("", color=COLORS['dark_gray'])
        
        # Form fields
        self.ssc_url = ft.TextField(
            label="SSC URL",
            value=self.config.get('ssc', 'url'),
            width=400,
            on_change=self._validate_ssc_url
        )
        self.ssc_username = ft.TextField(
            label="Username",
            value=self.config.get('ssc', 'username'),
            width=400
        )
        self.ssc_password = ft.TextField(
            label="Password",
            password=True,
            can_reveal_password=True,
            width=400
        )
        
        # Aviator session token field and file picker
        self.aviator_token_path = ft.TextField(
            label="Token File Path",
            value=self.config.get('tokens', 'current_token_file'),
            width=350,
            read_only=True
        )
        
        self.aviator_token_picker = ft.FilePicker(
            on_result=self._on_aviator_token_picker_result
        )
        self.page.overlay.append(self.aviator_token_picker)
        
        self.new_app_name = ft.TextField(
            label="New App Name",
            width=400,
            on_change=self._validate_app_name
        )
        
        # Data tables with checkbox support for multi-select
        self.selected_ssc_apps = set()
        self.selected_aviator_apps = set()
        
        self.ssc_apps_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Select")),
                ft.DataColumn(ft.Text("SSC Application")),
                ft.DataColumn(ft.Text("Version")),
                ft.DataColumn(ft.Text("ID")),
            ],
            rows=[],
            show_checkbox_column=False  # We'll manage checkboxes manually
        )
        
        self.aviator_apps_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Select")),
                ft.DataColumn(ft.Text("Aviator Application")),
                ft.DataColumn(ft.Text("ID")),
            ],
            rows=[],
            show_checkbox_column=False
        )
        
        # Create scrollable containers for tables
        self.ssc_apps_list = ft.ListView(
            controls=[self.ssc_apps_table],
            height=250,
            spacing=0,
            padding=ft.padding.all(5)
        )
        
        self.aviator_apps_list = ft.ListView(
            controls=[self.aviator_apps_table],
            height=250,
            spacing=0,
            padding=ft.padding.all(5)
        )
        
        # Multi-select mapping interface
        self.mapping_mode = ft.RadioGroup(
            content=ft.Row([
                ft.Radio(value="single", label="Single Mapping"),
                ft.Radio(value="multi", label="Multi-Select Mapping")
            ]),
            value="single"
        )
        
        # Single mapping dropdowns (existing)
        self.ssc_app_dropdown = ft.Dropdown(
            label="Select SSC App:Version",
            width=300
        )
        self.aviator_app_dropdown = ft.Dropdown(
            label="Select Aviator App",
            width=300
        )
        
        self.mappings_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("SSC App:Version")),
                ft.DataColumn(ft.Text("Aviator App")),
                ft.DataColumn(ft.Text("Actions")),
            ],
            rows=[]
        )
        
        # Create scrollable container for mappings table
        self.mappings_list = ft.ListView(
            controls=[self.mappings_table],
            height=200,
            spacing=0,
            padding=ft.padding.all(5)
        )
        
        # Audit controls
        self.audit_mapping_dropdown = ft.Dropdown(
            label="Select Mapping for Audit",
            width=400
        )
        
        # Create properly scrollable audit results
        self.audit_results = ft.TextField(
            label="Audit Results",
            multiline=True,
            min_lines=15,
            max_lines=15,
            read_only=True,
            width=700,
            height=400,
            text_size=12,
            color=COLORS['dark_gray']
        )
        
        # Wrap audit results in a scrollable container with fixed height
        self.audit_results_container = ft.Container(
            content=ft.ListView(
                controls=[self.audit_results],
                height=400,
                spacing=0,
                padding=ft.padding.all(5)
            ),
            border=ft.border.all(1, COLORS['dark_gray']),
            border_radius=8,
            height=420,
            width=720
        )
    
    def build(self) -> ft.Container:
        """Build the audit tab UI"""
        # Create scrollable column with all sections
        scrollable_content = ft.Column(
            [
                ft.Text("Audit Operations", size=24, weight=ft.FontWeight.BOLD, color=COLORS['electric_blue']),
                ft.Text("Execute SAST audits after completing setup. Ensure Setup tab is completed first.", 
                       size=14, color=COLORS['dark_gray'], italic=True),
                ft.Divider(),
                
                # Step 5: SSC Session
                self._build_ssc_session_section(),
                ft.Divider(height=20),
                
                # Step 6: Aviator Session with browse option
                self._build_aviator_session_section(),
                ft.Divider(height=20),
                
                # Steps 7-8: Application Management with multi-select
                self._build_app_management_section(),
                ft.Divider(height=20),
                
                # Step 9: Audit Execution with scrollable results
                self._build_audit_section(),
                
                ft.Container(height=20)  # Bottom padding
            ],
            spacing=10,
            scroll=ft.ScrollMode.AUTO
        )
        
        # Wrap in container with proper height constraints
        self.container = ft.Container(
            content=scrollable_content,
            padding=20,
            expand=True
        )
        
        return self.container
    
    def _build_ssc_session_section(self) -> ft.Container:
        """Build SSC session section"""
        help_text = ft.Container(
            content=ft.Text(
                "🔗 Connect to Software Security Center (SSC):\n"
                "• SSC URL: Your organization's SSC server (e.g., http://your-ssc:8080/ssc)\n"
                "• Username: Your SSC login credentials\n"
                "• Password: Your SSC password (stored securely, not saved)\n"
                "• This connection allows access to your application versions for audit",
                size=12,
                color=COLORS['dark_gray']
            ),
            bgcolor=COLORS['light_blue'],
            border_radius=5,
            padding=10
        )
        
        return create_section_container(
            "Step 5: SSC Session",
            [
                help_text,
                self.ssc_url,
                ft.Row([
                    self.ssc_username,
                    self.ssc_password
                ]),
                create_button("Login to SSC", self._login_ssc, 
                            COLORS['electric_blue'], COLORS['white']),
                self.ssc_status
            ],
            COLORS['cobalt_blue'],
            COLORS['light_gray']
        )
    
    def _build_aviator_session_section(self) -> ft.Container:
        """Build Aviator session section with token browse option"""
        help_text = ft.Container(
            content=ft.Text(
                "🚀 Connect to Aviator service:\n"
                "• Uses authentication token (from Setup tab or browse for different token)\n"
                "• Establishes authenticated session with Aviator\n"
                "• Required for creating apps and running audits\n"
                "• You can use the default token or browse for a different one",
                size=12,
                color=COLORS['dark_gray']
            ),
            padding=ft.padding.only(bottom=10),
            bgcolor=COLORS['light_blue'],
            border_radius=5
        )
        
        return create_section_container(
            "Step 6: Aviator Session",
            [
                help_text,
                ft.Row([
                    self.aviator_token_path,
                    create_button("Browse Token", self._browse_aviator_token, 
                                COLORS['cobalt_blue'], COLORS['white'])
                ]),
                create_button("Login to Aviator", self._login_aviator, 
                            COLORS['electric_blue'], COLORS['white']),
                self.aviator_status
            ],
            COLORS['cobalt_blue'],
            COLORS['light_gray']
        )
    
    def _build_app_management_section(self) -> ft.Container:
        """Build application management section with multi-select support"""
        help_text = ft.Container(
            content=ft.Text(
                "📱 Manage applications and create mappings:\n"
                "• Create new Aviator apps if needed, or use existing ones\n"
                "• List applications from both SSC and Aviator\n"
                "• Single Mapping: Select one SSC app and one Aviator app\n"
                "• Multi-Select: Check multiple apps from each table and map them all at once\n"
                "• Multiple SSC apps can map to the same Aviator app",
                size=12,
                color=COLORS['dark_gray']
            ),
            padding=ft.padding.only(bottom=10),
            bgcolor=COLORS['light_blue'],
            border_radius=5
        )
        
        # Single mapping interface (existing dropdowns)
        single_mapping_ui = ft.Column([
            ft.Row([
                self.ssc_app_dropdown,
                self.aviator_app_dropdown,
                create_button("Add Mapping", self._add_mapping, 
                            COLORS['yellow'], COLORS['black'])
            ])
        ], visible=True)
        
        # Multi-select mapping interface
        multi_mapping_ui = ft.Column([
            ft.Text("Select multiple apps from the tables above by checking the boxes", 
                   size=12, color=COLORS['dark_gray'], italic=True),
            ft.Row([
                create_button("Map Selected Apps", self._add_multi_mappings, 
                            COLORS['yellow'], COLORS['black']),
                create_button("Clear Selection", self._clear_selection, 
                            COLORS['cobalt_blue'], COLORS['white'])
            ])
        ], visible=False)
        
        # Toggle visibility based on mode
        def on_mapping_mode_change(e):
            is_multi = self.mapping_mode.value == "multi"
            single_mapping_ui.visible = not is_multi
            multi_mapping_ui.visible = is_multi
            self.page.update()
        
        self.mapping_mode.on_change = on_mapping_mode_change
        
        return create_section_container(
            "Steps 7-8: Application Management",
            [
                help_text,
                # Create new Aviator app
                ft.Row([
                    self.new_app_name,
                    create_button("Create Aviator App", self._create_aviator_app, 
                                COLORS['cobalt_blue'], COLORS['white'])
                ]),
                
                # List applications
                ft.Row([
                    create_button("List SSC Apps", self._list_ssc_apps, 
                                COLORS['electric_blue'], COLORS['white']),
                    create_button("List Aviator Apps", self._list_aviator_apps, 
                                COLORS['electric_blue'], COLORS['white'])
                ]),
                
                self.app_mgmt_status,
                
                # Applications tables with checkboxes
                ft.Row([
                    ft.Column([
                        ft.Text("SSC Applications", weight=ft.FontWeight.BOLD),
                        ft.Container(
                            content=self.ssc_apps_list,
                            border=ft.border.all(1, COLORS['dark_gray']),
                            border_radius=8
                        )
                    ], expand=1),
                    ft.Column([
                        ft.Text("Aviator Applications", weight=ft.FontWeight.BOLD),
                        ft.Container(
                            content=self.aviator_apps_list,
                            border=ft.border.all(1, COLORS['dark_gray']),
                            border_radius=8
                        )
                    ], expand=1)
                ]),
                
                # Mapping mode selector
                ft.Text("Mapping Mode", size=16, weight=ft.FontWeight.BOLD),
                self.mapping_mode,
                
                # Mapping interfaces
                single_mapping_ui,
                multi_mapping_ui,
                
                ft.Text("Current Mappings", weight=ft.FontWeight.BOLD),
                ft.Container(
                    content=self.mappings_list,
                    border=ft.border.all(1, COLORS['dark_gray']),
                    border_radius=8
                )
            ],
            COLORS['cobalt_blue'],
            COLORS['light_gray']
        )
    
    def _build_audit_section(self) -> ft.Container:
        """Build audit execution section with scrollable results"""
        help_text = ft.Container(
            content=ft.Text(
                "🔍 Execute SAST audit on your applications:\n"
                "• Select a mapping from the dropdown (created in Steps 7-8)\n"
                "• Run audit to analyze SSC app using Aviator intelligence\n"
                "• Results will show in the scrollable text area below\n"
                "• Audit may take several minutes depending on application size",
                size=12,
                color=COLORS['dark_gray']
            ),
            padding=ft.padding.only(bottom=10),
            bgcolor=COLORS['light_blue'],
            border_radius=5
        )
        
        return create_section_container(
            "Step 9: Audit Execution",
            [
                help_text,
                self.audit_mapping_dropdown,
                create_button("Run Audit", self._run_audit, 
                            COLORS['electric_blue'], COLORS['white']),
                self.audit_status,
                ft.Text("Audit Results (Scrollable):", weight=ft.FontWeight.BOLD),
                self.audit_results_container
            ],
            COLORS['cobalt_blue'],
            COLORS['light_gray']
        )
    
    def _browse_aviator_token(self, e):
        """Browse for Aviator token file"""
        logger.info("Browsing for Aviator token file")
        try:
            self.aviator_token_picker.pick_files(
                dialog_title="Select Aviator token file",
                allowed_extensions=["json"],
                file_type=ft.FilePickerFileType.CUSTOM
            )
        except Exception as ex:
            logger.error(f"Error opening token file picker: {str(ex)}")
            self._update_section_status(self.aviator_status, 
                                      f"Error opening file picker: {str(ex)}", 
                                      COLORS['error_red'])
    
    def _on_aviator_token_picker_result(self, e: ft.FilePickerResultEvent):
        """Handle Aviator token file picker result"""
        if e.files and len(e.files) > 0:
            file_path = e.files[0].path
            self.aviator_token_path.value = file_path
            logger.info(f"Selected Aviator token: {file_path}")
            self._update_section_status(self.aviator_status, 
                                      f"Token selected: {Path(file_path).name}", 
                                      COLORS['success_green'])
        self.page.update()
    
    def _validate_ssc_url(self, e):
        """Validate SSC URL format"""
        if not Validators.validate_url(self.ssc_url.value):
            self.ssc_url.error_text = "Invalid URL format"
        else:
            self.ssc_url.error_text = None
        self.page.update()
    
    def _validate_app_name(self, e):
        """Validate app name format"""
        if not Validators.validate_app_name(self.new_app_name.value):
            self.new_app_name.error_text = "Invalid app name (use only letters, numbers, spaces, hyphens, underscores)"
        else:
            self.new_app_name.error_text = None
        self.page.update()
    
    def _login_ssc(self, e):
        """Login to SSC"""
        if not Validators.validate_url(self.ssc_url.value):
            self._update_section_status(self.ssc_status, 
                                      "Please enter a valid SSC URL", COLORS['error_red'])
            return
        
        def login():
            try:
                self._update_section_status(self.ssc_status, "Logging into SSC...", COLORS['yellow'])
                
                success, message = SSCService.login(
                    self.ssc_url.value,
                    self.ssc_username.value,
                    self.ssc_password.value
                )
                
                if success:
                    self._update_section_status(self.ssc_status, message, COLORS['success_green'])
                    self.config.set('ssc', 'url', self.ssc_url.value)
                    self.config.set('ssc', 'username', self.ssc_username.value)
                    self.config.set('ssc', 'last_session', datetime.now().isoformat())
                else:
                    self._update_section_status(self.ssc_status, message, COLORS['error_red'])
                    
            except Exception as e:
                self._update_section_status(self.ssc_status, 
                                          f"SSC login failed: {str(e)}", COLORS['error_red'])
        
        threading.Thread(target=login, daemon=True).start()
    
    def _login_aviator(self, e):
        """Login to Aviator with selected token"""
        def login():
            try:
                self._update_section_status(self.aviator_status, "Logging into Aviator...", COLORS['yellow'])
                
                token_file = self.aviator_token_path.value
                server_url = self.config.get('server', 'url')
                
                if not token_file or not Path(token_file).exists():
                    self._update_section_status(self.aviator_status, 
                                              "Please select a valid token file", COLORS['error_red'])
                    return
                
                success, message = AviatorService.login(server_url, token_file)
                
                if success:
                    self._update_section_status(self.aviator_status, message, COLORS['success_green'])
                    # Update config with the currently used token
                    self.config.set('tokens', 'current_token_file', token_file)
                else:
                    self._update_section_status(self.aviator_status, message, COLORS['error_red'])
                    
            except Exception as e:
                self._update_section_status(self.aviator_status, 
                                          f"Aviator login failed: {str(e)}", COLORS['error_red'])
        
        threading.Thread(target=login, daemon=True).start()
    
    def _create_aviator_app(self, e):
        """Create new Aviator application"""
        if not self.new_app_name.value:
            self._update_section_status(self.app_mgmt_status, 
                                      "Please enter an app name", COLORS['error_red'])
            return
        
        if not Validators.validate_app_name(self.new_app_name.value):
            self._update_section_status(self.app_mgmt_status, 
                                      "Invalid app name format", COLORS['error_red'])
            return
        
        def create():
            try:
                self._update_section_status(self.app_mgmt_status, "Creating Aviator app...", COLORS['yellow'])
                
                success, message = AviatorService.create_app(self.new_app_name.value)
                
                if success:
                    self._update_section_status(self.app_mgmt_status, message, COLORS['success_green'])
                    self.new_app_name.value = ""
                    self.page.update()
                    # Refresh the Aviator apps list
                    self._list_aviator_apps(None)
                else:
                    self._update_section_status(self.app_mgmt_status, message, COLORS['error_red'])
                    
            except Exception as e:
                self._update_section_status(self.app_mgmt_status, 
                                          f"App creation failed: {str(e)}", COLORS['error_red'])
        
        threading.Thread(target=create, daemon=True).start()
    
    def _list_ssc_apps(self, e):
        """List SSC applications with checkboxes for multi-select"""
        def list_apps():
            try:
                self._update_section_status(self.app_mgmt_status, "Listing SSC applications...", COLORS['yellow'])
                
                success, apps_data, error_msg = SSCService.list_applications()
                
                if success:
                    self.ssc_apps_table.rows.clear()
                    self.selected_ssc_apps.clear()
                    dropdown_options = []
                    
                    for app in apps_data:
                        app_name = app.get('application', {}).get('name', 'Unknown')
                        version = app.get('name', 'Unknown')
                        app_id = app.get('id', 'Unknown')
                        app_key = f"{app_name}:{version}"
                        
                        # Create checkbox for multi-select
                        checkbox = ft.Checkbox(
                            value=False,
                            data=app_key,
                            on_change=lambda e, key=app_key: self._toggle_ssc_selection(key, e.control.value)
                        )
                        
                        self.ssc_apps_table.rows.append(
                            ft.DataRow(cells=[
                                ft.DataCell(checkbox),
                                ft.DataCell(ft.Text(app_name)),
                                ft.DataCell(ft.Text(version)),
                                ft.DataCell(ft.Text(str(app_id)))
                            ])
                        )
                        
                        dropdown_options.append(ft.dropdown.Option(
                            key=app_key,
                            text=app_key
                        ))
                    
                    self.ssc_app_dropdown.options = dropdown_options
                    self.page.update()
                    self._update_section_status(self.app_mgmt_status, 
                                              f"Listed {len(apps_data)} SSC applications", COLORS['success_green'])
                else:
                    self._update_section_status(self.app_mgmt_status, error_msg, COLORS['error_red'])
                    
            except Exception as e:
                self._update_section_status(self.app_mgmt_status, 
                                          f"Failed to list SSC apps: {str(e)}", COLORS['error_red'])
        
        threading.Thread(target=list_apps, daemon=True).start()
    
    def _list_aviator_apps(self, e):
        """List Aviator applications with checkboxes for multi-select"""
        def list_apps():
            try:
                self._update_section_status(self.app_mgmt_status, "Listing Aviator applications...", COLORS['yellow'])
                
                success, apps_data, error_msg = AviatorService.list_apps()
                
                if success:
                    self.aviator_apps_table.rows.clear()
                    self.selected_aviator_apps.clear()
                    dropdown_options = []
                    
                    for app in apps_data:
                        app_name = app.get('name', 'Unknown')
                        app_id = app.get('id', 'Unknown')
                        
                        # Create checkbox for multi-select
                        checkbox = ft.Checkbox(
                            value=False,
                            data=app_name,
                            on_change=lambda e, name=app_name: self._toggle_aviator_selection(name, e.control.value)
                        )
                        
                        self.aviator_apps_table.rows.append(
                            ft.DataRow(cells=[
                                ft.DataCell(checkbox),
                                ft.DataCell(ft.Text(app_name)),
                                ft.DataCell(ft.Text(str(app_id)))
                            ])
                        )
                        
                        dropdown_options.append(ft.dropdown.Option(
                            key=app_name,
                            text=app_name
                        ))
                    
                    self.aviator_app_dropdown.options = dropdown_options
                    self.page.update()
                    self._update_section_status(self.app_mgmt_status, 
                                              f"Listed {len(apps_data)} Aviator applications", COLORS['success_green'])
                else:
                    self._update_section_status(self.app_mgmt_status, error_msg, COLORS['error_red'])
                    
            except Exception as e:
                self._update_section_status(self.app_mgmt_status, 
                                          f"Failed to list Aviator apps: {str(e)}", COLORS['error_red'])
        
        threading.Thread(target=list_apps, daemon=True).start()
    
    def _toggle_ssc_selection(self, app_key: str, selected: bool):
        """Toggle SSC app selection for multi-mapping"""
        if selected:
            self.selected_ssc_apps.add(app_key)
        else:
            self.selected_ssc_apps.discard(app_key)
        logger.debug(f"SSC selection updated: {self.selected_ssc_apps}")
    
    def _toggle_aviator_selection(self, app_name: str, selected: bool):
        """Toggle Aviator app selection for multi-mapping"""
        if selected:
            self.selected_aviator_apps.add(app_name)
        else:
            self.selected_aviator_apps.discard(app_name)
        logger.debug(f"Aviator selection updated: {self.selected_aviator_apps}")
    
    def _clear_selection(self, e):
        """Clear all multi-select checkboxes"""
        self.selected_ssc_apps.clear()
        self.selected_aviator_apps.clear()
        
        # Uncheck all checkboxes in SSC table
        for row in self.ssc_apps_table.rows:
            checkbox = row.cells[0].content
            if isinstance(checkbox, ft.Checkbox):
                checkbox.value = False
        
        # Uncheck all checkboxes in Aviator table
        for row in self.aviator_apps_table.rows:
            checkbox = row.cells[0].content
            if isinstance(checkbox, ft.Checkbox):
                checkbox.value = False
        
        self._update_section_status(self.app_mgmt_status, "Selection cleared", COLORS['success_green'])
        self.page.update()
    
    def _add_mapping(self, e):
        """Add single application mapping"""
        if not self.ssc_app_dropdown.value or not self.aviator_app_dropdown.value:
            self._update_section_status(self.app_mgmt_status, 
                                      "Please select both SSC and Aviator applications", COLORS['error_red'])
            return
        
        ssc_app = self.ssc_app_dropdown.value
        aviator_app = self.aviator_app_dropdown.value
        
        # Save to config
        self.config.add_mapping(ssc_app, aviator_app)
        
        # Refresh the mappings table
        self._refresh_mappings_table()
        
        self._update_section_status(self.app_mgmt_status, 
                                  f"Mapping added: {ssc_app} → {aviator_app}", COLORS['success_green'])
    
    def _add_multi_mappings(self, e):
        """Add multiple mappings at once"""
        if not self.selected_ssc_apps:
            self._update_section_status(self.app_mgmt_status, 
                                      "Please select at least one SSC application", COLORS['error_red'])
            return
        
        if not self.selected_aviator_apps:
            self._update_section_status(self.app_mgmt_status, 
                                      "Please select at least one Aviator application", COLORS['error_red'])
            return
        
        # Create mappings for all combinations
        mappings_added = []
        
        # If only one Aviator app is selected, map all SSC apps to it
        if len(self.selected_aviator_apps) == 1:
            aviator_app = list(self.selected_aviator_apps)[0]
            for ssc_app in self.selected_ssc_apps:
                self.config.add_mapping(ssc_app, aviator_app)
                mappings_added.append(f"{ssc_app} → {aviator_app}")
        # If multiple Aviator apps selected, create 1:1 mappings
        else:
            ssc_list = list(self.selected_ssc_apps)
            aviator_list = list(self.selected_aviator_apps)
            
            # Map as many as possible (1:1)
            for i in range(min(len(ssc_list), len(aviator_list))):
                self.config.add_mapping(ssc_list[i], aviator_list[i])
                mappings_added.append(f"{ssc_list[i]} → {aviator_list[i]}")
        
        # Clear selections
        self._clear_selection(None)
        
        # Refresh the mappings table
        self._refresh_mappings_table()
        
        if mappings_added:
            self._update_section_status(self.app_mgmt_status, 
                                      f"Added {len(mappings_added)} mappings", COLORS['success_green'])
            logger.info(f"Mappings added: {mappings_added}")
        else:
            self._update_section_status(self.app_mgmt_status, 
                                      "No mappings were added", COLORS['yellow'])
    
    def _remove_mapping(self, ssc_app: str):
        """Remove application mapping"""
        self.config.remove_mapping(ssc_app)
        self._refresh_mappings_table()
        self._update_section_status(self.app_mgmt_status, f"Mapping removed: {ssc_app}", COLORS['success_green'])
    
    def _refresh_mappings_table(self):
        """Refresh the mappings table from config"""
        self.mappings_table.rows.clear()
        audit_options = []
        
        mappings = self.config.get_all_mappings()
        for ssc_app, aviator_app in mappings.items():
            self.mappings_table.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(ssc_app)),
                    ft.DataCell(ft.Text(aviator_app)),
                    ft.DataCell(create_button(
                        "Remove",
                        lambda e, ssc=ssc_app: self._remove_mapping(ssc),
                        COLORS['error_red'],
                        COLORS['white']
                    ))
                ])
            )
            
            audit_options.append(ft.dropdown.Option(
                key=f"{ssc_app}|{aviator_app}",
                text=f"{ssc_app} → {aviator_app}"
            ))
        
        self.audit_mapping_dropdown.options = audit_options
        self.page.update()
    
    def _run_audit(self, e):
        """Run audit on selected mapping with scrollable results"""
        if not self.audit_mapping_dropdown.value:
            self._update_section_status(self.audit_status, 
                                      "Please select a mapping for audit", COLORS['error_red'])
            return
        
        def run_audit():
            try:
                self._update_section_status(self.audit_status, "Running audit...", COLORS['yellow'])
                self.audit_results.value = "Audit in progress...\n\n"
                self.page.update()
                
                mapping_key = self.audit_mapping_dropdown.value
                ssc_app, aviator_app = mapping_key.split('|')
                
                # Add timestamp and audit info
                audit_start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                self.audit_results.value += f"Audit started at: {audit_start_time}\n"
                self.audit_results.value += f"SSC Application: {ssc_app}\n"
                self.audit_results.value += f"Aviator Application: {aviator_app}\n"
                self.audit_results.value += "-" * 80 + "\n\n"
                self.page.update()
                
                success, result = AviatorService.run_audit(ssc_app, aviator_app)
                
                if success:
                    self.audit_results.value += f"Audit completed successfully!\n\n"
                    self.audit_results.value += "=== AUDIT OUTPUT ===\n"
                    self.audit_results.value += result
                    self._update_section_status(self.audit_status, "Audit completed successfully!", COLORS['success_green'])
                else:
                    self.audit_results.value += f"Audit failed!\n\n"
                    self.audit_results.value += "=== ERROR DETAILS ===\n"
                    self.audit_results.value += result
                    self._update_section_status(self.audit_status, f"Audit failed", COLORS['error_red'])
                
                # Add completion timestamp
                audit_end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                self.audit_results.value += f"\n\n-" * 40
                self.audit_results.value += f"\nAudit ended at: {audit_end_time}"
                
                self.page.update()
                    
            except Exception as e:
                error_msg = f"Audit exception: {str(e)}"
                self.audit_results.value += f"\n\n=== EXCEPTION ===\n{error_msg}"
                self._update_section_status(self.audit_status, error_msg, COLORS['error_red'])
                logger.error(error_msg, exc_info=True)
                self.page.update()
        
        threading.Thread(target=run_audit, daemon=True).start()
    
    def _update_section_status(self, status_text: ft.Text, message: str, color: str):
        """Update section-specific status message"""
        update_status(status_text, message, color, self.page)