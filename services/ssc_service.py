"""SSC-specific operations service"""

import json
from typing import Dict, List, Tuple
from .fcli_service import FCLIService


class SSCService:
    """Handles SSC-specific operations"""
    
    @staticmethod
    def login(url: str, username: str, password: str) -> Tuple[bool, str]:
        """Login to SSC"""
        command = [
            'fcli', 'ssc', 'session', 'login',
            '--url', url,
            '-u', username,
            '-p', password
        ]
        
        success, stdout, stderr = FCLIService.run_command(command)
        
        if success:
            return True, "SSC login successful!"
        else:
            return False, f"SSC login failed: {stderr}"
    
    @staticmethod
    def list_applications() -> Tuple[bool, List[Dict], str]:
        """List SSC applications"""
        command = ['fcli', 'ssc', 'appversion', 'ls', '--output', 'json']
        success, stdout, stderr = FCLIService.run_command(command)
        
        if success:
            try:
                apps_data = json.loads(stdout)
                return True, apps_data, ""
            except json.JSONDecodeError:
                return False, [], "Failed to parse SSC apps response"
        else:
            return False, [], f"Failed to list SSC apps: {stderr}"