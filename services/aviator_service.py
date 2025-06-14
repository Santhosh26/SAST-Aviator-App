"""Aviator-specific operations service"""

import json
from pathlib import Path
from typing import Dict, List, Tuple
from .fcli_service import FCLIService


class AviatorService:
    """Handles Aviator-specific operations"""
    
    @staticmethod
    def generate_keys(private_key_path: str) -> Tuple[bool, str]:
        """Generate RSA 4096-bit key pair"""
        try:
            # Ensure the directory exists
            private_key_path_obj = Path(private_key_path)
            private_key_path_obj.parent.mkdir(parents=True, exist_ok=True)
            
            # Use absolute paths
            private_key_abs = str(private_key_path_obj.absolute())
            public_key_abs = str(private_key_path_obj.with_suffix('').absolute()) + "_public.pem"
            
            # Generate private key
            success1, stdout1, stderr1 = FCLIService.run_command([
                'openssl', 'genpkey', '-algorithm', 'RSA',
                '-pkeyopt', 'rsa_keygen_bits:4096',
                '-out', private_key_abs
            ])
            
            if not success1:
                return False, f"Failed to generate private key: {stderr1}"
            
            # Generate public key
            success2, stdout2, stderr2 = FCLIService.run_command([
                'openssl', 'rsa', '-in', private_key_abs,
                '-pubout', '-out', public_key_abs
            ])
            
            if not success2:
                return False, f"Failed to generate public key: {stderr2}"
            
            return True, f"Key pair generated successfully! Private: {private_key_abs}, Public: {public_key_abs}"
            
        except Exception as e:
            return False, f"Key generation failed: {str(e)}"
    
    @staticmethod
    def read_public_key(public_key_path: str) -> Tuple[bool, str]:
        """Read public key content"""
        try:
            with open(public_key_path, 'r') as f:
                content = f.read()
            return True, content
        except Exception as e:
            return False, f"Failed to read public key: {str(e)}"
    
    @staticmethod
    def configure_server(url: str, tenant: str, private_key_path: str) -> Tuple[bool, str]:
        """Configure Aviator server"""
        command = [
            'fcli', 'aviator', 'admin-config', 'create',
            '--url', url,
            '--tenant', tenant,
            '--private-key', private_key_path
        ]
        
        success, stdout, stderr = FCLIService.run_command(command)
        if success:
            return True, "Server configured successfully!"
        else:
            return False, f"Server configuration failed: {stderr}"
    
    @staticmethod
    def generate_token(email: str, token_name: str, token_file_path: str) -> Tuple[bool, str]:
        """Generate Aviator token"""
        command = [
            'fcli', 'aviator', 'token', 'create',
            '--email', email,
            '--name', token_name,
            '--save-token', token_file_path
        ]
        
        success, stdout, stderr = FCLIService.run_command(command)
        if success:
            return True, "Token generated successfully!"
        else:
            return False, f"Token generation failed: {stderr}"
    
    @staticmethod
    def login(server_url: str, token_file: str) -> Tuple[bool, str]:
        """Login to Aviator"""
        command = [
            'fcli', 'aviator', 'session', 'login',
            '--url', server_url,
            '--token', token_file
        ]
        
        success, stdout, stderr = FCLIService.run_command(command)
        if success:
            return True, "Aviator login successful!"
        else:
            return False, f"Aviator login failed: {stderr}"
    
    @staticmethod
    def create_app(app_name: str) -> Tuple[bool, str]:
        """Create new Aviator application"""
        command = ['fcli', 'aviator', 'app', 'create', app_name]
        success, stdout, stderr = FCLIService.run_command(command)
        
        if success:
            return True, f"Aviator app '{app_name}' created!"
        else:
            return False, f"App creation failed: {stderr}"
    
    @staticmethod
    def list_apps() -> Tuple[bool, List[Dict], str]:
        """List Aviator applications"""
        command = ['fcli', 'aviator', 'app', 'list', '--output', 'json']
        success, stdout, stderr = FCLIService.run_command(command)
        
        if success:
            try:
                apps_data = json.loads(stdout)
                return True, apps_data, ""
            except json.JSONDecodeError:
                return False, [], "Failed to parse Aviator apps response"
        else:
            return False, [], f"Failed to list Aviator apps: {stderr}"
    
    @staticmethod
    def run_audit(ssc_app: str, aviator_app: str) -> Tuple[bool, str]:
        """Run audit on application mapping"""
        command = [
            'fcli', 'aviator', 'ssc', 'audit',
            '--av', ssc_app,
            '--app', aviator_app
        ]
        
        success, stdout, stderr = FCLIService.run_command(command, timeout=300)  # 5 minute timeout for audits
        
        if success:
            return True, stdout
        else:
            return False, stderr