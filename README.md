# 🚀 RYAN - Bulk Tools Engine

> A modern desktop application for bulk file processing — archiving, unarchiving, document conversion, and PDF merging — all in one sleek dark-themed interface.

![Python](https://img.shields.io/badge/Python-3.8%2B-00d18f?style=flat-square&logo=python&logoColor=white)
![PySide6](https://img.shields.io/badge/PySide6-Qt-green)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📖 Table of Contents

- [About the Project](#about-the-project)
- [✨ Features](#features)
- [🖥️ Screenshots](#screenshots)
- [🚀 Getting Started](#getting-started)
- [📦 Building the Executable](#building-the-executable)
- [🧰 Tools Included](#tools-included)
- [🛠️ Technologies](#technologies)
- [📄 License](#license)

---

## 📌 About the Project

**RYAN - Bulk Tools Engine** is a desktop application built with **PySide6 (Qt)** that consolidates everyday file operations into a single, powerful, and user-friendly tool. Whether you need to compress hundreds of folders, extract archives, convert documents, or merge PDFs, RYAN handles it all in bulk with a modern, gradient-themed dark interface.

The application is designed for **zero-dependency, offline-friendly environments** (like corporate/security-compliant setups) and can be packaged as a standalone executable for both **Windows** and **Linux**.

---

## ✨ Features

- 🎨 **Modern Dark UI** — Clean gradient theme with a responsive tabbed layout.
- 📦 **Bulk Archiver** — Archive multiple folders into ZIP or TAR.GZ, either one-per-folder or all-in-one.
- 📂 **Unarchiver** — Bulk extract `.zip` and `.tar.gz` archives with custom output directories.
- 📄 **Docs to PDF** — Document conversion workspace with security-compliance guidance.
- 📑 **PDF Merger** — Combine multiple PDF files into a single document in seconds.

---

## 🖥️ Screenshots

> _(Add screenshots of the application here — e.g., a screenshot of the Home tab and each tool tab.)_

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.8 or higher**
- **pip** (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ryan-bulk-tools.git
   cd ryan-bulk-tools
   ```

2. **Install dependencies**
   ```bash
   pip install PySide6 pypdf
   ```

3. **Run the application**
   ```bash
   python ryan_dashboard.py
   ```

---

## 📦 Building the Executable

The project includes **PyInstaller** spec files to build standalone executables for different platforms.

### For Windows
```bash
pyinstaller RyanBulkTools.spec
```

### Alternative Windows build
```bash
pyinstaller ryan_dashboard.spec
```

### For Linux
```bash
pyinstaller linuxbulk.spec
```

The resulting executables will be placed in the `dist/` directory.

---

## 🧰 Tools Included

| Tool | Description | Formats |
|------|-------------|---------|
| **Bulk Archiver** | Compress selected folders into archives | ZIP, TAR.GZ |
| **Unarchiver** | Extract archives in bulk | ZIP, TAR.GZ |
| **Docs to PDF** | Document conversion workspace | DOCX, DOC, ODT |
| **PDF Merger** | Merge multiple PDFs into one | PDF |

---

## 🛠️ Technologies

- **Python** — Core language
- **PySide6 / Qt** — GUI framework
- **pypdf** — PDF reading & writing
- **shutil / tarfile** — Archive handling
- **PyInstaller** — Executable packaging

---

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## 🙌 Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request to improve the project.

---

## 📬 Contact

**Project:** RYAN - Bulk Tools Engine
**Author:** Ryan

---

> ⚡ **RYAN — One tool, every bulk file operation.**
