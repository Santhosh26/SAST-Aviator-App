SAST Aviator Desktop Application - Project Instructions
Project Overview
Develop a cross-platform desktop application using Flet Python to simplify the SAST Aviator setup and audit workflow. The app will replace complex command-line operations with an intuitive GUI following OpenText design standards.
Design Requirements
Color Scheme (OpenText Brand Colors)

Primary Colors:

Electric Blue: RGB(26, 106, 255) / HEX #1a6aff
Cobalt Blue: RGB(0, 0, 139) / HEX #00008b


Secondary Colors:

Black: RGB(0, 0, 0) / HEX #000000
White: RGB(255, 255, 255) / HEX #ffffff
Yellow: RGB(225, 188, 54) / HEX #e1bc36



Typography

Primary Font: Inter
Fallback Font: Arial
Use consistent font sizes and weights for hierarchy

UI/UX Guidelines

Clean, modern interface with proper spacing
Use Electric Blue for primary buttons and headers
Use Cobalt Blue for secondary elements and accents
Implement proper error handling with clear user feedback
Show loading states for long-running operations
Responsive design that works across different screen sizes

Application Architecture
Technology Stack

Framework: Flet Python
Target Platforms: Windows, macOS, Linux
Configuration Storage: config.ini file
Dependencies: FCLI 3.5.1+, OpenSSL

Application Structure
sast_aviator_app/
├── main.py                    # Application entry point
├── config/                    # Configuration management
│   ├── __init__.py
│   ├── config_manager.py      # Config operations
├── ui/                        # User interface
│   ├── __init__.py
│   ├── setup_tab.py          # Setup & Configuration tab
│   ├── audit_tab.py          # Audit Operations tab
├── services/                  # Business logic
│   ├── __init__.py
│   ├── fcli_service.py       # FCLI command execution
│   ├── aviator_service.py    # Aviator operations
│   ├── ssc_service.py        # SSC operations
├── utils/                     # Utilities
│   ├── __init__.py
│   ├── constants.py          # Colors and defaults
│   ├── validators.py         # Input validation
│   ├── helpers.py            # Helper functions
├── requirements.txt          # Dependencies
├── README.md                 # Documentation
└── setup_project.py          # Setup helper script

Core Functionality
Tab 1: Setup and Configuration
Handles initial setup steps (Steps 1-4):

Prerequisites Check

Verify FCLI version 3.5.1+ installation
Verify OpenSSL installation
Show installation guides if missing


Key Generation (Step 2)

Generate RSA 4096-bit private/public key pair
Commands to execute:
bashopenssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:4096 -out private_key.pem
openssl rsa -in private_key.pem -pubout -out public_key.pem

Display public key for sharing with PM
Save private key securely


Server Configuration (Step 3)

Input fields for:

Server URL (default: https://ams.aviator.fortify.com)
Tenant (default: demo_presales)
Private key file path


Execute: fcli aviator admin-config create --url [URL] --tenant [TENANT] --private-key [KEY_FILE]


Token Generation (Step 4)

Input fields for:

Email address
Token name
Token file save location


Execute: fcli aviator token create --email [EMAIL] --name [TOKEN_NAME] --save-token [FILE]
Parse and display token details



Tab 2: Audit Operations
Handles operational steps (Steps 5-9):

SSC Session (Step 5)

Input fields for:

SSC URL
Username
Password (masked input)


Execute: fcli ssc session login --url [URL] -u [USER] -p [PASS]


Aviator Session (Step 6)

Use saved token file
Execute: fcli aviator session login --url [URL] --token [TOKEN_FILE]


Application Management (Steps 7-8)

Create Aviator App (Optional):

Input field for app name
Execute: fcli aviator app create "[APP_NAME]"


List Applications:

Fetch SSC apps: fcli ssc appversion ls --output json
Fetch Aviator apps: fcli aviator app list --output json
Display in organized tables


App Mapping Interface:

Dropdown/selection for SSC app:version combinations
Dropdown/selection for Aviator app names
Save mappings for reuse
Allow multiple SSC apps to map to same Aviator app




Audit Execution (Step 9)

Select SSC app:version from mapped pairs
Select corresponding Aviator app
Execute: fcli aviator ssc audit --av "[SSC_APP]:[VERSION]" --app "[AVIATOR_APP]"
Display audit progress and results



Configuration Management
config.ini Structure
ini[server]
url = https://ams.aviator.fortify.com
tenant = demo_presales
private_key_path = ./private_key.pem

[tokens]
current_token_file = ./token_meapresales.json
token_email = user@example.com

[ssc]
url = http://10.0.1.203:8080/ssc
username = admin
last_session = 2025-06-03T17:57:28Z

[app_mappings]
# Format: ssc_app:version = aviator_app
ZeroWebApp:test = AVIATOR_APP_NAME
Error Handling & Validation
Input Validation

Validate URLs (proper format, reachability)
Validate email addresses
Validate file paths and permissions
Check FCLI command availability

Error Scenarios

Missing dependencies (FCLI, OpenSSL)
Network connectivity issues
Authentication failures
Invalid credentials
File permission errors
Command execution failures

User Feedback

Progress indicators for long operations
Clear error messages with suggested solutions
Success confirmations with next steps
Tooltips and help text for complex fields

Security Considerations
Key Management

Store private keys securely
Never log or display private keys
Implement secure token storage
Clear sensitive data from memory

Credential Handling

Mask password inputs
Encrypt stored credentials
Implement session timeouts
Secure token file handling

Development Guidelines
Code Organization

Use modular design with clear separation of concerns
Implement proper logging for debugging
Use type hints and docstrings
Follow PEP 8 style guidelines

Testing Strategy

Unit tests for core functions
Integration tests for FCLI interactions
UI tests for critical workflows
Cross-platform compatibility testing

User Experience

Intuitive navigation between tabs
Clear visual feedback for all actions
Consistent button placement and sizing
Keyboard shortcuts for common actions
Auto-save functionality for forms

Flet-Specific Implementation Notes
UI Components

Use ft.Tabs for main navigation
Implement ft.TextField with proper validation
Use ft.ElevatedButton with OpenText colors
Implement ft.DataTable for app listings
Use ft.ProgressBar for long operations

State Management

Implement proper state management between tabs
Use ft.Page.update() for UI refreshes
Handle async operations properly
Implement proper cleanup on app close

Platform Considerations

Handle different OS path separators
Account for different command execution methods
Test file operations across platforms
Handle different default installation paths

This application should significantly improve the user experience for SAST Aviator setup and operation, making it accessible to users who may not be comfortable with command-line interfaces while maintaining all the functionality of the original workflow.