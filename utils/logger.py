"""Logging configuration for SAST Aviator application"""

import logging
import logging.handlers
from pathlib import Path
from datetime import datetime
import sys


def setup_logger(name: str = None) -> logging.Logger:
    """
    Set up comprehensive logging for the application
    
    Args:
        name: Logger name (module name)
    
    Returns:
        Configured logger instance
    """
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Generate log filename with timestamp
    log_filename = log_dir / f"sast_aviator_{datetime.now().strftime('%Y%m%d')}.log"
    
    # Get logger
    logger = logging.getLogger(name or "SASTAviator")
    
    # Only configure if not already configured
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        
        # Create formatters
        detailed_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        simple_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        )
        
        # File handler with rotation
        file_handler = logging.handlers.RotatingFileHandler(
            log_filename,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(detailed_formatter)
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(simple_formatter)
        
        # Add handlers to logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        # Log startup message
        if name is None or name == "__main__":
            logger.info("="*60)
            logger.info("SAST Aviator Application Starting")
            logger.info(f"Log file: {log_filename}")
            logger.info(f"Python version: {sys.version}")
            logger.info("="*60)
    
    return logger


def log_exception(logger: logging.Logger, exc: Exception, context: str = ""):
    """
    Log an exception with full traceback
    
    Args:
        logger: Logger instance
        exc: Exception to log
        context: Additional context about where the exception occurred
    """
    logger.error(f"Exception in {context}: {type(exc).__name__}: {str(exc)}", exc_info=True)


def log_command_execution(logger: logging.Logger, command: list, success: bool, 
                         stdout: str = "", stderr: str = ""):
    """
    Log command execution details
    
    Args:
        logger: Logger instance
        command: Command that was executed
        success: Whether command succeeded
        stdout: Standard output
        stderr: Standard error
    """
    command_str = ' '.join(command)
    logger.debug(f"Executing command: {command_str}")
    
    if success:
        logger.debug(f"Command succeeded: {command_str}")
        if stdout:
            logger.debug(f"STDOUT: {stdout[:500]}...")  # Limit output length
    else:
        logger.error(f"Command failed: {command_str}")
        if stderr:
            logger.error(f"STDERR: {stderr}")
        if stdout:
            logger.debug(f"STDOUT: {stdout[:500]}...")


def log_api_call(logger: logging.Logger, method: str, endpoint: str, 
                 status_code: int = None, response_time: float = None):
    """
    Log API call details
    
    Args:
        logger: Logger instance
        method: HTTP method
        endpoint: API endpoint
        status_code: Response status code
        response_time: Response time in seconds
    """
    if status_code and response_time:
        logger.info(f"API Call: {method} {endpoint} - Status: {status_code} - Time: {response_time:.2f}s")
    else:
        logger.debug(f"API Call: {method} {endpoint}")


def log_user_action(logger: logging.Logger, action: str, details: dict = None):
    """
    Log user actions for audit trail
    
    Args:
        logger: Logger instance
        action: Description of user action
        details: Additional details about the action
    """
    if details:
        logger.info(f"User Action: {action} - Details: {details}")
    else:
        logger.info(f"User Action: {action}")