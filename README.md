# SAST Aviator Desktop Application

A cross-platform desktop application that simplifies SAST Aviator setup and audit workflows with an intuitive GUI interface.

## Overview

This application transforms complex command-line SAST operations into an intuitive desktop experience. Built with Flet Python, it provides a complete workflow for setting up secure connections, managing applications, and executing security audits between Fortify SSC and SAST Aviator services.

## Features

- **Guided Setup**: Replace 9+ command-line steps with simple UI workflows
- **Secure Key Management**: Generate RSA 4096-bit keys and manage tokens securely
- **Application Mapping**: Visual mapping between SSC and Aviator applications
- **Real-time Auditing**: Live progress tracking and detailed results
- **Cross-Platform**: Native desktop experience on Windows, macOS, and Linux

## Prerequisites

| Component | Version | Purpose |
|-----------|---------|---------|
| **Python** | 3.8+ | Application runtime |
| **FCLI** | 3.5.1+ | Fortify Command Line Interface |
| **OpenSSL** | Latest | Cryptographic operations |

## Installation

### Option 1: Pre-built Executable (Recommended)

1. Download the latest release
2. Extract to your preferred directory
3. Run the executable:
   - **Windows**: `SAST_Aviator.exe`
   - **macOS**: `SAST_Aviator.app`
   - **Linux**: `./SAST_Aviator`

### Option 2: From Source

```bash
git clone <repository-url>
cd SAST-Aviator-App
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

## Quick Start

### Setup (5 minutes)

1. Launch the application → "Setup & Configuration" tab
2. **Check Prerequisites**: Verify FCLI and OpenSSL installation
3. **Generate Keys**: Create RSA 4096 key pair
4. **Configure Server**: Enter Aviator server URL and tenant
5. **Generate Token**: Create authentication token

### First Audit (3 minutes)

1. Switch to "Audit Operations" tab
2. **Connect to SSC**: Enter SSC URL and credentials
3. **Connect to Aviator**: Verify token file path
4. **Map Applications**: Link SSC apps to Aviator apps
5. **Run Audit**: Select mapping and execute audit

## Configuration

The application stores settings in `config.ini`:

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

[app_mappings]
WebApp:v1.0 = AVIATOR_APP_NAME
```

## Building from Source

```bash
python build_app.py
```

This creates a standalone executable in the `dist/` directory.

## Troubleshooting

### Common Issues

- **"FCLI not found"**: Install FCLI 3.5.1+ and add to PATH
- **"OpenSSL not found"**: Install OpenSSL for your platform
- **Application won't start**: Check Python version (3.8+) and dependencies
- **Audit fails**: Verify SSC/Aviator sessions are active

### Debug Mode

Check logs in `logs/sast_aviator_YYYYMMDD.log` for detailed error information.

## Contributing

This is an open source project created by **Santhosh Kumar** to improve Application Security workflows. Contributions welcome!

### Areas for Contribution
- Bug fixes and error handling
- New features and UI enhancements
- Documentation improvements
- Testing and validation tools
- Security enhancements

## License

Open source contribution to Application Security solutions. Free to use for personal and commercial purposes. Ensure compliance with your organization's security policies when handling authentication tokens and keys.

---

**Created by [Santhosh Kumar](mailto:santgutz2000@live.com) • Built with Flet Python**