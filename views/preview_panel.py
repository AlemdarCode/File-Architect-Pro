"""
Preview Panel for File-Architect-Pro.
Dynamic right panel with STATE MANAGEMENT:
- Default: Shows "File Preview" with file info
- Action Mode: Shows settings form for the selected action

This panel switches content based on action selection.
"""

from pathlib import Path
from typing import Optional, Dict, Any

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QFrame, QStackedWidget, QTextEdit,
    QLineEdit, QSpinBox, QFormLayout, QCheckBox,
    QScrollArea, QSizePolicy
)


class FilePreviewWidget(QWidget):
    """Default view: File Preview with file information."""
    
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Initialize the UI components."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        
        # Centered placeholder when no file selected
        self._placeholder = QLabel("Select a file to preview")
        self._placeholder.setObjectName("PlaceholderLabel")
        self._placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._placeholder, 1)
        
        # File info container (hidden by default)
        self._info_container = QWidget()
        self._info_container.hide()
        info_layout = QVBoxLayout(self._info_container)
        info_layout.setContentsMargins(0, 0, 0, 0)
        info_layout.setSpacing(12)
        
        # File icon preview
        self._preview_image = QLabel()
        self._preview_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._preview_image.setMinimumHeight(100)
        info_layout.addWidget(self._preview_image)
        
        # File information form
        info_form = QFormLayout()
        info_form.setSpacing(8)
        info_form.setContentsMargins(0, 0, 0, 0)
        
        self._name_label = QLabel("-")
        self._name_label.setWordWrap(True)
        self._type_label = QLabel("-")
        self._size_label = QLabel("-")
        self._modified_label = QLabel("-")
        self._path_label = QLabel("-")
        self._path_label.setWordWrap(True)
        self._path_label.setObjectName("PathLabel")
        
        info_form.addRow("Name:", self._name_label)
        info_form.addRow("Type:", self._type_label)
        info_form.addRow("Size:", self._size_label)
        info_form.addRow("Modified:", self._modified_label)
        info_form.addRow("Path:", self._path_label)
        
        info_layout.addLayout(info_form)
        
        # Text preview for text files
        self._text_preview = QTextEdit()
        self._text_preview.setReadOnly(True)
        self._text_preview.setPlaceholderText("Content preview (text files only)")
        self._text_preview.setMaximumHeight(150)
        self._text_preview.hide()
        info_layout.addWidget(self._text_preview)
        
        info_layout.addStretch(1)
        
        layout.addWidget(self._info_container)
    
    def show_file_info(self, file_path: str) -> None:
        """Display information about the selected file."""
        try:
            path = Path(file_path)
            
            if not path.exists():
                self._show_placeholder("File not found")
                return
            
            self._placeholder.hide()
            self._info_container.show()
            
            # Update file info
            self._name_label.setText(path.name)
            self._type_label.setText(path.suffix if path.suffix else ("Folder" if path.is_dir() else "Unknown"))
            
            if path.is_file():
                size = path.stat().st_size
                self._size_label.setText(self._format_size(size))
                
                # Show text preview for text files
                if self._is_text_file(path):
                    self._show_text_preview(path)
                else:
                    self._text_preview.hide()
                    
                # Show image preview for image files
                if self._is_image_file(path):
                    self._show_image_preview(path)
                else:
                    icon = QIcon("icons/file-lines-solid.svg")
                    self._preview_image.setPixmap(icon.pixmap(48, 48))
            else:
                self._size_label.setText("-")
                self._text_preview.hide()
                icon = QIcon("icons/folder-open-solid.svg")
                self._preview_image.setPixmap(icon.pixmap(48, 48))
            
            # Modification time
            import datetime
            mtime = datetime.datetime.fromtimestamp(path.stat().st_mtime)
            self._modified_label.setText(mtime.strftime("%Y-%m-%d %H:%M"))
            
            self._path_label.setText(str(path))
            
        except PermissionError:
            self._show_placeholder("Permission denied")
        except Exception as e:
            self._show_placeholder(f"Error: {str(e)}")
    
    def _show_placeholder(self, text: str) -> None:
        """Show placeholder with message."""
        self._info_container.hide()
        self._placeholder.setText(text)
        self._placeholder.show()
    
    def _format_size(self, size: int) -> str:
        """Format file size in human-readable format."""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} PB"
    
    def _is_text_file(self, path: Path) -> bool:
        """Check if file is a text file."""
        text_extensions = {'.txt', '.md', '.py', '.js', '.html', '.css', 
                          '.json', '.xml', '.csv', '.log', '.ini', '.cfg',
                          '.yaml', '.yml', '.toml', '.bat', '.sh', '.ps1'}
        return path.suffix.lower() in text_extensions
    
    def _is_image_file(self, path: Path) -> bool:
        """Check if file is an image file."""
        image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.ico', '.webp'}
        return path.suffix.lower() in image_extensions
    
    def _show_text_preview(self, path: Path) -> None:
        """Show text content preview."""
        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read(2048)
                if len(content) == 2048:
                    content += "\n\n... (truncated)"
                self._text_preview.setText(content)
                self._text_preview.show()
        except Exception:
            self._text_preview.hide()
    
    def _show_image_preview(self, path: Path) -> None:
        """Show image preview."""
        try:
            pixmap = QPixmap(str(path))
            if not pixmap.isNull():
                scaled = pixmap.scaled(
                    160, 120, 
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                self._preview_image.setPixmap(scaled)
        except Exception:
            pass
    
    def clear(self) -> None:
        """Clear the preview."""
        self._show_placeholder("Select a file to preview")


class ActionSettingsWidget(QWidget):
    """
    Settings form for a specific action.
    Each action has its own configuration options.
    """
    
    settings_changed = pyqtSignal(dict)
    execute_requested = pyqtSignal()
    cancel_requested = pyqtSignal()
    
    def __init__(self, action_key: str, action_name: str, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._action_key = action_key
        self._action_name = action_name
        self._settings: Dict[str, Any] = {}
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Build the settings form based on action type."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        
        # Scrollable content area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 8, 0)
        content_layout.setSpacing(12)
        
        # Build action-specific form
        self._build_action_form(content_layout)
        
        content_layout.addStretch(1)
        scroll_area.setWidget(content)
        layout.addWidget(scroll_area, 1)
        
        # Action buttons at bottom
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        
        self._cancel_btn = QPushButton("Cancel")
        self._cancel_btn.clicked.connect(self.cancel_requested.emit)
        btn_layout.addWidget(self._cancel_btn)
        
        btn_layout.addStretch()
        
        self._execute_btn = QPushButton("Execute")
        self._execute_btn.clicked.connect(self.execute_requested.emit)
        btn_layout.addWidget(self._execute_btn)
        
        layout.addLayout(btn_layout)
    
    def _build_action_form(self, layout: QVBoxLayout) -> None:
        """Build action-specific form fields."""
        form = QFormLayout()
        form.setSpacing(10)
        form.setContentsMargins(0, 0, 0, 0)
        
        if self._action_key == "sequential_rename":
            # Sequential rename settings
            self._pattern_input = QLineEdit()
            self._pattern_input.setPlaceholderText("File_{n:03d}")
            form.addRow("Pattern:", self._pattern_input)
            
            self._start_num = QSpinBox()
            self._start_num.setRange(0, 99999)
            self._start_num.setValue(1)
            form.addRow("Start Number:", self._start_num)
            
            self._step = QSpinBox()
            self._step.setRange(1, 100)
            self._step.setValue(1)
            form.addRow("Step:", self._step)
            
            self._preserve_ext = QCheckBox("Preserve original extension")
            self._preserve_ext.setChecked(True)
            form.addRow("", self._preserve_ext)
            
        elif self._action_key == "prefix_suffix":
            self._prefix_input = QLineEdit()
            self._prefix_input.setPlaceholderText("Prefix text...")
            form.addRow("Prefix:", self._prefix_input)
            
            self._suffix_input = QLineEdit()
            self._suffix_input.setPlaceholderText("Suffix text...")
            form.addRow("Suffix:", self._suffix_input)
            
            self._before_ext = QCheckBox("Add suffix before extension")
            self._before_ext.setChecked(True)
            form.addRow("", self._before_ext)
            
        elif self._action_key == "find_replace":
            self._find_input = QLineEdit()
            self._find_input.setPlaceholderText("Text to find...")
            form.addRow("Find:", self._find_input)
            
            self._replace_input = QLineEdit()
            self._replace_input.setPlaceholderText("Replace with...")
            form.addRow("Replace:", self._replace_input)
            
            self._case_sensitive = QCheckBox("Case sensitive")
            form.addRow("", self._case_sensitive)
            
            self._use_regex = QCheckBox("Use regular expressions")
            form.addRow("", self._use_regex)
            
        elif self._action_key == "change_extension":
            self._from_ext = QLineEdit()
            self._from_ext.setPlaceholderText(".txt")
            form.addRow("From:", self._from_ext)
            
            self._to_ext = QLineEdit()
            self._to_ext.setPlaceholderText(".md")
            form.addRow("To:", self._to_ext)
            
        elif self._action_key == "secure_delete":
            info = QLabel("⚠️ Files will be permanently deleted and cannot be recovered.")
            info.setWordWrap(True)
            form.addRow(info)
            
            self._passes = QSpinBox()
            self._passes.setRange(1, 10)
            self._passes.setValue(3)
            form.addRow("Overwrite Passes:", self._passes)
            
        else:
            # Generic placeholder for unimplemented actions
            info = QLabel(f"Settings for '{self._action_name}' will be available in a future update.")
            info.setWordWrap(True)
            info.setObjectName("PlaceholderLabel")
            form.addRow(info)
        
        layout.addLayout(form)
    
    def get_settings(self) -> Dict[str, Any]:
        """Collect and return current settings from form fields."""
        settings = {"action": self._action_key}
        
        # Collect settings based on action type
        if self._action_key == "sequential_rename":
            settings["pattern"] = getattr(self, '_pattern_input', None) and self._pattern_input.text()
            settings["start"] = getattr(self, '_start_num', None) and self._start_num.value()
            settings["step"] = getattr(self, '_step', None) and self._step.value()
            settings["preserve_ext"] = getattr(self, '_preserve_ext', None) and self._preserve_ext.isChecked()
        
        elif self._action_key == "prefix_suffix":
            settings["prefix"] = getattr(self, '_prefix_input', None) and self._prefix_input.text()
            settings["suffix"] = getattr(self, '_suffix_input', None) and self._suffix_input.text()
            settings["before_ext"] = getattr(self, '_before_ext', None) and self._before_ext.isChecked()
        
        # Add more action types as needed
        
        return settings


class PreviewPanel(QFrame):
    """
    Dynamic right panel with STATE MANAGEMENT.
    
    States:
    - "preview": Default file preview (index 0)
    - "action": Action settings form (dynamic index)
    
    Signals:
        action_execute_requested: (action_key: str, settings: dict)
    """
    
    action_execute_requested = pyqtSignal(str, dict)
    
    # Action names for display
    ACTION_NAMES: Dict[str, str] = {
        "sequential_rename": "Sıralı Adlandırma",
        "prefix_suffix": "Ön/Son Ek Ekle",
        "find_replace": "Bul/Değiştir",
        "change_extension": "Uzantı Değiştir",
        "copy": "Kopyala",
        "tag": "Etiket",
        "single_folder": "Tek Klasör",
        "secure_delete": "Güvenli Sil",
        "merge_text": "Metin Birleştir",
        "csv_report": "CSV Rapor",
        "excel_report": "Excel Rapor",
    }
    
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setObjectName("PreviewPanel")
        self._current_mode = "preview"
        self._current_action: Optional[str] = None
        self._action_widgets: Dict[str, ActionSettingsWidget] = {}
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Initialize the UI components."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(10)
        
        # Header
        self._header_label = QLabel("File Preview")
        self._header_label.setObjectName("SectionHeader")
        layout.addWidget(self._header_label)
        
        # Header underline
        header_line = QFrame()
        header_line.setObjectName("HeaderLine")
        header_line.setFrameShape(QFrame.Shape.HLine)
        layout.addWidget(header_line)
        
        # Stacked widget for state switching
        self._stack = QStackedWidget()
        
        # Index 0: File preview (default)
        self._file_preview = FilePreviewWidget()
        self._stack.addWidget(self._file_preview)
        
        # Create action settings widgets (added to stack dynamically)
        self._create_action_widgets()
        
        layout.addWidget(self._stack, 1)
    
    def _create_action_widgets(self) -> None:
        """Create settings widgets for each action type."""
        for action_key, action_name in self.ACTION_NAMES.items():
            widget = ActionSettingsWidget(action_key, action_name)
            widget.execute_requested.connect(
                lambda ak=action_key: self._on_execute_requested(ak)
            )
            widget.cancel_requested.connect(self.show_preview)
            self._action_widgets[action_key] = widget
            self._stack.addWidget(widget)
    
    def _on_execute_requested(self, action_key: str) -> None:
        """Handle action execution request."""
        if action_key in self._action_widgets:
            settings = self._action_widgets[action_key].get_settings()
            self.action_execute_requested.emit(action_key, settings)
    
    def show_preview(self) -> None:
        """Switch to file preview mode (default state)."""
        self._current_mode = "preview"
        self._current_action = None
        self._header_label.setText("File Preview")
        self._stack.setCurrentIndex(0)
    
    def show_action_settings(self, action_key: str) -> None:
        """
        Switch to action settings mode.
        Called when user clicks an action button.
        """
        if action_key in self._action_widgets:
            self._current_mode = "action"
            self._current_action = action_key
            
            # Update header to show action name
            action_name = self.ACTION_NAMES.get(action_key, action_key)
            self._header_label.setText(f"{action_name} Settings")
            
            # Switch to action widget
            widget = self._action_widgets[action_key]
            index = self._stack.indexOf(widget)
            self._stack.setCurrentIndex(index)
    
    def update_file_preview(self, file_path: str) -> None:
        """Update file preview with new file (only in preview mode)."""
        if self._current_mode == "preview":
            self._file_preview.show_file_info(file_path)
    
    def clear_preview(self) -> None:
        """Clear the file preview."""
        self._file_preview.clear()
    
    def get_current_mode(self) -> str:
        """Return current panel mode: 'preview' or 'action'."""
        return self._current_mode
