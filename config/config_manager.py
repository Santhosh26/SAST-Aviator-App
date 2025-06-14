"""Configuration manager for application settings"""

import configparser
from pathlib import Path


class ConfigManager:
    """Manages application configuration using config.ini"""
    
    def __init__(self):
        self.config_path = Path('config.ini')
        self.config = configparser.ConfigParser()
        self.load_config()
    
    def load_config(self):
        """Load configuration from file"""
        if self.config_path.exists():
            self.config.read(self.config_path)
        else:
            self.create_default_config()
    
    def create_default_config(self):
        """Create default configuration"""
        self.config['server'] = {
            'url': 'https://ams.aviator.fortify.com',
            'tenant': 'demo_presales',
            'private_key_path': './private_key.pem'
        }
        self.config['tokens'] = {
            'current_token_file': './token_meapresales.json',
            'token_email': ''
        }
        self.config['ssc'] = {
            'url': 'http://10.0.1.203:8080/ssc',
            'username': 'admin',
            'last_session': ''
        }
        self.config['app_mappings'] = {}
        self.save_config()
    
    def save_config(self):
        """Save configuration to file"""
        with open(self.config_path, 'w') as f:
            self.config.write(f)
    
    def get(self, section: str, key: str, fallback: str = '') -> str:
        """Get configuration value"""
        return self.config.get(section, key, fallback=fallback)
    
    def set(self, section: str, key: str, value: str):
        """Set configuration value"""
        if section not in self.config:
            self.config[section] = {}
        self.config[section][key] = value
        self.save_config()
    
    def get_all_mappings(self):
        """Get all application mappings"""
        if 'app_mappings' in self.config:
            return dict(self.config['app_mappings'])
        return {}
    
    def add_mapping(self, ssc_app: str, aviator_app: str):
        """Add an application mapping"""
        self.set('app_mappings', ssc_app, aviator_app)
    
    def remove_mapping(self, ssc_app: str):
        """Remove an application mapping"""
        if 'app_mappings' in self.config and ssc_app in self.config['app_mappings']:
            del self.config['app_mappings'][ssc_app]
            self.save_config()