# SAST Aviator Desktop Application

<div align="center">

![SAST Aviator](https://img.shields.io/badge/SAST-Aviator-1a6aff?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8+-3776ab?style=for-the-badge&logo=python)
![Flet](https://img.shields.io/badge/Flet-Cross--Platform-00d4aa?style=for-the-badge)
![OpenText](https://img.shields.io/badge/OpenText-Fortify-e1bc36?style=for-the-badge)

**A cross-platform desktop application that simplifies SAST Aviator setup and audit workflows with an intuitive GUI interface.**

*An open source contribution to Application Security solutions by [Santhosh Kumar](mailto:santgutz2000@live.com)*

[Features](#features) • [Installation](#installation) • [Usage](#usage) • [Build](#building-from-source) • [Troubleshooting](#troubleshooting)

</div>

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Detailed Usage Guide](#detailed-usage-guide)
- [Configuration](#configuration)
- [Building from Source](#building-from-source)
- [Troubleshooting](#troubleshooting)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

## Overview

The SAST Aviator Desktop Application transforms complex command-line SAST (Static Application Security Testing) operations into an intuitive, user-friendly desktop experience. Built with Flet Python, this cross-platform application provides a complete workflow for setting up secure connections, managing applications, and executing security audits between Fortify SSC (Software Security Center) and SAST Aviator services.

### Project Background

This open source project was created by **Santhosh Kumar** to address a critical gap in Application Security tooling - making enterprise-grade security tools accessible to security professionals regardless of their command-line expertise. 


### Why This Application?

- **Simplifies Complex Workflows**: Replaces 9+ command-line steps with guided UI workflows
- **Enhanced Security**: Secure key generation, token management, and encrypted credential storage
- **Real-time Monitoring**: Live progress tracking and detailed audit result visualization
- **Advanced Management**: Multi-select operations, search functionality, and bulk application mapping
- **Cross-Platform**: Native desktop experience on Windows, macOS, and Linux
- **Comprehensive Logging**: Detailed operation tracking and debugging capabilities
- **Community-Driven**: Open source contribution to benefit the entire Application Security community

## Features

### Setup & Configuration (Steps 1-4)
- **Prerequisites Validation**: Automatic checking of FCLI 3.5.1+ and OpenSSL installations
- **Cryptographic Key Management**: 
  - Generate RSA 4096-bit key pairs with OpenSSL
  - Import existing private/public key files
  - Secure key storage and public key sharing
- **Server Configuration**: Aviator server connection setup with validation
- **Token Management**: 
  - Generate new authentication tokens
  - Import existing token files
  - Secure token file handling

### 🔍 Audit Operations (Steps 5-9)
- **Multi-Platform Authentication**: 
  - SSC session management with credential validation
  - Aviator session establishment using tokens
- **Application Management**:
  - Real-time application listing from both SSC and Aviator
  - Advanced search and filtering capabilities
  - Create new Aviator applications on-demand
- **Intelligent Mapping System**:
  - Single application mapping (1:1)
  - Multi-select bulk mapping operations
  - Visual mapping management with add/remove functionality
- **Advanced Audit Execution**:
  - Real-time progress tracking with percentage indicators
  - Scrollable, formatted audit results
  - Output filtering and cleaning for readability
  - Comprehensive audit logging with timestamps

### User Experience
- **Modern UI Design**: Material Design 3 with OpenText brand colors
- **Responsive Layout**: Adaptive interface with proper scrolling containers
- **Intelligent Status Management**: Section-specific status indicators with timestamps
- **Error Handling**: Comprehensive validation with clear error messages and suggestions
- **File Management**: Integrated file browsers for keys, tokens, and configuration files

## Prerequisites

### Required Software

| Component | Version | Purpose |
|-----------|---------|---------|
| **Python** | 3.8+ | Application runtime |
| **FCLI** | 3.5.1+ | Fortify Command Line Interface |
| **OpenSSL** | Latest | Cryptographic operations |

### Platform Requirements

- **Windows**: Windows 10/11 (x64)
- **macOS**: macOS 10.14+ (Intel/Apple Silicon)
- **Linux**: Ubuntu 18.04+, CentOS 7+, or equivalent

### Network Requirements

- Internet connectivity for initial setup
- Access to your organization's SSC server
- Access to SAST Aviator service (typically `https://ams.aviator.fortify.com`)

## 🚀 Installation

### Option 1: Download Pre-built Executable (Recommended)

1. **Download the latest release** from the releases page
2. **Extract** the archive to your preferred directory
3. **Run** the executable:
   - **Windows**: Double-click `SAST_Aviator.exe`
   - **macOS**: Double-click `SAST_Aviator.app`
   - **Linux**: Run `./SAST_Aviator` in terminal

### Option 2: Install from Source

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd SAST-Aviator-App
   ```

2. **Create virtual environment** (recommended):
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python main.py
   ```

### Installing Prerequisites

#### FCLI Installation
```bash
# Download from Fortify official repository
# Ensure FCLI is added to your system PATH
fcli --version  # Should show 3.5.1 or higher
```

#### OpenSSL Installation
- **Windows**: Download from [OpenSSL official site](https://slproweb.com/products/Win32OpenSSL.html)
- **macOS**: `brew install openssl`
- **Linux**: `sudo apt-get install openssl` (Ubuntu/Debian) or `sudo yum install openssl` (CentOS/RHEL)

## 🏃‍♂️ Quick Start

### First-Time Setup (5 minutes)

1. **Launch the application** and navigate to the "Setup & Configuration" tab

2. **Check Prerequisites** (Step 1):
   - Click "Check FCLI" and "Check OpenSSL"
   - Ensure both show green checkmarks

3. **Generate Keys** (Step 2):
   - Choose a location for your private key
   - Click "Generate RSA 4096 Key Pair"
   - Copy the displayed public key to share with your PM

4. **Configure Server** (Step 3):
   - Enter your Aviator server URL (usually `https://ams.aviator.fortify.com`)
   - Enter your tenant name
   - Click "Configure Server"

5. **Generate Token** (Step 4):
   - Enter your email address
   - Choose a token name and save location
   - Click "Generate Token"

### Running Your First Audit (3 minutes)

1. **Switch to "Audit Operations" tab**

2. **Connect to SSC** (Step 5):
   - Enter your SSC server URL and credentials
   - Click "Login to SSC"

3. **Connect to Aviator** (Step 6):
   - Verify token file path
   - Click "Login to Aviator"

4. **Map Applications** (Steps 7-8):
   - Click "Refresh SSC Apps" and "Refresh Aviator Apps"
   - Select applications from the dropdowns
   - Click "Add Mapping"

5. **Run Audit** (Step 9):
   - Select a mapping from the dropdown
   - Click "Run Audit"
   - Monitor progress and view results

## Detailed Usage Guide

### Setup & Configuration Tab

#### Step 1: Prerequisites Check
The application automatically validates your environment on startup. You can manually re-check:

- **FCLI Check**: Validates version 3.5.1+ installation and PATH accessibility
- **OpenSSL Check**: Confirms OpenSSL is installed and accessible
- **Status Indicators**: Green checkmarks indicate successful validation

#### Step 2: Key Generation/Import
Choose between generating new keys or importing existing ones:

**Generate New Keys**:
1. Click "Browse" to select save location for private key
2. Click "Generate RSA 4096 Key Pair"
3. Public key appears in the text area below
4. Share the public key with your Project Manager

**Load Existing Keys**:
1. Use "Load Private Key" to import your existing private key
2. Use "Load Public Key" to import your existing public key
3. The application auto-detects matching public keys

#### Step 3: Server Configuration
Configure your connection to the Aviator service:

1. **Server URL**: Your organization's Aviator endpoint
2. **Tenant**: Your organization's tenant identifier
3. **Private Key Path**: Path to your private key (auto-filled if generated in Step 2)

#### Step 4: Token Generation/Import
Generate or import authentication tokens:

**Generate New Token**:
1. Enter your email address (validates format)
2. Specify token name for identification
3. Choose save location for token file
4. Click "Generate Token"

**Load Existing Token**:
- Use "Load Token File" to import previously generated tokens

### Audit Operations Tab

#### Step 5: SSC Session Management
Connect to your Software Security Center:

1. Enter SSC server URL (validates format)
2. Provide username and password
3. Click "Login to SSC"
4. Applications are automatically loaded after successful login

#### Step 6: Aviator Session Management
Establish connection with Aviator service:

1. Verify token file path (or browse for different token)
2. Click "Login to Aviator"
3. Session is established using the authentication token

#### Steps 7-8: Application Management
Manage applications and create mappings:

**List Applications**:
- Click "Refresh SSC Apps" to load from SSC
- Click "Refresh Aviator Apps" to load from Aviator
- Use search boxes to filter large application lists

**Create New Aviator App**:
1. Enter application name
2. Click "Create Aviator App"
3. New app appears in the Aviator applications list

**Application Mapping**:

*Single Mapping Mode*:
1. Select SSC app:version from dropdown
2. Select Aviator app from dropdown
3. Click "Add Mapping"

*Multi-Select Mapping Mode*:
1. Switch to "Multi-Select Mapping" radio button
2. Check boxes next to desired SSC applications
3. Check boxes next to desired Aviator applications
4. Click "Map Selected Apps"

**Mapping Management**:
- View all mappings in the "Current Mappings" table
- Remove mappings using the "Remove" button
- Mappings are automatically saved to configuration

#### Step 9: Audit Execution
Execute security audits on your applications:

1. **Select Mapping**: Choose from dropdown of configured mappings
2. **Run Audit**: Click "Run Audit" to start the process
3. **Monitor Progress**: Watch the progress bar and status updates
4. **View Results**: Review detailed audit output in the scrollable results area

**Audit Features**:
- Real-time progress tracking with percentage indicators
- Comprehensive output logging with timestamps
- Filtered output for improved readability
- Full audit history in application logs

## ⚙️ Configuration

The application stores configuration in `config.ini`:

```ini
[server]
url = https://ams.aviator.fortify.com
tenant = demo_presales
private_key_path = ./private_key.pem

[tokens]
current_token_file = ./token_meapresales.json
token_email = user@example.com

[ssc]
url = http://your-ssc:8080/ssc
username = admin
last_session = 2025-06-27T10:44:30.659165

[app_mappings]
# Format: ssc_app:version = aviator_app
WebApp:v1.0 = AVIATOR_APP_NAME
```

### Configuration Locations

- **Windows**: Same directory as executable
- **macOS**: Same directory as application bundle
- **Linux**: Same directory as executable

### Advanced Configuration

**Logging Configuration**:
- Log files: `logs/sast_aviator_YYYYMMDD.log`
- Rotation: 10MB per file, 5 backup files
- Levels: DEBUG (file), INFO (console)

**Security Settings**:
- Private keys: Stored with restricted file permissions
- Tokens: Encrypted JSON format
- Passwords: Not stored persistently

## 🔨 Building from Source

### Development Setup

1. **Clone repository**:
   ```bash
   git clone <repository-url>
   cd SAST-Aviator-App
   ```

2. **Install development dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run in development mode**:
   ```bash
   python main.py
   ```

### Building Executables

The application provides a comprehensive build script supporting multiple packaging methods:

```bash
python build_app.py
```

**Build Options**:
- **Flet Pack** (Recommended): Native Flet packaging
- **PyInstaller**: Custom spec with optimizations
- **Auto-fallback**: Tries Flet first, falls back to PyInstaller

**Build Output**:
- **Executable**: `dist/SAST_Aviator.exe` (Windows) or equivalent
- **Build Info**: `dist/README.txt` with build details
- **Single File**: Self-contained executable with dependencies

### Custom Build Configuration

Edit `build_app.py` to customize:
- Application name and version
- Icon file location
- Included/excluded dependencies
- Platform-specific options

## 🔧 Troubleshooting

### Common Issues

#### "FCLI not found" Error
**Solution**:
1. Download FCLI 3.5.1+ from Fortify
2. Add FCLI to your system PATH
3. Restart the application
4. Run "Check FCLI" in Step 1

#### "OpenSSL not found" Error
**Solution**:
1. Install OpenSSL for your platform
2. Ensure OpenSSL is in PATH
3. Test with `openssl version` in terminal
4. Restart the application

#### Application Won't Start
**Solutions**:
1. Check Python version (3.8+ required)
2. Verify all dependencies installed
3. Check logs in `logs/` directory
4. Run from command line to see error messages

#### Audit Fails to Execute
**Common Causes**:
1. SSC session expired - re-login in Step 5
2. Aviator session expired - re-login in Step 6
3. Invalid application mapping - verify in Steps 7-8
4. Network connectivity issues

#### Multiple Windows Opening (Packaged App)
**Solution**:
1. Close all instances via Task Manager
2. Run only the executable from `dist/` folder
3. Avoid running multiple build commands simultaneously

### Debug Mode

Enable detailed logging:
1. Check `logs/sast_aviator_YYYYMMDD.log`
2. Look for ERROR and WARNING messages
3. Report issues with relevant log excerpts

### Getting Help

1. **Check logs**: Review application logs for error details
2. **Verify prerequisites**: Ensure FCLI and OpenSSL are properly installed
3. **Test connectivity**: Verify network access to SSC and Aviator services
4. **Configuration review**: Check `config.ini` for correct settings

## Development

### Project Structure

```
SAST-Aviator-App/
├── main.py                    # Application entry point
├── config/
│   └── config_manager.py      # Configuration management
├── services/                  # Business logic
│   ├── fcli_service.py        # Command execution
│   ├── aviator_service.py     # Aviator operations
│   └── ssc_service.py         # SSC integration
├── ui/                        # User interface
│   ├── setup_tab.py           # Setup workflow UI
│   └── audit_tab.py           # Audit workflow UI
└── utils/                     # Utilities
    ├── constants.py           # Application constants
    ├── validators.py          # Input validation
    ├── helpers.py             # UI helpers
    └── logger.py              # Logging system
```

### Development Guidelines

- **Code Style**: Follow PEP 8 standards
- **Type Hints**: Use comprehensive type annotations
- **Documentation**: Include docstrings for all functions
- **Error Handling**: Implement comprehensive exception handling
- **Logging**: Use the centralized logging system for all operations

### Testing

```bash
# Run application in development mode
python main.py

# Test individual components
python -m services.fcli_service
python -m utils.validators
```

## Contributing

This is an **open source project** created by **Santhosh Kumar** to improve Application Security workflows for the community. We welcome contributions from security professionals, developers, and anyone passionate about making application security more accessible!

### 👨‍💻 Project Author
**Santhosh Kumar**  
[santgutz2000@live.com](mailto:santgutz2000@live.com)  
*Passionate about simplifying Application Security workflows*

### How to Contribute

1. Fork the repository
2. Create a feature branch
3. Make your changes with proper documentation
4. Test thoroughly across platforms
5. Submit a pull request

### Contribution Areas

- 🐛 Bug fixes and error handling improvements
- ✨ New features and workflow enhancements
- 📚 Documentation improvements
- 🎨 UI/UX enhancements
- 🔧 Build and packaging improvements
- 🧪 Testing and validation tools
- 🌐 Internationalization and localization
- 🔐 Security enhancements and best practices

### Community Goals

This project aims to:
- **Democratize Application Security**: Make advanced security tools accessible to all skill levels
- **Reduce Learning Curve**: Transform complex CLI operations into intuitive workflows
- **Improve Productivity**: Streamline repetitive security tasks for teams
- **Foster Innovation**: Provide a foundation for further Application Security tool development

## License

This application is an **open source contribution** to Application Security solutions, created by **Santhosh Kumar** ([santgutz2000@live.com](mailto:santgutz2000@live.com)).

While this tool integrates with OpenText Fortify products (FCLI, SSC, SAST Aviator), it is an independent open source project designed to enhance the user experience of Application Security workflows.

### Usage Rights
- Free to use for personal and commercial purposes
- Modify and distribute under open source principles
- Contribute improvements back to the community
- Ensure compliance with your organization's security policies when handling authentication tokens and keys

### Disclaimer
This is a community-contributed tool and is not officially endorsed or supported by OpenText. Users are responsible for ensuring compliance with their organization's security policies and Fortify licensing agreements.

---

<div align="center">

**Open Source Contribution to Application Security Solutions**  
**Created by [Santhosh Kumar](mailto:santgutz2000@live.com) • Built with ❤️ using Flet Python**

*Enhancing Application Security workflows for the community*

[Report Issues](./issues) • [Request Features](./issues) • [Contact Author](mailto:santgutz2000@live.com)

</div>