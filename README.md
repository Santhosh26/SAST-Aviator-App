# SAST Aviator Desktop Application

A cross-platform desktop application using Flet Python to simplify the SAST Aviator setup and audit workflow.

## Prerequisites

1. **Python 3.8+** installed
2. **FCLI 3.5.1+** installed and available in PATH
3. **OpenSSL** installed and available in PATH

## Installation

1. Clone or download the project files to your local machine

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

From the project root directory, run:

```bash
python main.py
```

## Features

### Setup & Configuration Tab
- **Step 1**: Prerequisites Check - Verify FCLI and OpenSSL installation
- **Step 2**: Key Generation - Generate RSA 4096-bit key pairs
- **Step 3**: Server Configuration - Configure Aviator server settings
- **Step 4**: Token Generation - Generate authentication tokens

### Audit Operations Tab
- **Step 5**: SSC Session - Login to SSC server
- **Step 6**: Aviator Session - Login to Aviator using token
- **Step 7-8**: Application Management - List and map applications
- **Step 9**: Audit Execution - Run audits on mapped applications

## Configuration

The application stores its configuration in `config.ini` which is automatically created on first run. This includes:
- Server URLs and tenant information
- File paths for keys and tokens
- SSC connection details
- Application mappings

## Key Improvements in This Version

1. **Fixed Scrolling**: Each tab now has proper scrollable content with:
   - `scroll=ft.ScrollMode.AUTO` on tab content columns
   - Proper height constraints on tables
   - Expanded containers for better layout management

2. **Modular Architecture**: The application is now organized into:
   - **config/**: Configuration management
   - **services/**: Business logic separated from UI
   - **ui/**: UI components for each tab
   - **utils/**: Shared utilities and constants

3. **Better Error Handling**: 
   - Input validation with visual feedback
   - Proper error messages for missing commands
   - Status messages displayed within each section

4. **Code Organization Benefits**:
   - Easier to maintain and test
   - Clear separation of concerns
   - Reusable components and services
   - Better scalability for future features

## Troubleshooting

1. **"FCLI not found" error**: Ensure FCLI is installed and added to your system PATH
2. **"OpenSSL not found" error**: Install OpenSSL and ensure it's in your PATH
3. **Scrolling issues**: Try resizing the window or restarting the application
4. **Key generation fails**: Ensure you have write permissions in the specified directory

## Development

To add new features or modify the application:

1. UI changes: Modify files in the `ui/` directory
2. New services: Add to the `services/` directory
3. Configuration: Update `config_manager.py`
4. Constants: Add to `utils/constants.py`

## License

This application is part of the OpenText Fortify suite.