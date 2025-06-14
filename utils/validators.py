"""Input validation utilities"""

import re
from urllib.parse import urlparse


class Validators:
    """Input validation methods"""
    
    @staticmethod
    def validate_url(url: str) -> bool:
        """Validate URL format"""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email address format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_file_path(path: str) -> bool:
        """Validate file path format"""
        # Basic validation - can be enhanced based on OS
        return len(path) > 0 and not path.startswith(' ') and not path.endswith(' ')
    
    @staticmethod
    def validate_app_name(name: str) -> bool:
        """Validate application name"""
        # Allow alphanumeric, spaces, hyphens, and underscores
        pattern = r'^[a-zA-Z0-9\s\-_]+$'
        return bool(name) and re.match(pattern, name) is not None