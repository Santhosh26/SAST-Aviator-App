"""Setup and Configuration Tab UI"""

import flet as ft
import threading
from pathlib import Path
from datetime import datetime

from config.config_manager import ConfigManager
from services.fcli_service import FCLIService
from services.aviator_service import AviatorService
from utils.constants import COLORS
from utils.validators import Validators
from utils.helpers import update_status, create_section_container, create_button


class SetupTab:
    """Setup and Configuration Tab (Steps 1-4)"""
    
    def __init__(self, page: ft.Page, config_manager: ConfigManager):
        self.page = page
        self.config = config_manager
        self.container = None
        
        # Individual status texts for each section
        self.prerequisites_status = ft.Text("", color=COLORS['dark_gray'])
        self.key_gen_status = ft.Text("", color=COLORS['dark_gray'])
        self.server_config_status = ft.Text("", color=COLORS['dark_gray'])
        self.token_gen_status = ft.Text("", color=COLORS['dark_gray'])
        
        # File picker for key generation
        self.key_file_picker = ft.FilePicker(
            on_result=self._on_key_file_picker_result
        )
        self.page.overlay.append(self.key_file_picker)
        
        # File picker for token generation
        self.token_file_picker = ft.FilePicker(
            on_result=self._on_token_file_picker_result
        )
        self.page.overlay.append(self.token_file_picker)
        
        # Form fields
        self.server_url = ft.TextField(
            label="Server URL",
            value=self.config.get('server', 'url'),
            width=400,
            on_change=self._validate_server_url
        )
        self.tenant = ft.TextField(
            label="Tenant",
            value=self.config.get('server', 'tenant'),
            width=400
        )
        self.private_key_path = ft.TextField(
            label="Private Key Path",
            value=self.config.get('server', 'private_key_path'),
            width=400
        )
        self.email = ft.TextField(
            label="Email Address",
            value=self.config.get('tokens', 'token_email'),
            width=400,
            on_change=self._validate_email
        )
        self.token_name = ft.TextField(
            label="Token Name",
            value="aviator_token",
            width=400
        )
        self.token_file_path = ft.TextField(
            label="Token Save Path",
            value=self.config.get('tokens', 'current_token_file'),
            width=400
        )
        
        self.public_key_display = ft.TextField(
            label="Public Key (Share with PM)",
            multiline=True,
            min_lines=5,
            max_lines=8,
            read_only=True,
            width=600
        )
    
    def build(self) -> ft.Container:
        """Build the setup tab UI"""
        # Create scrollable column with all sections
        scrollable_content = ft.Column(
            [
                ft.Text("Setup and Configuration", size=24, weight=ft.FontWeight.BOLD, color=COLORS['electric_blue']),
                ft.Divider(),
                
                # Step 1: Prerequisites Check
                self._build_prerequisites_section(),
                ft.Divider(height=20),
                
                # Step 2: Key Generation
                self._build_key_generation_section(),
                ft.Divider(height=20),
                
                # Step 3: Server Configuration
                self._build_server_config_section(),
                ft.Divider(height=20),
                
                # Step 4: Token Generation
                self._build_token_section(),
                
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
        
        # Automatically check prerequisites on startup
        self._auto_check_prerequisites()
        
        return self.container
    
    def _build_prerequisites_section(self) -> ft.Container:
        """Build prerequisites check section"""
        return create_section_container(
            "Step 1: Prerequisites Check",
            [
                ft.Row([
                    create_button("Check FCLI", self._check_fcli, COLORS['electric_blue'], COLORS['white']),
                    create_button("Check OpenSSL", self._check_openssl, COLORS['electric_blue'], COLORS['white'])
                ]),
                self.prerequisites_status
            ],
            COLORS['cobalt_blue'],
            COLORS['light_gray']
        )
    
    def _build_key_generation_section(self) -> ft.Container:
        """Build key generation section"""
        return create_section_container(
            "Step 2: Key Generation",
            [
                ft.Row([
                    self.private_key_path,
                    create_button("Browse", self._browse_key_path, COLORS['cobalt_blue'], COLORS['white'])
                ]),
                create_button("Generate RSA 4096 Key Pair", self._generate_keys, 
                            COLORS['electric_blue'], COLORS['white'], 250),
                self.key_gen_status,
                self.public_key_display
            ],
            COLORS['cobalt_blue'],
            COLORS['light_gray']
        )
    
    def _build_server_config_section(self) -> ft.Container:
        """Build server configuration section"""
        return create_section_container(
            "Step 3: Server Configuration",
            [
                self.server_url,
                self.tenant,
                create_button("Configure Server", self._configure_server, 
                            COLORS['electric_blue'], COLORS['white']),
                self.server_config_status
            ],
            COLORS['cobalt_blue'],
            COLORS['light_gray']
        )
    
    def _build_token_section(self) -> ft.Container:
        """Build token generation section"""
        return create_section_container(
            "Step 4: Token Generation",
            [
                self.email,
                self.token_name,
                ft.Row([
                    self.token_file_path,
                    create_button("Browse", self._browse_token_path, COLORS['cobalt_blue'], COLORS['white'])
                ]),
                create_button("Generate Token", self._generate_token, 
                            COLORS['electric_blue'], COLORS['white']),
                self.token_gen_status
            ],
            COLORS['cobalt_blue'],
            COLORS['light_gray']
        )
    
    def _validate_server_url(self, e):
        """Validate server URL format"""
        if not Validators.validate_url(self.server_url.value):
            self.server_url.error_text = "Invalid URL format"
        else:
            self.server_url.error_text = None
        self.page.update()
    
    def _validate_email(self, e):
        """Validate email format"""
        if not Validators.validate_email(self.email.value):
            self.email.error_text = "Invalid email format"
        else:
            self.email.error_text = None
        self.page.update()
    
    def _check_fcli(self, e):
        """Check FCLI installation"""
        success, message = FCLIService.check_fcli_version()
        self._update_section_status(self.prerequisites_status, message, 
                                  COLORS['success_green'] if success else COLORS['error_red'])
    
    def _check_openssl(self, e):
        """Check OpenSSL installation"""
        success, message = FCLIService.check_openssl()
        self._update_section_status(self.prerequisites_status, message, 
                                  COLORS['success_green'] if success else COLORS['error_red'])
    
    def _browse_key_path(self, e):
        """Browse for private key path"""
        try:
            self.key_file_picker.save_file(
                dialog_title="Select location to save private key",
                file_name="private_key.pem",
                allowed_extensions=["pem", "key"],
                file_type=ft.FilePickerFileType.CUSTOM
            )
        except Exception as ex:
            self._update_section_status(self.key_gen_status, 
                                      f"Error opening file picker: {str(ex)}", 
                                      COLORS['error_red'])
    
    def _on_key_file_picker_result(self, e: ft.FilePickerResultEvent):
        """Handle key file picker result"""
        if e.path:
            self.private_key_path.value = e.path
            self._update_section_status(self.key_gen_status, 
                                      f"Selected path: {e.path}", 
                                      COLORS['success_green'])
        else:
            self._update_section_status(self.key_gen_status, 
                                      "No file selected", 
                                      COLORS['yellow'])
        self.page.update()
    
    def _browse_token_path(self, e):
        """Browse for token file path"""
        try:
            # Generate default token filename based on email if available
            default_name = "aviator_token.json"
            if self.email.value:
                # Create filename from email (e.g., user@example.com -> token_user_example.json)
                email_part = self.email.value.split('@')[0]
                default_name = f"token_{email_part}.json"
            
            self.token_file_picker.save_file(
                dialog_title="Select location to save token file",
                file_name=default_name,
                allowed_extensions=["json"],
                file_type=ft.FilePickerFileType.CUSTOM
            )
        except Exception as ex:
            self._update_section_status(self.token_gen_status, 
                                      f"Error opening file picker: {str(ex)}", 
                                      COLORS['error_red'])
    
    def _generate_keys(self, e):
        """Generate RSA 4096-bit key pair"""
        def generate():
            try:
                self._update_section_status(self.key_gen_status, "Generating keys...", COLORS['yellow'])
                
                success, message = AviatorService.generate_keys(self.private_key_path.value)
                
                if success:
                    # Read and display public key
                    public_key_path = str(Path(self.private_key_path.value).with_suffix('')) + "_public.pem"
                    pub_success, pub_content = AviatorService.read_public_key(public_key_path)
                    
                    if pub_success:
                        self.public_key_display.value = pub_content
                        self.page.update()
                    
                    self._update_section_status(self.key_gen_status, message, COLORS['success_green'])
                    self.config.set('server', 'private_key_path', self.private_key_path.value)
                else:
                    self._update_section_status(self.key_gen_status, message, COLORS['error_red'])
                    
            except Exception as e:
                self._update_section_status(self.key_gen_status, 
                                          f"Key generation failed: {str(e)}", COLORS['error_red'])
        
        threading.Thread(target=generate, daemon=True).start()
    
    def _configure_server(self, e):
        """Configure FCLI server settings"""
        if not Validators.validate_url(self.server_url.value):
            self._update_section_status(self.server_config_status, 
                                      "Please enter a valid server URL", COLORS['error_red'])
            return
        
        def configure():
            try:
                self._update_section_status(self.server_config_status, "Configuring server...", COLORS['yellow'])
                
                success, message = AviatorService.configure_server(
                    self.server_url.value,
                    self.tenant.value,
                    self.private_key_path.value
                )
                
                if success:
                    self._update_section_status(self.server_config_status, message, COLORS['success_green'])
                    self.config.set('server', 'url', self.server_url.value)
                    self.config.set('server', 'tenant', self.tenant.value)
                else:
                    self._update_section_status(self.server_config_status, message, COLORS['error_red'])
                    
            except Exception as e:
                self._update_section_status(self.server_config_status, 
                                          f"Configuration failed: {str(e)}", COLORS['error_red'])
        
        threading.Thread(target=configure, daemon=True).start()
    
    def _generate_token(self, e):
        """Generate Aviator token"""
        if not Validators.validate_email(self.email.value):
            self._update_section_status(self.token_gen_status, 
                                      "Please enter a valid email address", COLORS['error_red'])
            return
        
        def generate():
            try:
                self._update_section_status(self.token_gen_status, "Generating token...", COLORS['yellow'])
                
                success, message = AviatorService.generate_token(
                    self.email.value,
                    self.token_name.value,
                    self.token_file_path.value
                )
                
                if success:
                    self._update_section_status(self.token_gen_status, message, COLORS['success_green'])
                    self.config.set('tokens', 'current_token_file', self.token_file_path.value)
                    self.config.set('tokens', 'token_email', self.email.value)
                else:
                    self._update_section_status(self.token_gen_status, message, COLORS['error_red'])
                    
            except Exception as e:
                self._update_section_status(self.token_gen_status, 
                                          f"Token generation failed: {str(e)}", COLORS['error_red'])
        
        threading.Thread(target=generate, daemon=True).start()
    
    def _auto_check_prerequisites(self):
        """Automatically check prerequisites on application startup"""
        def check_all():
            try:
                # Check FCLI
                fcli_success, fcli_message = FCLIService.check_fcli_version()
                
                # Check OpenSSL
                ssl_success, ssl_message = FCLIService.check_openssl()
                
                # Combine results
                if fcli_success and ssl_success:
                    combined_message = f"✓ FCLI: {fcli_message}\n✓ OpenSSL: {ssl_message}"
                    color = COLORS['success_green']
                elif fcli_success or ssl_success:
                    combined_message = f"{'✓' if fcli_success else '✗'} FCLI: {fcli_message}\n{'✓' if ssl_success else '✗'} OpenSSL: {ssl_message}"
                    color = COLORS['yellow']
                else:
                    combined_message = f"✗ FCLI: {fcli_message}\n✗ OpenSSL: {ssl_message}"
                    color = COLORS['error_red']
                
                self._update_section_status(self.prerequisites_status, combined_message, color)
                
            except Exception as e:
                self._update_section_status(self.prerequisites_status, 
                                          f"Error checking prerequisites: {str(e)}", 
                                          COLORS['error_red'])
        
        # Run in background thread to avoid blocking UI
        threading.Thread(target=check_all, daemon=True).start()
    
    def _update_section_status(self, status_text: ft.Text, message: str, color: str):
        """Update section-specific status message"""
        update_status(status_text, message, color, self.page)