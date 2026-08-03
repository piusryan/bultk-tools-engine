import sys
import os
import shutil
import tarfile
from pathlib import Path
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, 
    QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, 
    QListWidget, QListWidgetItem, QRadioButton, QButtonGroup, 
    QTextEdit, QMessageBox, QFrame
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QIcon, QPalette, QColor

try:
    from pypdf import PdfReader, PdfWriter
except ImportError:
    PdfReader = None
    PdfWriter = None

class RyanDashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RYAN - Bulk Tools Engine")
        self.setMinimumSize(900, 700)
        self.init_ui()
        self.apply_theme()

    def init_ui(self):
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.home_tab = QWidget()
        self.archiver_tab = QWidget()
        self.unarchiver_tab = QWidget()
        self.docs_tab = QWidget()
        self.merger_tab = QWidget()
        
        self.tabs.addTab(self.home_tab, "Home")
        self.tabs.addTab(self.archiver_tab, "Bulk Archiver")
        self.tabs.addTab(self.unarchiver_tab, "Unarchiver")
        self.tabs.addTab(self.docs_tab, "Docs to PDF")
        self.tabs.addTab(self.merger_tab, "PDF Merger")

        self.setup_home_tab()
        self.setup_archiver_tab()
        self.setup_unarchiver_tab()
        self.setup_docs_tab()
        self.setup_merger_tab()

    def apply_theme(self):
        # Modern Dark Theme
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(12, 18, 32))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(2, 4, 10))
        palette.setColor(QPalette.AlternateBase, QColor(18, 26, 44))
        palette.setColor(QPalette.ToolTipBase, Qt.white)
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(0, 209, 143))
        palette.setColor(QPalette.ButtonText, QColor(2, 4, 10))
        palette.setColor(QPalette.Link, QColor(0, 209, 143))
        palette.setColor(QPalette.Highlight, QColor(0, 209, 143))
        palette.setColor(QPalette.HighlightedText, QColor(2, 4, 10))
        self.setPalette(palette)
        
        self.setStyleSheet("""
            QTabWidget::pane { border: 1px solid #1e2638; top: -1px; background: #0c1220; }
            QTabBar::tab { background: #0c1220; border: 1px solid #1e2638; padding: 10px 20px; color: #8a92a7; border-top-left-radius: 4px; border-top-right-radius: 4px; }
            QTabBar::tab:selected { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #00d18f, stop:1 #00f0a6); color: #02040a; font-weight: bold; }
            QPushButton { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #00d18f, stop:1 #00f0a6); border-radius: 15px; padding: 8px 16px; color: #02040a; font-weight: bold; border: none; }
            QPushButton:hover { background: #00f0a6; }
            QLineEdit { background: #060a16; border: 1px solid #1e2638; border-radius: 5px; padding: 8px; color: white; }
            QListWidget { background: #060a16; border: 1px solid #1e2638; border-radius: 5px; color: white; }
            QTextEdit { background: #050815; border: 1px solid #1e2638; border-radius: 5px; color: #00f0a6; font-family: 'Consolas', 'Courier New'; }
            QLabel { color: #f5f7ff; }
        """)

    def setup_home_tab(self):
        layout = QVBoxLayout()
        layout.addStretch()
        
        label = QLabel("RYAN")
        label.setAlignment(Qt.AlignCenter)
        font = QFont("Segoe UI", 120, QFont.Bold)
        label.setFont(font)
        label.setStyleSheet("color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #00d18f, stop:1 #00f0a6); letter-spacing: 15px;")
        layout.addWidget(label)
        
        layout.addStretch()
        self.home_tab.setLayout(layout)

    def setup_archiver_tab(self):
        layout = QVBoxLayout()
        
        # Path selection
        path_layout = QHBoxLayout()
        self.arch_path_edit = QLineEdit()
        self.arch_path_edit.setPlaceholderText("Select parent directory...")
        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self.browse_arch_dir)
        path_layout.addWidget(self.arch_path_edit)
        path_layout.addWidget(browse_btn)
        layout.addLayout(path_layout)
        
        # List and Scan
        scan_btn = QPushButton("Scan Folders")
        scan_btn.clicked.connect(self.scan_arch_folders)
        layout.addWidget(scan_btn)
        
        self.arch_list = QListWidget()
        layout.addWidget(self.arch_list)
        
        # Options
        self.arch_mode_group = QButtonGroup(self)
        self.one_per_folder = QRadioButton("One archive per folder")
        self.one_per_folder.setChecked(True)
        self.all_in_one = QRadioButton("All folders into one archive")
        self.arch_mode_group.addButton(self.one_per_folder)
        self.arch_mode_group.addButton(self.all_in_one)
        
        options_layout = QHBoxLayout()
        options_layout.addWidget(self.one_per_folder)
        options_layout.addWidget(self.all_in_one)
        layout.addLayout(options_layout)
        
        self.arch_name_edit = QLineEdit()
        self.arch_name_edit.setPlaceholderText("Archive name (for All-in-One)...")
        layout.addWidget(self.arch_name_edit)
        
        # Format
        format_layout = QHBoxLayout()
        format_layout.addWidget(QLabel("Format:"))
        self.format_combo = QRadioButton("ZIP")
        self.format_combo.setChecked(True)
        self.format_tar = QRadioButton("TAR.GZ")
        format_layout.addWidget(self.format_combo)
        format_layout.addWidget(self.format_tar)
        layout.addLayout(format_layout)
        
        # Action
        start_btn = QPushButton("Start Archiving")
        start_btn.clicked.connect(self.start_archiving)
        layout.addWidget(start_btn)
        
        self.arch_status = QTextEdit()
        self.arch_status.setReadOnly(True)
        layout.addWidget(self.arch_status)
        
        self.archiver_tab.setLayout(layout)

    def setup_unarchiver_tab(self):
        layout = QVBoxLayout()
        
        # Select Files
        scan_btn = QPushButton("Select Archives (.zip, .tar.gz)...")
        scan_btn.clicked.connect(self.select_unarch_files)
        layout.addWidget(scan_btn)
        
        self.unarch_list = QListWidget()
        layout.addWidget(self.unarch_list)
        
        # Output Path
        path_layout = QHBoxLayout()
        self.unarch_out_edit = QLineEdit()
        self.unarch_out_edit.setPlaceholderText("Extraction directory (optional)...")
        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self.browse_unarch_out)
        path_layout.addWidget(self.unarch_out_edit)
        path_layout.addWidget(browse_btn)
        layout.addLayout(path_layout)
        
        # Action
        start_btn = QPushButton("Start Unarchiving")
        start_btn.clicked.connect(self.start_unarchiving)
        layout.addWidget(start_btn)
        
        self.unarch_status = QTextEdit()
        self.unarch_status.setReadOnly(True)
        layout.addWidget(self.unarch_status)
        
        self.unarchiver_tab.setLayout(layout)

    def setup_docs_tab(self):
        layout = QVBoxLayout()
        
        # Select Files
        scan_btn = QPushButton("Select Document Files (.docx, .doc, .odt)...")
        scan_btn.clicked.connect(self.select_doc_files)
        layout.addWidget(scan_btn)
        
        self.docs_list = QListWidget()
        layout.addWidget(self.docs_list)
        
        # Action
        start_btn = QPushButton("Convert to PDF")
        start_btn.clicked.connect(self.start_doc_conversion)
        layout.addWidget(start_btn)
        
        self.docs_status = QTextEdit()
        self.docs_status.setReadOnly(True)
        layout.addWidget(self.docs_status)
        
        self.docs_tab.setLayout(layout)

    def setup_merger_tab(self):
        layout = QVBoxLayout()
        
        # Scan Files
        scan_btn = QPushButton("Select PDF Files...")
        scan_btn.clicked.connect(self.select_pdf_files)
        layout.addWidget(scan_btn)
        
        self.merge_list = QListWidget()
        layout.addWidget(self.merge_list)
        
        # Output Name
        self.merge_name_edit = QLineEdit()
        self.merge_name_edit.setPlaceholderText("Merged file name (default: merged.pdf)...")
        layout.addWidget(self.merge_name_edit)
        
        # Action
        start_btn = QPushButton("Merge PDFs")
        start_btn.clicked.connect(self.start_merging)
        layout.addWidget(start_btn)
        
        self.merge_status = QTextEdit()
        self.merge_status.setReadOnly(True)
        layout.addWidget(self.merge_status)
        
        self.merger_tab.setLayout(layout)

    # --- Archiver Logic ---
    def browse_arch_dir(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Directory")
        if dir_path:
            self.arch_path_edit.setText(dir_path)

    def scan_arch_folders(self):
        path = self.arch_path_edit.text()
        if not path or not os.path.isdir(path):
            QMessageBox.warning(self, "Error", "Please select a valid directory.")
            return
        
        self.arch_list.clear()
        for item in os.listdir(path):
            full_path = os.path.join(path, item)
            if os.path.isdir(full_path):
                list_item = QListWidgetItem(item)
                list_item.setFlags(list_item.flags() | Qt.ItemIsUserCheckable)
                list_item.setCheckState(Qt.Checked)
                self.arch_list.addItem(list_item)

    def start_archiving(self):
        path = self.arch_path_edit.text()
        selected_folders = []
        for i in range(self.arch_list.count()):
            item = self.arch_list.item(i)
            if item.checkState() == Qt.Checked:
                selected_folders.append(os.path.join(path, item.text()))
        
        if not selected_folders:
            QMessageBox.warning(self, "Error", "No folders selected.")
            return

        fmt = "zip" if self.format_combo.isChecked() else "gztar"
        ext = ".zip" if fmt == "zip" else ".tar.gz"
        
        self.arch_status.clear()
        try:
            if self.one_per_folder.isChecked():
                for folder in selected_folders:
                    base_name = folder
                    shutil.make_archive(base_name, fmt, folder)
                    self.arch_status.append(f"Created: {base_name}{ext}")
            else:
                name = self.arch_name_edit.text() or "combined_archive"
                out_path = os.path.join(path, name)
                # For all-in-one, we create a temporary dir, copy stuff, archive it
                temp_dir = os.path.join(path, "_temp_ryan_archiver")
                os.makedirs(temp_dir, exist_ok=True)
                for folder in selected_folders:
                    shutil.copytree(folder, os.path.join(temp_dir, os.path.basename(folder)))
                shutil.make_archive(out_path, fmt, temp_dir)
                shutil.rmtree(temp_dir)
                self.arch_status.append(f"Created combined archive: {out_path}{ext}")
            
            QMessageBox.information(self, "Success", "Archiving completed successfully.")
        except Exception as e:
            self.arch_status.append(f"Error: {str(e)}")
            QMessageBox.critical(self, "Error", f"Archiving failed: {str(e)}")

    # --- Unarchiver Logic ---
    def select_unarch_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select Archives", "", "Archives (*.zip *.tar.gz)")
        if files:
            for f in files:
                self.unarch_list.addItem(f)

    def browse_unarch_out(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Extraction Directory")
        if dir_path:
            self.unarch_out_edit.setText(dir_path)

    def start_unarchiving(self):
        files = [self.unarch_list.item(i).text() for i in range(self.unarch_list.count())]
        if not files:
            QMessageBox.warning(self, "Error", "No archive files selected.")
            return

        self.unarch_status.clear()
        try:
            for arch_path in files:
                path_obj = Path(arch_path)
                out_dir = self.unarch_out_edit.text()
                if not out_dir:
                    # Default: extract into folder named after archive in same directory
                    out_dir = str(path_obj.parent / path_obj.stem.replace(".tar", ""))
                
                os.makedirs(out_dir, exist_ok=True)
                
                if arch_path.endswith(".zip"):
                    shutil.unpack_archive(arch_path, out_dir, "zip")
                elif arch_path.endswith(".tar.gz") or arch_path.endswith(".tgz"):
                    shutil.unpack_archive(arch_path, out_dir, "gztar")
                
                self.unarch_status.append(f"Extracted: {os.path.basename(arch_path)} -> {out_dir}")
            
            QMessageBox.information(self, "Success", "Unarchiving completed successfully.")
        except Exception as e:
            self.unarch_status.append(f"Error: {str(e)}")
            QMessageBox.critical(self, "Error", f"Unarchiving failed: {str(e)}")

    # --- Docs to PDF Logic ---
    def select_doc_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select Documents", "", "Documents (*.docx *.doc *.odt)")
        if files:
            for f in files:
                self.docs_list.addItem(f)

    def start_doc_conversion(self):
        files = [self.docs_list.item(i).text() for i in range(self.docs_list.count())]
        if not files:
            QMessageBox.warning(self, "Error", "No document files selected.")
            return

        self.docs_status.clear()
        self.docs_status.append("DOC-TO-PDF SECURITY NOTICE:")
        self.docs_status.append("-" * 30)
        self.docs_status.append("For compliance with RBI/SEBI security standards, this tool does NOT use third-party command-line software (like LibreOffice/Word) or external open-source conversion commands.")
        self.docs_status.append("\nCurrently, true offline document conversion (DOCX to PDF) without external rendering engines is not possible with pure Python standard libraries alone.")
        self.docs_status.append("\nRECOMMENDATION:")
        self.docs_status.append("To maintain zero-dependency compliance, we recommend integrating a secure, bank-approved conversion API (e.g., Adobe PDF Services API) which can be added here with an API key.")
        
        QMessageBox.information(self, "Security Notice", "Native document conversion requires a secure API for zero-dependency environments.")

    # --- Merger Logic ---
    def select_pdf_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select PDF Files", "", "PDF Files (*.pdf)")
        if files:
            for f in files:
                self.merge_list.addItem(f)

    def start_merging(self):
        if not PdfWriter:
            QMessageBox.critical(self, "Error", "pypdf library not found. Please install it.")
            return

        files = [self.merge_list.item(i).text() for i in range(self.merge_list.count())]
        if not files:
            QMessageBox.warning(self, "Error", "No PDF files selected.")
            return

        out_name = self.merge_name_edit.text() or "merged.pdf"
        if not out_name.endswith(".pdf"):
            out_name += ".pdf"
            
        save_path, _ = QFileDialog.getSaveFileName(self, "Save Merged PDF", out_name, "PDF Files (*.pdf)")
        if not save_path:
            return

        self.merge_status.clear()
        try:
            writer = PdfWriter()
            for f in files:
                reader = PdfReader(f)
                for page in reader.pages:
                    writer.add_page(page)
                self.merge_status.append(f"Added: {os.path.basename(f)}")
            
            with open(save_path, "wb") as out_f:
                writer.write(out_f)
            
            self.merge_status.append(f"\nSuccessfully created: {save_path}")
            QMessageBox.information(self, "Success", "PDFs merged successfully.")
        except Exception as e:
            self.merge_status.append(f"Error: {str(e)}")
            QMessageBox.critical(self, "Error", f"Merging failed: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RyanDashboard()
    window.show()
    sys.exit(app.exec())
