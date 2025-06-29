"""FCLI command execution service with comprehensive logging and hidden windows"""

import subprocess
import re
import platform
from typing import List, Tuple
from utils.logger import setup_logger, log_command_execution

# Set up logging
logger = setup_logger(__name__)


class FCLIService:
    """Handles FCLI command execution with logging and hidden windows"""
    
    @staticmethod
    def get_subprocess_kwargs() -> dict:
        """Get platform-specific subprocess kwargs to hide windows"""
        kwargs = {}
        
        if platform.system() == "Windows":
            # Method 1: Use CREATE_NO_WINDOW flag (Windows 10+, Python 3.7+)
            kwargs['creationflags'] = subprocess.CREATE_NO_WINDOW
            
            # Method 2: Alternative approach using startupinfo (for older systems)
            # startupinfo = subprocess.STARTUPINFO()
            # startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            # startupinfo.wShowWindow = subprocess.SW_HIDE
            # kwargs['startupinfo'] = startupinfo
        
        return kwargs
    
    @staticmethod
    def run_command(command: List[str], capture_output: bool = True, timeout: int = 30) -> Tuple[bool, str, str]:
        """Execute a command and return success, stdout, stderr with hidden windows"""
        logger.debug(f"Preparing to execute command: {' '.join(command)}")
        
        try:
            # Get platform-specific kwargs to hide windows
            subprocess_kwargs = FCLIService.get_subprocess_kwargs()
            
            result = subprocess.run(
                command,
                capture_output=capture_output,
                text=True,
                timeout=timeout,
                **subprocess_kwargs  # Apply platform-specific window hiding
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
    def run_command_with_input(command: List[str], input_data: str = None, timeout: int = 30) -> Tuple[bool, str, str]:
        """Execute a command with stdin input and return success, stdout, stderr"""
        logger.debug(f"Preparing to execute command with input: {' '.join(command)}")
        
        try:
            # Get platform-specific kwargs to hide windows
            subprocess_kwargs = FCLIService.get_subprocess_kwargs()
            
            result = subprocess.run(
                command,
                input=input_data,
                capture_output=True,
                text=True,
                timeout=timeout,
                **subprocess_kwargs  # Apply platform-specific window hiding
            )
            
            success = result.returncode == 0
            stdout = result.stdout
            stderr = result.stderr
            
            # Log command execution details (without exposing sensitive input)
            log_command_execution(logger, command, success, stdout, stderr, has_input=True)
            
            return success, stdout, stderr
            
        except subprocess.TimeoutExpired:
            logger.error(f"Command with input timed out after {timeout} seconds: {' '.join(command)}")
            return False, "", "Command timed out"
        except FileNotFoundError:
            logger.error(f"Command not found: {command[0]}")
            return False, "", f"Command not found: {command[0]}"
        except Exception as e:
            logger.error(f"Unexpected error executing command with input: {str(e)}", exc_info=True)
            return False, "", str(e)
    
    @staticmethod
    def check_fcli_version() -> Tuple[bool, str]:
        """Check if FCLI 3.5.1+ is installed and added to PATH"""
        logger.info("Checking FCLI version")
        
        success, stdout, stderr = FCLIService.run_command(['fcli', '--version'])
        if not success:
            error_msg = "FCLI not found. Please install FCLI 3.5.1 or later and add to PATH variable."
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
            
        error_msg = "OpenSSL not found. Please install OpenSSL and add to PATH variable."
        logger.error(error_msg)
        return False, error_msg
    
    @staticmethod
    def generate_rsa_keys(private_key_path: str, public_key_path: str) -> Tuple[bool, str]:
        """Generate RSA 4096-bit key pair using OpenSSL"""
        logger.info(f"Generating RSA key pair: {private_key_path}, {public_key_path}")
        
        # Generate private key
        success, stdout, stderr = FCLIService.run_command([
            'openssl', 'genrsa', '-out', private_key_path, '4096'
        ])
        
        if not success:
            error_msg = f"Failed to generate private key: {stderr}"
            logger.error(error_msg)
            return False, error_msg
        
        # Extract public key
        success, stdout, stderr = FCLIService.run_command([
            'openssl', 'rsa', '-in', private_key_path, '-pubout', '-out', public_key_path
        ])
        
        if not success:
            error_msg = f"Failed to extract public key: {stderr}"
            logger.error(error_msg)
            return False, error_msg
        
        success_msg = "RSA key pair generated successfully ✓"
        logger.info(success_msg)
        return True, success_msg