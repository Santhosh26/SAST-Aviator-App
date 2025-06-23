"""Audit Operations Tab UI"""

import flet as ft
import threading
from datetime import datetime

from config.config_manager import ConfigManager
from services.ssc_service import SSCService
from services.aviator_service import AviatorService
from utils.constants import COLORS
from utils.validators import Validators
from utils.helpers import update_status, create_section_container, create_button


class AuditTab:
    """Audit Operations Tab (Steps 5-9)"""
    
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
        
        self.new_app_name = ft.TextField(
            label="New App Name",
            width=400,
            on_change=self._validate_app_name
        )
        
        # Data tables wrapped in ListViews for proper scrolling
        self.ssc_apps_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("SSC Application")),
                ft.DataColumn(ft.Text("Version")),
                ft.DataColumn(ft.Text("ID")),
            ],
            rows=[]
        )
        
        self.aviator_apps_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Aviator Application")),
                ft.DataColumn(ft.Text("ID")),
            ],
            rows=[]
        )
        
        # Create scrollable containers for tables
        self.ssc_apps_list = ft.ListView(
            controls=[self.ssc_apps_table],
            height=200,
            spacing=0,
            padding=ft.padding.all(5)
        )
        
        self.aviator_apps_list = ft.ListView(
            controls=[self.aviator_apps_table],
            height=200,
            spacing=0,
            padding=ft.padding.all(5)
        )
        
        # Mapping controls
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
            height=150,
            spacing=0,
            padding=ft.padding.all(5)
        )
        
        # Audit controls
        self.audit_mapping_dropdown = ft.Dropdown(
            label="Select Mapping for Audit",
            width=400
        )
        
        self.audit_results = ft.TextField(
            label="Audit Results",
            multiline=True,
            min_lines=10,
            read_only=True,
            width=600
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
                
                # Step 6: Aviator Session
                self._build_aviator_session_section(),
                ft.Divider(height=20),
                
                # Steps 7-8: Application Management
                self._build_app_management_section(),
                ft.Divider(height=20),
                
                # Step 9: Audit Execution
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
        """Build Aviator session section"""
        help_text = ft.Container(
            content=ft.Text(
                "🚀 Connect to Aviator service:\n"
                "• Uses the token generated in Step 4 of Setup tab\n"
                "• Establishes authenticated session with Aviator\n"
                "• Required for creating apps and running audits\n"
                "• Ensure you've completed all Setup steps before proceeding",
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
                ft.Text(f"Token File: {self.config.get('tokens', 'current_token_file')}"),
                create_button("Login to Aviator", self._login_aviator, 
                            COLORS['electric_blue'], COLORS['white']),
                self.aviator_status
            ],
            COLORS['cobalt_blue'],
            COLORS['light_gray']
        )
    
    def _build_app_management_section(self) -> ft.Container:
        """Build application management section"""
        help_text = ft.Container(
            content=ft.Text(
                "📱 Manage applications and create mappings:\n"
                "• Create new Aviator apps if needed, or use existing ones\n"
                "• List applications from both SSC and Aviator to see what's available\n"
                "• Map SSC app:version combinations to Aviator apps for audit\n"
                "• Multiple SSC apps can map to the same Aviator app\n"
                "• Complete both SSC and Aviator login (Steps 5-6) before proceeding",
                size=12,
                color=COLORS['dark_gray']
            ),
            padding=ft.padding.only(bottom=10),
            bgcolor=COLORS['light_blue'],
            border_radius=5
        )
        
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
                
                # Applications tables with proper scrolling
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
                
                # Mapping interface
                ft.Text("App Mapping", size=16, weight=ft.FontWeight.BOLD),
                ft.Row([
                    self.ssc_app_dropdown,
                    self.aviator_app_dropdown,
                    create_button("Add Mapping", self._add_mapping, 
                                COLORS['yellow'], COLORS['black'])
                ]),
                
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
        """Build audit execution section"""
        help_text = ft.Container(
            content=ft.Text(
                "🔍 Execute SAST audit on your applications:\n"
                "• Select a mapping from the dropdown (created in Steps 7-8)\n"
                "• Run audit to analyze SSC app using Aviator intelligence\n"
                "• Results will show findings, recommendations, and security insights\n"
                "• Ensure all previous steps are completed and sessions are active\n"
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
                self.audit_results
            ],
            COLORS['cobalt_blue'],
            COLORS['light_gray']
        )
    
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
        """Login to Aviator"""
        def login():
            try:
                self._update_section_status(self.aviator_status, "Logging into Aviator...", COLORS['yellow'])
                
                token_file = self.config.get('tokens', 'current_token_file')
                server_url = self.config.get('server', 'url')
                
                success, message = AviatorService.login(server_url, token_file)
                
                if success:
                    self._update_section_status(self.aviator_status, message, COLORS['success_green'])
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
        """List SSC applications"""
        def list_apps():
            try:
                self._update_section_status(self.app_mgmt_status, "Listing SSC applications...", COLORS['yellow'])
                
                success, apps_data, error_msg = SSCService.list_applications()
                
                if success:
                    self.ssc_apps_table.rows.clear()
                    dropdown_options = []
                    
                    for app in apps_data:
                        # Correct parsing of nested JSON structure
                        app_name = app.get('application', {}).get('name', 'Unknown')
                        version = app.get('name', 'Unknown')
                        app_id = app.get('id', 'Unknown')
                        
                        self.ssc_apps_table.rows.append(
                            ft.DataRow(cells=[
                                ft.DataCell(ft.Text(app_name)),
                                ft.DataCell(ft.Text(version)),
                                ft.DataCell(ft.Text(str(app_id)))
                            ])
                        )
                        
                        dropdown_options.append(ft.dropdown.Option(
                            key=f"{app_name}:{version}",
                            text=f"{app_name}:{version}"
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
        """List Aviator applications"""
        def list_apps():
            try:
                self._update_section_status(self.app_mgmt_status, "Listing Aviator applications...", COLORS['yellow'])
                
                success, apps_data, error_msg = AviatorService.list_apps()
                
                if success:
                    self.aviator_apps_table.rows.clear()
                    dropdown_options = []
                    
                    for app in apps_data:
                        app_name = app.get('name', 'Unknown')
                        app_id = app.get('id', 'Unknown')
                        
                        self.aviator_apps_table.rows.append(
                            ft.DataRow(cells=[
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
    
    def _add_mapping(self, e):
        """Add application mapping"""
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
        """Run audit on selected mapping"""
        if not self.audit_mapping_dropdown.value:
            self._update_section_status(self.audit_status, 
                                      "Please select a mapping for audit", COLORS['error_red'])
            return
        
        def run_audit():
            try:
                self._update_section_status(self.audit_status, "Running audit...", COLORS['yellow'])
                self.audit_results.value = "Audit in progress..."
                self.page.update()
                
                mapping_key = self.audit_mapping_dropdown.value
                ssc_app, aviator_app = mapping_key.split('|')
                
                success, result = AviatorService.run_audit(ssc_app, aviator_app)
                
                if success:
                    self.audit_results.value = f"Audit completed successfully!\n\nOutput:\n{result}"
                    self._update_section_status(self.audit_status, "Audit completed successfully!", COLORS['success_green'])
                else:
                    self.audit_results.value = f"Audit failed!\n\nError:\n{result}"
                    self._update_section_status(self.audit_status, f"Audit failed: {result}", COLORS['error_red'])
                
                self.page.update()
                    
            except Exception as e:
                error_msg = f"Audit failed: {str(e)}"
                self.audit_results.value = error_msg
                self._update_section_status(self.audit_status, error_msg, COLORS['error_red'])
                self.page.update()
        
        threading.Thread(target=run_audit, daemon=True).start()
    
    def _update_section_status(self, status_text: ft.Text, message: str, color: str):
        """Update section-specific status message"""
        update_status(status_text, message, color, self.page)