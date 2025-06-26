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
from utils.logger import setup_logger, log_user_action, log_exception

# Set up logging
logger = setup_logger(__name__)


class SetupTab:
    """Setup and Configuration Tab (Steps 1-4)"""
    
    def __init__(self, page: ft.Page, config_manager: ConfigManager):
        logger.debug("Initializing SetupTab")
        self.page = page
        self.config = config_manager
        self.container = None
        
        # Individual status texts for each section
        self.prerequisites_status = ft.Text("", color=COLORS['dark_gray'])
        self.key_gen_status = ft.Text("", color=COLORS['dark_gray'])
        self.server_config_status = ft.Text("", color=COLORS['dark_gray'])
        self.token_gen_status = ft.Text("", color=COLORS['dark_gray'])
        
        # File pickers
        self._setup_file_pickers()
        
        # Form fields
        self._setup_form_fields()
        
        logger.info("SetupTab initialized successfully")
    
    def _setup_file_pickers(self):
        """Initialize all file pickers"""
        # File picker for key generation
        self.key_file_picker = ft.FilePicker(
            on_result=self._on_key_file_picker_result
        )
        self.page.overlay.append(self.key_file_picker)
        
        # File picker for loading existing private key
        self.load_private_key_picker = ft.FilePicker(
            on_result=self._on_load_private_key_result
        )
        self.page.overlay.append(self.load_private_key_picker)
        
        # File picker for loading existing public key
        self.load_public_key_picker = ft.FilePicker(
            on_result=self._on_load_public_key_result
        )
        self.page.overlay.append(self.load_public_key_picker)
        
        # File picker for token generation
        self.token_file_picker = ft.FilePicker(
            on_result=self._on_token_file_picker_result
        )
        self.page.overlay.append(self.token_file_picker)
        
        # File picker for loading existing token
        self.load_token_picker = ft.FilePicker(
            on_result=self._on_load_token_result
        )
        self.page.overlay.append(self.load_token_picker)
    
    def _setup_form_fields(self):
        """Initialize all form fields"""
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
        logger.debug("Building SetupTab UI")
        
        # Create scrollable column with all sections
        scrollable_content = ft.Column(
            [
                ft.Text("Setup and Configuration", size=24, weight=ft.FontWeight.BOLD, color=COLORS['electric_blue']),
                ft.Text("Complete these steps to configure your SAST Aviator environment", 
                       size=14, color=COLORS['dark_gray'], italic=True),
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
            scroll=ft.ScrollMode.AUTO,
            expand=True
        )
        
        # Wrap in container with proper constraints
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
        help_text = ft.Container(
            content=ft.Text(
                "ℹ️ Prerequisites are checked automatically on startup. Ensure you have:\n"
                "• FCLI version 3.5.1 or higher installed\n"
                "• OpenSSL installed and accessible from command line\n"
                "• Network connectivity to download dependencies if needed",
                size=12,
                color=COLORS['dark_gray']
            ),
            bgcolor=COLORS['light_blue'],
            border_radius=5,
            padding=10
        )
        
        return create_section_container(
            "Step 1: Prerequisites Check",
            [
                help_text,
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
        """Build key generation section with import options"""
        help_text = ft.Container(
            content=ft.Text(
                "🔐 Generate new RSA 4096-bit key pair OR load existing keys:\n"
                "• Option 1: Generate new keys (recommended for first-time setup)\n"
                "• Option 2: Load existing private/public key pair from previous setup\n"
                "• Private key stays with you - never share it\n"
                "• Public key will be displayed below - share this with your PM",
                size=12,
                color=COLORS['dark_gray']
            ),
            padding=10,
            bgcolor=COLORS['light_blue'],
            border_radius=5
        )
        
        # Tab for Generate vs Load
        key_tabs = ft.Tabs(
            selected_index=0,
            tabs=[
                ft.Tab(
                    text="Generate New Keys",
                    content=ft.Container(
                        content=ft.Column([
                            ft.Row([
                                self.private_key_path,
                                create_button("Browse", self._browse_key_path, COLORS['cobalt_blue'], COLORS['white'])
                            ]),
                            create_button("Generate RSA 4096 Key Pair", self._generate_keys, 
                                        COLORS['electric_blue'], COLORS['white'], 250),
                        ]),
                        padding=ft.padding.only(top=10)
                    )
                ),
                ft.Tab(
                    text="Load Existing Keys",
                    content=ft.Container(
                        content=ft.Column([
                            ft.Row([
                                create_button("Load Private Key", self._browse_load_private_key, 
                                            COLORS['cobalt_blue'], COLORS['white'], 150),
                                create_button("Load Public Key", self._browse_load_public_key, 
                                            COLORS['cobalt_blue'], COLORS['white'], 150),
                            ]),
                            ft.Text("Loaded key paths will appear in the fields above", 
                                   size=12, color=COLORS['dark_gray'], italic=True)
                        ]),
                        padding=ft.padding.only(top=10)
                    )
                )
            ],
            height=150
        )
        
        return create_section_container(
            "Step 2: Key Generation / Import",
            [
                help_text,
                key_tabs,
                self.key_gen_status,
                self.public_key_display
            ],
            COLORS['cobalt_blue'],
            COLORS['light_gray']
        )
    
    def _build_server_config_section(self) -> ft.Container:
        """Build server configuration section"""
        help_text = ft.Container(
            content=ft.Text(
                "🌐 Configure connection to your Aviator server:\n"
                "• Server URL: Usually https://ams.aviator.fortify.com (or your organization's URL)\n"
                "• Tenant: Your organization's tenant name (e.g., demo_presales)\n"
                "• Ensure your private key from Step 2 is available\n"
                "• This establishes secure communication with the Aviator service",
                size=12,
                color=COLORS['dark_gray']
            ),
            padding=10,
            bgcolor=COLORS['light_blue'],
            border_radius=5
        )
        
        return create_section_container(
            "Step 3: Server Configuration",
            [
                help_text,
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
        """Build token generation section with import option"""
        help_text = ft.Container(
            content=ft.Text(
                "🎟️ Generate new authentication token OR load existing token:\n"
                "• Option 1: Generate new token (requires completed server config)\n"
                "• Option 2: Load existing token JSON file from previous setup\n"
                "• Keep token file secure - it's your key to the service",
                size=12,
                color=COLORS['dark_gray']
            ),
            padding=10,
            bgcolor=COLORS['light_blue'],
            border_radius=5
        )
        
        # Tab for Generate vs Load
        token_tabs = ft.Tabs(
            selected_index=0,
            tabs=[
                ft.Tab(
                    text="Generate New Token",
                    content=ft.Container(
                        content=ft.Column([
                            self.email,
                            self.token_name,
                            ft.Row([
                                self.token_file_path,
                                create_button("Browse", self._browse_token_path, COLORS['cobalt_blue'], COLORS['white'])
                            ]),
                            create_button("Generate Token", self._generate_token, 
                                        COLORS['electric_blue'], COLORS['white']),
                        ]),
                        padding=ft.padding.only(top=10)
                    )
                ),
                ft.Tab(
                    text="Load Existing Token",
                    content=ft.Container(
                        content=ft.Column([
                            create_button("Load Token File", self._browse_load_token, 
                                        COLORS['cobalt_blue'], COLORS['white'], 150),
                            ft.Text("Loaded token path will appear in the field above", 
                                   size=12, color=COLORS['dark_gray'], italic=True)
                        ]),
                        padding=ft.padding.only(top=10)
                    )
                )
            ],
            height=250
        )
        
        return create_section_container(
            "Step 4: Token Generation / Import",
            [
                help_text,
                token_tabs,
                self.token_gen_status
            ],
            COLORS['cobalt_blue'],
            COLORS['light_gray']
        )
    
    # File picker handlers for loading existing files
    def _browse_load_private_key(self, e):
        """Browse for existing private key"""
        log_user_action(logger, "Browse for existing private key")
        try:
            self.load_private_key_picker.pick_files(
                dialog_title="Select existing private key file",
                allowed_extensions=["pem", "key"],
                file_type=ft.FilePickerFileType.CUSTOM
            )
        except Exception as ex:
            log_exception(logger, ex, "browse_load_private_key")
            self._update_section_status(self.key_gen_status, 
                                      f"Error opening file picker: {str(ex)}", 
                                      COLORS['error_red'])
    
    def _on_load_private_key_result(self, e: ft.FilePickerResultEvent):
        """Handle loading existing private key"""
        if e.files and len(e.files) > 0:
            file_path = e.files[0].path
            self.private_key_path.value = file_path
            self.config.set('server', 'private_key_path', file_path)
            log_user_action(logger, "Loaded private key", {"path": file_path})
            self._update_section_status(self.key_gen_status, 
                                      f"Private key loaded: {file_path}", 
                                      COLORS['success_green'])
            
            # Try to load corresponding public key
            self._auto_load_public_key(file_path)
        else:
            logger.debug("No private key file selected")
        self.page.update()
    
    def _browse_load_public_key(self, e):
        """Browse for existing public key"""
        log_user_action(logger, "Browse for existing public key")
        try:
            self.load_public_key_picker.pick_files(
                dialog_title="Select existing public key file",
                allowed_extensions=["pem", "pub", "key"],
                file_type=ft.FilePickerFileType.CUSTOM
            )
        except Exception as ex:
            log_exception(logger, ex, "browse_load_public_key")
            self._update_section_status(self.key_gen_status, 
                                      f"Error opening file picker: {str(ex)}", 
                                      COLORS['error_red'])
    
    def _on_load_public_key_result(self, e: ft.FilePickerResultEvent):
        """Handle loading existing public key"""
        if e.files and len(e.files) > 0:
            file_path = e.files[0].path
            success, content = AviatorService.read_public_key(file_path)
            if success:
                self.public_key_display.value = content
                log_user_action(logger, "Loaded public key", {"path": file_path})
                self._update_section_status(self.key_gen_status, 
                                          "Public key loaded successfully!", 
                                          COLORS['success_green'])
            else:
                logger.error(f"Failed to read public key: {content}")
                self._update_section_status(self.key_gen_status, content, COLORS['error_red'])
        else:
            logger.debug("No public key file selected")
        self.page.update()
    
    def _auto_load_public_key(self, private_key_path: str):
        """Try to automatically load corresponding public key"""
        try:
            # Try common public key naming patterns
            private_path = Path(private_key_path)
            possible_public_paths = [
                private_path.with_suffix('').with_suffix('.pub'),
                private_path.parent / f"{private_path.stem}_public.pem",
                private_path.parent / f"{private_path.stem}.pub",
                private_path.parent / "public_key.pem"
            ]
            
            for pub_path in possible_public_paths:
                if pub_path.exists():
                    success, content = AviatorService.read_public_key(str(pub_path))
                    if success:
                        self.public_key_display.value = content
                        logger.info(f"Auto-loaded public key from {pub_path}")
                        self._update_section_status(self.key_gen_status, 
                                                  f"Keys loaded successfully!", 
                                                  COLORS['success_green'])
                        break
        except Exception as e:
            logger.debug(f"Could not auto-load public key: {str(e)}")
    
    def _browse_load_token(self, e):
        """Browse for existing token file"""
        log_user_action(logger, "Browse for existing token")
        try:
            self.load_token_picker.pick_files(
                dialog_title="Select existing token file",
                allowed_extensions=["json"],
                file_type=ft.FilePickerFileType.CUSTOM
            )
        except Exception as ex:
            log_exception(logger, ex, "browse_load_token")
            self._update_section_status(self.token_gen_status, 
                                      f"Error opening file picker: {str(ex)}", 
                                      COLORS['error_red'])
    
    def _on_load_token_result(self, e: ft.FilePickerResultEvent):
        """Handle loading existing token"""
        if e.files and len(e.files) > 0:
            file_path = e.files[0].path
            self.token_file_path.value = file_path
            self.config.set('tokens', 'current_token_file', file_path)
            log_user_action(logger, "Loaded token", {"path": file_path})
            self._update_section_status(self.token_gen_status, 
                                      f"Token loaded: {file_path}", 
                                      COLORS['success_green'])
            
            # Try to extract email from token if possible
            try:
                import json
                with open(file_path, 'r') as f:
                    token_data = json.load(f)
                    if 'email' in token_data:
                        self.email.value = token_data['email']
                        self.config.set('tokens', 'token_email', token_data['email'])
                        logger.debug(f"Extracted email from token: {token_data['email']}")
            except:
                pass
        else:
            logger.debug("No token file selected")
        self.page.update()
    
    # Existing methods with added logging
    def _validate_server_url(self, e):
        """Validate server URL format"""
        if not Validators.validate_url(self.server_url.value):
            self.server_url.error_text = "Invalid URL format"
            logger.debug(f"Invalid URL format: {self.server_url.value}")
        else:
            self.server_url.error_text = None
        self.page.update()
    
    def _validate_email(self, e):
        """Validate email format"""
        if not Validators.validate_email(self.email.value):
            self.email.error_text = "Invalid email format"
            logger.debug(f"Invalid email format: {self.email.value}")
        else:
            self.email.error_text = None
        self.page.update()
    
    def _check_fcli(self, e):
        """Check FCLI installation"""
        log_user_action(logger, "Check FCLI")
        success, message = FCLIService.check_fcli_version()
        self._update_section_status(self.prerequisites_status, message, 
                                  COLORS['success_green'] if success else COLORS['error_red'])
    
    def _check_openssl(self, e):
        """Check OpenSSL installation"""
        log_user_action(logger, "Check OpenSSL")
        success, message = FCLIService.check_openssl()
        self._update_section_status(self.prerequisites_status, message, 
                                  COLORS['success_green'] if success else COLORS['error_red'])
    
    def _browse_key_path(self, e):
        """Browse for private key path"""
        log_user_action(logger, "Browse for key save path")
        try:
            self.key_file_picker.save_file(
                dialog_title="Select location to save private key",
                file_name="private_key.pem",
                allowed_extensions=["pem", "key"],
                file_type=ft.FilePickerFileType.CUSTOM
            )
        except Exception as ex:
            log_exception(logger, ex, "browse_key_path")
            self._update_section_status(self.key_gen_status, 
                                      f"Error opening file picker: {str(ex)}", 
                                      COLORS['error_red'])
    
    def _on_key_file_picker_result(self, e: ft.FilePickerResultEvent):
        """Handle key file picker result"""
        if e.path:
            self.private_key_path.value = e.path
            logger.debug(f"Key save path selected: {e.path}")
            self._update_section_status(self.key_gen_status, 
                                      f"Selected path: {e.path}", 
                                      COLORS['success_green'])
        else:
            logger.debug("No key save path selected")
            self._update_section_status(self.key_gen_status, 
                                      "No file selected", 
                                      COLORS['yellow'])
        self.page.update()
    
    def _browse_token_path(self, e):
        """Browse for token file path"""
        log_user_action(logger, "Browse for token save path")
        try:
            # Generate default token filename based on email if available
            default_name = "aviator_token.json"
            if self.email.value:
                email_part = self.email.value.split('@')[0]
                default_name = f"token_{email_part}.json"
            
            self.token_file_picker.save_file(
                dialog_title="Select location to save token file",
                file_name=default_name,
                allowed_extensions=["json"],
                file_type=ft.FilePickerFileType.CUSTOM
            )
        except Exception as ex:
            log_exception(logger, ex, "browse_token_path")
            self._update_section_status(self.token_gen_status, 
                                      f"Error opening file picker: {str(ex)}", 
                                      COLORS['error_red'])
    
    def _on_token_file_picker_result(self, e: ft.FilePickerResultEvent):
        """Handle token file picker result"""
        if e.path:
            self.token_file_path.value = e.path
            logger.debug(f"Token save path selected: {e.path}")
            self._update_section_status(self.token_gen_status, 
                                      f"Selected path: {e.path}", 
                                      COLORS['success_green'])
        else:
            logger.debug("No token save path selected")
            self._update_section_status(self.token_gen_status, 
                                      "No file selected", 
                                      COLORS['yellow'])
        self.page.update()
    
    def _generate_keys(self, e):
        """Generate RSA 4096-bit key pair"""
        log_user_action(logger, "Generate keys")
        
        def generate():
            try:
                self._update_section_status(self.key_gen_status, "Generating keys...", COLORS['yellow'])
                logger.info("Starting key generation")
                
                success, message = AviatorService.generate_keys(self.private_key_path.value)
                
                if success:
                    # Read and display public key
                    public_key_path = str(Path(self.private_key_path.value).with_suffix('')) + "_public.pem"
                    pub_success, pub_content = AviatorService.read_public_key(public_key_path)
                    
                    if pub_success:
                        self.public_key_display.value = pub_content
                        self.page.update()
                        logger.info("Public key loaded and displayed")
                    
                    self._update_section_status(self.key_gen_status, message, COLORS['success_green'])
                    self.config.set('server', 'private_key_path', self.private_key_path.value)
                    logger.info("Key generation completed successfully")
                else:
                    self._update_section_status(self.key_gen_status, message, COLORS['error_red'])
                    logger.error(f"Key generation failed: {message}")
                    
            except Exception as e:
                log_exception(logger, e, "generate_keys")
                self._update_section_status(self.key_gen_status, 
                                          f"Key generation failed: {str(e)}", COLORS['error_red'])
        
        threading.Thread(target=generate, daemon=True).start()
    
    def _configure_server(self, e):
        """Configure FCLI server settings"""
        log_user_action(logger, "Configure server", {
            "url": self.server_url.value,
            "tenant": self.tenant.value
        })
        
        if not Validators.validate_url(self.server_url.value):
            self._update_section_status(self.server_config_status, 
                                      "Please enter a valid server URL", COLORS['error_red'])
            return
        
        def configure():
            try:
                self._update_section_status(self.server_config_status, "Configuring server...", COLORS['yellow'])
                logger.info(f"Configuring server: {self.server_url.value}")
                
                success, message = AviatorService.configure_server(
                    self.server_url.value,
                    self.tenant.value,
                    self.private_key_path.value
                )
                
                if success:
                    self._update_section_status(self.server_config_status, message, COLORS['success_green'])
                    self.config.set('server', 'url', self.server_url.value)
                    self.config.set('server', 'tenant', self.tenant.value)
                    logger.info("Server configuration completed successfully")
                else:
                    self._update_section_status(self.server_config_status, message, COLORS['error_red'])
                    logger.error(f"Server configuration failed: {message}")
                    
            except Exception as e:
                log_exception(logger, e, "configure_server")
                self._update_section_status(self.server_config_status, 
                                          f"Configuration failed: {str(e)}", COLORS['error_red'])
        
        threading.Thread(target=configure, daemon=True).start()
    
    def _generate_token(self, e):
        """Generate Aviator token"""
        log_user_action(logger, "Generate token", {
            "email": self.email.value,
            "token_name": self.token_name.value
        })
        
        if not Validators.validate_email(self.email.value):
            self._update_section_status(self.token_gen_status, 
                                      "Please enter a valid email address", COLORS['error_red'])
            return
        
        def generate():
            try:
                self._update_section_status(self.token_gen_status, "Generating token...", COLORS['yellow'])
                logger.info(f"Generating token for {self.email.value}")
                
                success, message = AviatorService.generate_token(
                    self.email.value,
                    self.token_name.value,
                    self.token_file_path.value
                )
                
                if success:
                    self._update_section_status(self.token_gen_status, message, COLORS['success_green'])
                    self.config.set('tokens', 'current_token_file', self.token_file_path.value)
                    self.config.set('tokens', 'token_email', self.email.value)
                    logger.info("Token generation completed successfully")
                else:
                    self._update_section_status(self.token_gen_status, message, COLORS['error_red'])
                    logger.error(f"Token generation failed: {message}")
                    
            except Exception as e:
                log_exception(logger, e, "generate_token")
                self._update_section_status(self.token_gen_status, 
                                          f"Token generation failed: {str(e)}", COLORS['error_red'])
        
        threading.Thread(target=generate, daemon=True).start()
    
    def _auto_check_prerequisites(self):
        """Automatically check prerequisites on application startup"""
        def check_all():
            try:
                logger.info("Running automatic prerequisites check")
                
                # Check FCLI
                fcli_success, fcli_message = FCLIService.check_fcli_version()
                
                # Check OpenSSL
                ssl_success, ssl_message = FCLIService.check_openssl()
                
                # Combine results
                if fcli_success and ssl_success:
                    combined_message = f"✓ FCLI: {fcli_message}\n✓ OpenSSL: {ssl_message}"
                    color = COLORS['success_green']
                    logger.info("All prerequisites satisfied")
                elif fcli_success or ssl_success:
                    combined_message = f"{'✓' if fcli_success else '✗'} FCLI: {fcli_message}\n{'✓' if ssl_success else '✗'} OpenSSL: {ssl_message}"
                    color = COLORS['yellow']
                    logger.warning("Some prerequisites missing")
                else:
                    combined_message = f"✗ FCLI: {fcli_message}\n✗ OpenSSL: {ssl_message}"
                    color = COLORS['error_red']
                    logger.error("Prerequisites not satisfied")
                
                self._update_section_status(self.prerequisites_status, combined_message, color)
                
            except Exception as e:
                log_exception(logger, e, "auto_check_prerequisites")
                self._update_section_status(self.prerequisites_status, 
                                          f"Error checking prerequisites: {str(e)}", 
                                          COLORS['error_red'])
        
        # Run in background thread to avoid blocking UI
        threading.Thread(target=check_all, daemon=True).start()
    
    def _update_section_status(self, status_text: ft.Text, message: str, color: str):
        """Update section-specific status message"""
        update_status(status_text, message, color, self.page)
        logger.debug(f"Status update: {message}")