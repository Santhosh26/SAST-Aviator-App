"""FCLI command execution service with comprehensive logging"""

import subprocess
import re
from typing import List, Tuple
from utils.logger import setup_logger, log_command_execution

# Set up logging
logger = setup_logger(__name__)


class FCLIService:
    """Handles FCLI command execution with logging"""
    
    @staticmethod
    def run_command(command: List[str], capture_output: bool = True, timeout: int = 30) -> Tuple[bool, str, str]:
        """Execute a command and return success, stdout, stderr"""
        logger.debug(f"Preparing to execute command: {' '.join(command)}")
        
        try:
            result = subprocess.run(
                command,
                capture_output=capture_output,
                text=True,
                timeout=timeout
            )
            
            success = result.returncode == 0
            stdout = result.stdout if capture_output else ""
            stderr = result.stderr if capture_output else ""
            
            # Log command execution details
            log_command_execution(logger, command, success, stdout, stderr)
            
            return success, stdout, stderr
            
        except subprocess.TimeoutExpired:
            logger.error(f"Command timed out after {timeout} seconds: {' '.join(command)}")
            return False, "", "Command timed out"
        except FileNotFoundError:
            logger.error(f"Command not found: {command[0]}")
            return False, "", f"Command not found: {command[0]}"
        except Exception as e:
            logger.error(f"Unexpected error executing command: {str(e)}", exc_info=True)
            return False, "", str(e)
    
    @staticmethod
    def check_fcli_version() -> Tuple[bool, str]:
        """Check if FCLI 3.5.1+ is installed"""
        logger.info("Checking FCLI version")
        
        success, stdout, stderr = FCLIService.run_command(['fcli', '--version'])
        if not success:
            error_msg = "FCLI not found. Please install FCLI 3.5.1 or later."
            logger.error(error_msg)
            return False, error_msg
        
        version_match = re.search(r'(\d+\.\d+\.\d+)', stdout)
        if version_match:
            version = version_match.group(1)
            major, minor, patch = map(int, version.split('.'))
            logger.info(f"FCLI version detected: {version}")
            
            if (major, minor, patch) >= (3, 5, 1):
                success_msg = f"FCLI {version} found ✓"
                logger.info(success_msg)
                return True, success_msg
            else:
                error_msg = f"FCLI {version} found, but 3.5.1+ required"
                logger.warning(error_msg)
                return False, error_msg
                
        error_msg = "Could not determine FCLI version"
        logger.error(error_msg)
        return False, error_msg
    
    @staticmethod
    def check_openssl() -> Tuple[bool, str]:
        """Check if OpenSSL is installed"""
        logger.info("Checking OpenSSL installation")
        
        success, stdout, stderr = FCLIService.run_command(['openssl', 'version'])
        if success:
            success_msg = f"OpenSSL found: {stdout.strip()} ✓"
            logger.info(success_msg)
            return True, success_msg
            
        error_msg = "OpenSSL not found. Please install OpenSSL."
        logger.error(error_msg)
        return False, error_msg