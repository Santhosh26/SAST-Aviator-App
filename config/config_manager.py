"""Configuration manager for application settings with logging"""

import configparser
from pathlib import Path
from utils.logger import setup_logger

# Set up logging
logger = setup_logger(__name__)


class ConfigManager:
    """Manages application configuration using config.ini with comprehensive logging"""
    
    def __init__(self):
        self.config_path = Path('config.ini')
        self.config = configparser.ConfigParser()
        logger.info(f"Initializing ConfigManager with config path: {self.config_path}")
        self.load_config()
    
    def load_config(self):
        """Load configuration from file"""
        if self.config_path.exists():
            logger.info(f"Loading existing configuration from {self.config_path}")
            try:
                self.config.read(self.config_path)
                logger.debug(f"Configuration sections loaded: {self.config.sections()}")
            except Exception as e:
                logger.error(f"Failed to load configuration: {str(e)}", exc_info=True)
                self.create_default_config()
        else:
            logger.info("No existing configuration found, creating default")
            self.create_default_config()
    
    def create_default_config(self):
        """Create default configuration"""
        logger.info("Creating default configuration")
        
        self.config['server'] = {
            'url': '',
            'tenant': '',
            'private_key_path': './private_key.pem'
        }
        self.config['tokens'] = {
            'current_token_file': './sast_aviator_token.json',
            'token_email': ''
        }
        self.config['ssc'] = {
            'url': '',
            'username': '',
            'last_session': ''
        }
        self.config['app_mappings'] = {}
        
        self.save_config()
        logger.info("Default configuration created and saved")
    
    def save_config(self):
        """Save configuration to file"""
        try:
            with open(self.config_path, 'w') as f:
                self.config.write(f)
            logger.debug(f"Configuration saved to {self.config_path}")
        except Exception as e:
            logger.error(f"Failed to save configuration: {str(e)}", exc_info=True)
    
    def get(self, section: str, key: str, fallback: str = '') -> str:
        """Get configuration value with logging"""
        try:
            value = self.config.get(section, key, fallback=fallback)
            logger.debug(f"Config get: [{section}][{key}] = {value}")
            return value
        except Exception as e:
            logger.warning(f"Failed to get config [{section}][{key}]: {str(e)}, using fallback: {fallback}")
            return fallback
    
    def set(self, section: str, key: str, value: str):
        """Set configuration value with logging"""
        try:
            if section not in self.config:
                self.config[section] = {}
                logger.debug(f"Created new config section: {section}")
            
            old_value = self.config[section].get(key, '<not set>')
            self.config[section][key] = value
            self.save_config()
            
            logger.info(f"Config updated: [{section}][{key}] = {value} (was: {old_value})")
        except Exception as e:
            logger.error(f"Failed to set config [{section}][{key}] = {value}: {str(e)}", exc_info=True)
    
    def get_all_mappings(self):
        """Get all application mappings with logging"""
        try:
            if 'app_mappings' in self.config:
                mappings = dict(self.config['app_mappings'])
                logger.debug(f"Retrieved {len(mappings)} app mappings")
                return mappings
            logger.debug("No app_mappings section found, returning empty dict")
            return {}
        except Exception as e:
            logger.error(f"Failed to get app mappings: {str(e)}", exc_info=True)
            return {}
    
    def add_mapping(self, ssc_app: str, aviator_app: str):
        """Add an application mapping with logging"""
        try:
            self.set('app_mappings', ssc_app, aviator_app)
            logger.info(f"Added app mapping: {ssc_app} -> {aviator_app}")
        except Exception as e:
            logger.error(f"Failed to add mapping {ssc_app} -> {aviator_app}: {str(e)}", exc_info=True)
    
    def remove_mapping(self, ssc_app: str):
        """Remove an application mapping with logging"""
        try:
            if 'app_mappings' in self.config and ssc_app in self.config['app_mappings']:
                aviator_app = self.config['app_mappings'][ssc_app]
                del self.config['app_mappings'][ssc_app]
                self.save_config()
                logger.info(f"Removed app mapping: {ssc_app} -> {aviator_app}")
            else:
                logger.warning(f"Attempted to remove non-existent mapping: {ssc_app}")
        except Exception as e:
            logger.error(f"Failed to remove mapping {ssc_app}: {str(e)}", exc_info=True)