# File Architect Pro

<p align="center">
  <img src="icons/app.ico" alt="File Architect Pro" width="128">
</p>

<p align="center">
  <strong>Professional File Management and Organization Tool</strong>
</p>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#installation">Installation</a> •
  <a href="#usage">Usage</a> •
  <a href="#security">Security</a> •
  <a href="#building">Building</a>
</p>

---

## Features

### 📁 File Filtering
- **Extension Filter**: Select specific file types (.txt, .pdf, .jpg, etc.)
- **Text Search**: Memory-efficient content search within files
- **Size Filter**: Filter by size in KB, MB, GB
- **Date Filter**: Filter by creation/modification date
- **Regex Support**: Advanced pattern matching (ReDoS protected)

### ⚡ Action System
- **Sequential Rename**: Automatic file numbering
- **Find & Replace**: Batch rename operations
- **Copy**: Safe copying with conflict management
- **Secure Delete**: NIST 800-88 compliant data destruction
- **Text Merge**: Combine multiple files into one
- **CSV/Excel Report**: File listing and hash reports

### 🎨 Modern Interface
- **Dark/Light Theme**: Automatic system theme adaptation
- **Turkish/English**: Full multilingual support
- **Tree View**: Preview with folder structure preserved
- **Real-time Progress**: Operation status tracking

---

## Installation

### Requirements
- Python 3.10+
- PyQt6

### Quick Start

```bash
# Clone the repository
git clone https://github.com/AlemdarCode/File-Architect-Pro.git
cd File-Architect-Pro

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

---

## Usage

1. **Select Source Folder**: Choose a folder from the left panel or use "Browse"
2. **Add Filters**: Select a filter button and enter values
3. **Add Actions**: Choose an action from the list and configure it
4. **Execute**: Click "Run All Actions" button

---

## Security

This application is developed in compliance with OWASP security standards:

| Security Feature | Description |
|------------------|-------------|
| **ReDoS Protection** | Regex timeout mechanism prevents CPU exhaustion |
| **Path Traversal** | Directory traversal attacks are blocked |
| **TOCTOU Protection** | Race condition vulnerabilities are fixed |
| **SHA-256 Hash** | Secure hash algorithm instead of MD5 |
| **Symlink Control** | Symbolic links are skipped |
| **File Limit** | 100,000 file limit for DoS protection |

---

## Building

### Create Standalone EXE

```batch
# Run the build script
build.bat
```

> ⚠️ MinGW compiler may be required on first build. The script will prompt you.

### Create Installer

1. Download and install [Inno Setup](https://jrsoftware.org/isinfo.php)
2. Open `installer.iss` in Inno Setup
3. Click "Compile" button
4. Output: `installer_output/FileArchitectPro_Setup_v1.0.exe`

---

## License

MIT License - Copyright © 2025 Ahmet Alemdar

See [LICENSE](LICENSE) for details.

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## Author

**Ahmet Alemdar**
- GitHub: [@AlemdarCode](https://github.com/AlemdarCode)
