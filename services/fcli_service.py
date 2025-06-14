"""FCLI command execution service"""

import subprocess
import re
from typing import List, Tuple


class FCLIService:
    """Handles FCLI command execution"""
    
    @staticmethod
    def run_command(command: List[str], capture_output: bool = True, timeout: int = 30) -> Tuple[bool, str, str]:
        """Execute a command and return success, stdout, stderr"""
        try:
            result = subprocess.run(
                command,
                capture_output=capture_output,
                text=True,
                timeout=timeout
            )
            return result.returncode == 0, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return False, "", "Command timed out"
        except FileNotFoundError:
            return False, "", f"Command not found: {command[0]}"
        except Exception as e:
            return False, "", str(e)
    
    @staticmethod
    def check_fcli_version() -> Tuple[bool, str]:
        """Check if FCLI 3.5.1+ is installed"""
        success, stdout, stderr = FCLIService.run_command(['fcli', '--version'])
        if not success:
            return False, "FCLI not found. Please install FCLI 3.5.1 or later."
        
        version_match = re.search(r'(\d+\.\d+\.\d+)', stdout)
        if version_match:
            version = version_match.group(1)
            major, minor, patch = map(int, version.split('.'))
            if (major, minor, patch) >= (3, 5, 1):
                return True, f"FCLI {version} found ✓"
            else:
                return False, f"FCLI {version} found, but 3.5.1+ required"
        return False, "Could not determine FCLI version"
    
    @staticmethod
    def check_openssl() -> Tuple[bool, str]:
        """Check if OpenSSL is installed"""
        success, stdout, stderr = FCLIService.run_command(['openssl', 'version'])
        if success:
            return True, f"OpenSSL found: {stdout.strip()} ✓"
        return False, "OpenSSL not found. Please install OpenSSL."