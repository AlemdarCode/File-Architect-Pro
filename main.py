"""
File-Architect-Pro - Responsive Layout
Paneller pencere boyutuyla orantılı olarak genişler.
"""

import sys
from pathlib import Path
from datetime import datetime
from PyQt6.QtCore import (
    Qt, pyqtSignal, QModelIndex, QDir, QSize, QTimer, 
    QRect, QEvent, QFileInfo, QItemSelection, QDate
)
from PyQt6.QtGui import (
    QIcon, QPainter, QAbstractFileIconProvider, 
    QFileSystemModel, QColor, QPen, QPalette,
    QLinearGradient, QBrush
)
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTreeView, QLabel, QPushButton, QFrame, QFileDialog,
    QStyledItemDelegate, QStyleOptionViewItem, QStyle,
    QSizePolicy, QStackedWidget, QTextEdit,
    QLineEdit, QSpinBox, QDoubleSpinBox, QFormLayout, QMessageBox, QGridLayout,
    QButtonGroup, QCheckBox, QComboBox, QDateEdit, QScrollArea, QWidget
)


# =============================================================================
# STYLE SHEET
# =============================================================================

STYLE_SHEET = """
* {
    outline: 0;
    font-family: "Segoe UI", Arial, sans-serif;
}

QMainWindow {
    background-color: #F9F8F2;
}

QWidget {
    font-size: 12px;
    color: #444444;
    selection-background-color: #D7D6D2;
    selection-color: #444444;
}

QFrame#SourcePanel {
    background-color: #E7E6E2;
    border: 1px solid #D7D6D2;
    border-radius: 5px;
}

QFrame#FiltersPanel, QFrame#ActionsPanel {
    background-color: #F0EFEB;
    border: 1px solid #D7D6D2;
    border-radius: 5px;
}

QFrame#PreviewPanel {
    background-color: #F9F8F2;
    border: 1px solid #D7D6D2;
    border-radius: 5px;
}

QLabel#SectionHeader {
    color: #444444;
    font-size: 13px;
    font-weight: bold;
    padding: 1px 0px;
}

QFrame#VerticalSeparator {
    background-color: #D8D7D3;
    min-width: 2px;
    max-width: 2px;
}

/* Header lines removed */

QTreeView {
    background-color: transparent;
    border: none;
    outline: 0;
    color: #7D7D7B;
    font-size: 11px;
}

QTreeView::item {
    padding: 3px 2px;
    min-height: 24px;
    border: none;
}

QTreeView::item:hover {
    background-color: #D7D6D2;
}

QTreeView::item:selected {
    background-color: #D7D6D2;
    color: #444444;
    border: none;
}

QTreeView::branch {
    background: transparent;
    border-image: none;
    image: none;
}

/* Remove blue selection on branch areas */
QTreeView::branch:selected {
    background: transparent;
}

QTreeView::branch:hover {
    background: transparent;
}

/* Remove all branch indicator images on selection */
QTreeView::branch:has-siblings:!adjoins-item:selected,
QTreeView::branch:has-siblings:adjoins-item:selected,
QTreeView::branch:!has-children:!has-siblings:adjoins-item:selected,
QTreeView::branch:has-children:closed:has-siblings:selected,
QTreeView::branch:has-children:opened:has-siblings:selected,
QTreeView::branch:has-children:closed:selected,
QTreeView::branch:has-children:opened:selected {
    background: transparent;
    border-image: none;
    image: none;
}

/* Remove branch lines for all states */
QTreeView::branch:has-siblings:!adjoins-item,
QTreeView::branch:has-siblings:adjoins-item,
QTreeView::branch:!has-children:!has-siblings:adjoins-item,
QTreeView::branch:has-children:closed:has-siblings,
QTreeView::branch:has-children:opened:has-siblings,
QTreeView::branch:has-children:closed,
QTreeView::branch:has-children:opened {
    background: transparent;
    border-image: none;
    image: none;
}

QPushButton {
    background-color: #D7D6D2;
    color: #444444;
    border: 1px solid #C8C8C4;
    border-radius: 3px;
    padding: 1px 8px;
    min-height: 20px;
    max-height: 22px;
    font-size: 11px;
}

QPushButton:hover {
    background-color: #C8C8C4;
    border-color: #444444;
}

QPushButton:pressed, QPushButton:checked {
    background-color: #BCBCB8;
}

QPushButton#ListBtn {
    min-height: 20px;
    max-height: 22px;
    max-width: 160px;
    padding: 1px 6px;
    text-align: center;
    font-size: 12px;
    font-weight: bold;
}

QPushButton#BrowseBtn {
    min-height: 24px;
    max-height: 28px;
    padding: 4px 12px;
    font-size: 11px;
}

QScrollBar:vertical {
    background: transparent;
    width: 5px;
}

QScrollBar::handle:vertical {
    background: #C8C8C4;
    border-radius: 2px;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QDateEdit {
    background-color: #FFFFFF;
    color: #333333;
    border: 1px solid #D7D6D2;
    border-radius: 3px;
    padding: 3px 6px;
    min-height: 20px;
    font-size: 11px;
}

QComboBox::drop-down {
    border: none;
    background: transparent;
    width: 20px;
}

/* Modern SpinBox & DateEdit Styles - User Requested Design */
QSpinBox, QDoubleSpinBox, QDateEdit {
    border: 2px solid #D1D1D1;
    border-radius: 10px;
    padding: 2px 10px;
    padding-right: 30px; /* Butonlar için boşluk */
    background-color: white;
    font-size: 13px; /* Uygulama geneli için uygun boyut */
    font-weight: bold;
    color: #333;
    min-height: 36px;
    selection-background-color: #0078D7;
}

/* Yukarı butonu tasarımı */
QSpinBox::up-button, QDoubleSpinBox::up-button, QDateEdit::up-button {
    subcontrol-origin: border;
    subcontrol-position: top right;
    width: 30px;
    border-left: 1px solid #D1D1D1;
    border-bottom: 1px solid #D1D1D1;
    border-top-right-radius: 10px;
    background-color: #ffffff;
    margin: 0px;
}

/* Aşağı butonu tasarımı */
QSpinBox::down-button, QDoubleSpinBox::down-button, QDateEdit::down-button {
    subcontrol-origin: border;
    subcontrol-position: bottom right;
    width: 30px;
    border-left: 1px solid #D1D1D1;
    border-top: 0px solid #D1D1D1; /* Up button border handles separator */
    border-bottom-right-radius: 10px;
    background-color: #ffffff;
    margin: 0px;
}

/* Blok oklardan kurtulup ince ok (chevron/triangle) ekleme */
QSpinBox::up-arrow, QDoubleSpinBox::up-arrow, QDateEdit::up-arrow {
    image: none; /* Varsayılan blok oku kaldır */
    width: 0; 
    height: 0;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-bottom: 5px solid #555; /* Üçgen ok oluşturur */
}

QSpinBox::down-arrow, QDoubleSpinBox::down-arrow, QDateEdit::down-arrow {
    image: none; /* Varsayılan blok oku kaldır */
    width: 0; 
    height: 0;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 5px solid #555; /* Üçgen ok oluşturur */
}

/* Fare üzerine gelince efekt */
QSpinBox::up-button:hover, QSpinBox::down-button:hover,
QDoubleSpinBox::up-button:hover, QDoubleSpinBox::down-button:hover,
QDateEdit::up-button:hover, QDateEdit::down-button:hover {
    background-color: #f0f0f0;
} 

QSpinBox::up-button:pressed, QSpinBox::down-button:pressed,
QDoubleSpinBox::up-button:pressed, QDoubleSpinBox::down-button:pressed,
QDateEdit::up-button:pressed, QDateEdit::down-button:pressed {
    background-color: #e0e0e0;
}

QToolTip {
    background-color: #FFFFF0;
    color: #333333;
    border: 1px solid #CCCCCC;
    padding: 4px;
    font-size: 11px;
}



QTextEdit {
    background: white;
    border: 1px solid #D7D6D2;
    border-radius: 3px;
    font-size: 10px;
}

QLabel#PathLabel {
    color: #7D7D7B;
    font-size: 9px;
}

QLabel#PlaceholderLabel {
    color: #7D7D7B;
    font-size: 11px;
}

/* ComboBox Dropdown (Light Theme) */
QComboBox QAbstractItemView {
    background-color: #FFFFFF;
    color: #333333;
    border: 1px solid #CCCCCC;
    selection-background-color: #E8E8E8;
    selection-color: #333333;
}

/* Calendar Widget (Light Theme) */
QCalendarWidget {
    background-color: #FFFFFF;
}
QCalendarWidget QWidget {
    background-color: #FFFFFF;
    color: #333333;
}
QCalendarWidget QAbstractItemView:enabled {
    background-color: #FFFFFF;
    color: #333333;
    selection-background-color: #E0E0E0;
    selection-color: #333333;
}
QCalendarWidget QWidget#qt_calendar_navigationbar {
    background-color: #F0F0F0;
}
QCalendarWidget QToolButton {
    background-color: #F0F0F0;
    color: #333333;
}
QCalendarWidget QToolButton:hover {
    background-color: #E0E0E0;
}

/* MessageBox (Light Theme) */
QMessageBox {
    background-color: #F9F8F2;
}
QMessageBox QLabel {
    color: #333333;
}
QMessageBox QPushButton {
    min-width: 80px;
}
"""


# =============================================================================
# GRADIENT LINE WIDGET
# =============================================================================

class GradientLine(QWidget):
    """Vertical line with gradient - full color in center, fades to transparent at edges."""
    
    def __init__(self, color="#D8D7D3", width=2):
        super().__init__()
        self._color = QColor(color)
        self._width = width
        self.setFixedWidth(width + 4)  # Line width + padding
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        h = self.height()
        w = self.width()
        x = w // 2
        
        # Create vertical gradient: transparent -> full color -> transparent
        gradient = QLinearGradient(0, 0, 0, h)
        
        color_transparent = QColor(self._color)
        color_transparent.setAlpha(0)
        
        # Top: transparent
        gradient.setColorAt(0.0, color_transparent)
        # Middle: full color
        gradient.setColorAt(0.3, self._color)
        gradient.setColorAt(0.7, self._color)
        # Bottom: transparent
        gradient.setColorAt(1.0, color_transparent)
        
        # Draw the line
        pen = QPen(QBrush(gradient), self._width)
        painter.setPen(pen)
        painter.drawLine(x, 0, x, h)


# =============================================================================
# ICON PROVIDER
# =============================================================================

class IconProvider(QAbstractFileIconProvider):
    def __init__(self):
        super().__init__()
        self._folder = QIcon("icons/folder-open-solid.svg")
        self._file = QIcon("icons/file-lines-solid.svg")
        self._image = QIcon("icons/image-solid.svg")
        self._music = QIcon("icons/music-solid.svg")
        
    def icon(self, info) -> QIcon:
        if isinstance(info, QAbstractFileIconProvider.IconType):
            return self._folder if info == QAbstractFileIconProvider.IconType.Folder else self._file
        if isinstance(info, QFileInfo):
            if info.isDir():
                return self._folder
            ext = info.suffix().lower()
            if ext in ['png', 'jpg', 'jpeg', 'gif', 'bmp', 'svg', 'webp']:
                return self._image
            if ext in ['mp3', 'wav', 'flac', 'm4a', 'ogg']:
                return self._music
            return self._file
        return self._file


# =============================================================================
# TREE DELEGATE
# =============================================================================

class TreeDelegate(QStyledItemDelegate):
    delete_clicked = pyqtSignal(QModelIndex)
    
    LINE_COLOR = QColor("#AAAAAA")  # Darker, more visible
    ROW_HEIGHT = 26
    ICON_CENTER = 13
    
    def __init__(self, tree_view, model):
        super().__init__(tree_view)
        self._tree = tree_view
        self._model = model
        self._xicon = QIcon("icons/xmark-solid.svg")
    
    def paint(self, painter, option, index):
        painter.save()
        self._draw_lines(painter, option, index)
        
        content_rect = QRect(option.rect)
        content_rect.setRight(content_rect.right() - 20)
        opt = QStyleOptionViewItem(option)
        opt.rect = content_rect
        super().paint(painter, opt, index)
        
        xr = self._x_icon_rect(option.rect)
        painter.setOpacity(0.9 if option.state & QStyle.StateFlag.State_MouseOver else 0.25)
        self._xicon.paint(painter, xr)
        painter.restore()
    
    def _draw_lines(self, painter, option, index):
        # Use integer width + cosmetic pen for consistent thickness
        pen = QPen(self.LINE_COLOR, 1, Qt.PenStyle.SolidLine)
        pen.setCosmetic(True)
        painter.setPen(pen)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, False)
        
        indent = self._tree.indentation()
        rect = option.rect
        line_y = rect.top() + self.ICON_CENTER
        
        # Build ancestor chain from index up to root
        ancestors = []
        current = index
        while current.parent().isValid():
            ancestors.append(current)
            current = current.parent()
        
        depth = len(ancestors)
        if depth == 0:
            return
        
        # Draw lines for each level
        for i, ancestor in enumerate(ancestors):
            level = i + 1  # 1-based level (1 = direct parent)
            x = rect.left() - (indent * level) + 8  # Center of icon at this level
            
            if level == 1:
                # Direct parent connection: corner + horizontal
                # Vertical from top to icon center
                painter.drawLine(x, rect.top(), x, line_y)
                # Horizontal to item
                painter.drawLine(x, line_y, rect.left() - 1, line_y)
                # Continue down if current item has next sibling
                if self._has_next_sibling(index):
                    painter.drawLine(x, line_y, x, rect.bottom() + 1)
            else:
                # Ancestor level: draw vertical continuation if ancestor has next sibling
                if self._has_next_sibling(ancestor):
                    painter.drawLine(x, rect.top(), x, rect.bottom() + 1)
    
    def _has_next_sibling(self, index):
        if not index.isValid():
            return False
        return index.row() < self._model.rowCount(index.parent()) - 1
    
    def _x_rect(self, rect: QRect) -> QRect:
        # Icon size 11px but click area 20px for easier clicking
        sz = 20
        icon_sz = 11
        return QRect(rect.right() - sz - 2, rect.top() + self.ICON_CENTER - sz // 2, sz, sz)
    
    def _x_icon_rect(self, rect: QRect) -> QRect:
        # Actual icon drawing rect
        sz = 11
        return QRect(rect.right() - sz - 6, rect.top() + self.ICON_CENTER - sz // 2, sz, sz)
    
    def editorEvent(self, event, model, option, index):
        if event.type() == QEvent.Type.MouseButtonRelease:
            if self._x_rect(option.rect).contains(event.pos()):
                self.delete_clicked.emit(index)
                return True
        return super().editorEvent(event, model, option, index)
    
    def sizeHint(self, option, index):
        s = super().sizeHint(option, index)
        s.setHeight(self.ROW_HEIGHT)
        return s


# =============================================================================
# SOURCE PANEL
# =============================================================================

class SourcePanel(QFrame):
    file_selected = pyqtSignal(str)
    dir_selected = pyqtSignal(str)
    delete_requested = pyqtSignal(str)
    selection_changed = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.setObjectName("SourcePanel")
        self._root = None
        self._build()
    
    def _build(self):
        lay = QVBoxLayout(self)
        lay.setContentsMargins(8, 8, 8, 8)
        lay.setSpacing(6)
        
        hdr = QHBoxLayout()
        hdr.setSpacing(6)
        lbl = QLabel("Source Directory")
        lbl.setObjectName("SectionHeader")
        hdr.addWidget(lbl)
        hdr.addStretch()
        btn = QPushButton("Browse")
        btn.setObjectName("BrowseBtn")
        btn.setIcon(QIcon("icons/folder-open-solid.svg"))
        btn.setIconSize(QSize(14, 14))
        btn.clicked.connect(self._browse)
        hdr.addWidget(btn)
        lay.addLayout(hdr)
        
        # Header line removed

        
        self._tree = QTreeView()
        self._tree.setHeaderHidden(True)
        self._tree.setIndentation(16)
        self._tree.setAnimated(True)
        self._tree.setMouseTracking(True)
        self._tree.setRootIsDecorated(False)
        self._tree.setUniformRowHeights(True)
        self._tree.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        
        self._icons = IconProvider()
        self._model = QFileSystemModel()
        self._model.setIconProvider(self._icons)
        self._model.setFilter(QDir.Filter.AllDirs | QDir.Filter.Files | QDir.Filter.NoDotAndDotDot)
        self._tree.setModel(self._model)
        
        for c in range(1, 4):
            self._tree.setColumnHidden(c, True)
        
        self._delegate = TreeDelegate(self._tree, self._model)
        self._delegate.delete_clicked.connect(self._on_del)
        self._tree.setItemDelegate(self._delegate)
        self._tree.selectionModel().selectionChanged.connect(self._on_selection_changed)
        self._tree.expanded.connect(self._on_expand)
        
        lay.addWidget(self._tree, 1)
        
        self._path_lbl = QLabel("No folder selected")
        self._path_lbl.setObjectName("PathLabel")
        self._path_lbl.setWordWrap(True)
        lay.addWidget(self._path_lbl)
    
    def _browse(self):
        p = QFileDialog.getExistingDirectory(self, "Select Folder", str(Path.home()))
        if p:
            self.set_root(p)
    
    def set_root(self, path: str):
        try:
            self._root = Path(path)
            idx = self._model.setRootPath(path)
            self._tree.setRootIndex(idx)
            self._path_lbl.setText(path)
            self.dir_selected.emit(path)
            QTimer.singleShot(100, lambda: self._expand(idx, 10))  # Expand all subfolders
        except Exception as e:
            self._path_lbl.setText(str(e))
    
    def _expand(self, parent, depth):
        if depth <= 0 or not parent.isValid():
            return
        if self._model.canFetchMore(parent):
            self._model.fetchMore(parent)
        self._tree.expand(parent)
        for r in range(self._model.rowCount(parent)):  # Expand all, not just first 8
            ch = self._model.index(r, 0, parent)
            if ch.isValid() and self._model.isDir(ch):
                self._expand(ch, depth - 1)
    
    def _on_expand(self, idx):
        """When a folder is expanded, fetch and expand all its children."""
        if self._model.canFetchMore(idx):
            self._model.fetchMore(idx)
        # Expand all children after a short delay
        QTimer.singleShot(50, lambda: self._expand_children(idx))
    
    def _expand_children(self, parent):
        """Recursively expand all child folders."""
        for r in range(self._model.rowCount(parent)):
            ch = self._model.index(r, 0, parent)
            if ch.isValid() and self._model.isDir(ch):
                if self._model.canFetchMore(ch):
                    self._model.fetchMore(ch)
                self._tree.expand(ch)
    
    def _on_selection_changed(self, selected: QItemSelection, deselected: QItemSelection):
        indexes = selected.indexes()
        if indexes:
            path = self._model.filePath(indexes[0])
            if path:
                self.selection_changed.emit(path)
    
    def _on_del(self, idx):
        p = self._model.filePath(idx)
        if p:
            self.delete_requested.emit(p)


# =============================================================================
# FILTER CHIP WIDGET
# =============================================================================

class FilterChip(QWidget):
    """A small chip showing active filter with remove button."""
    removed = pyqtSignal(str)  # filter_id
    
    def __init__(self, filter_id: str, description: str):
        super().__init__()
        self.filter_id = filter_id
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        
        lay = QHBoxLayout(self)
        lay.setContentsMargins(6, 3, 4, 3)
        lay.setSpacing(6)
        
        lbl = QLabel(description)
        lbl.setStyleSheet("font-size: 10px; color: #444; background: transparent; border: none;")
        lay.addWidget(lbl)
        
        btn_x = QPushButton("✕")
        btn_x.setFixedSize(18, 18)
        btn_x.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_x.setStyleSheet("""
            QPushButton { 
                background: #E8E8E8; 
                border: 1px solid #CCC; 
                border-radius: 9px;
                color: #888;
                font-size: 11px;
                font-weight: bold;
            }
            QPushButton:hover { background: #D88; color: #FFF; border-color: #C66; }
        """)
        btn_x.clicked.connect(lambda: self.removed.emit(self.filter_id))
        lay.addWidget(btn_x)
        
        self.setStyleSheet("background: #F5F5F5; border: 1px solid #DDD; border-radius: 4px;")

# =============================================================================
# FILTER SETTINGS UI (RIGHT SIDE)
# =============================================================================

class FilterSettingsPanel(QWidget):
    filter_added = pyqtSignal(str, str, dict)  # filter_type, filter_id, settings
    filter_removed = pyqtSignal(str)  # filter_id
    
    MAX_FILTERS = 5
    
    def __init__(self):
        super().__init__()
        self.forms = {}
        self.active_filters = {}  # filter_id -> FilterChip
        self._current_filter_type = None
        self._build()

    def _build(self):
        # Dinamik genişlik - minimum tanımlı
        self.setMinimumWidth(250)
        
        lay = QVBoxLayout(self)
        lay.setContentsMargins(12, 8, 12, 8)
        lay.setSpacing(8)
        
        # Header - sabit yükseklik
        self.header_lbl = QLabel("Filtre Ayarları")
        self.header_lbl.setFixedHeight(20)
        self.header_lbl.setStyleSheet("font-weight: bold; font-size: 13px; color: #333;")
        lay.addWidget(self.header_lbl)
        
        # Stack - sabit yükseklik
        self.stack = QStackedWidget()
        self.stack.setFixedHeight(140)
        lay.addWidget(self.stack)
        
        # Forms
        self._init_forms()
        
        # Buttons - sabit boyutlar
        btn_lay = QHBoxLayout()
        btn_lay.setContentsMargins(0, 0, 0, 0)
        btn_lay.setSpacing(6)
        
        self.btn_add = QPushButton("Filtre Ekle")
        self.btn_add.setFixedWidth(80)
        self.btn_add.setFixedHeight(24)
        self.btn_add.clicked.connect(self._on_add_filter)
        
        self.btn_reset = QPushButton("Sıfırla")
        self.btn_reset.setFixedWidth(60)
        self.btn_reset.setFixedHeight(24)
        self.btn_reset.clicked.connect(self._on_reset)
        
        self.btn_cancel = QPushButton("İptal")
        self.btn_cancel.setFixedWidth(50)
        self.btn_cancel.setFixedHeight(24)
        self.btn_cancel.clicked.connect(self._on_cancel)
        
        btn_lay.addWidget(self.btn_add)
        btn_lay.addWidget(self.btn_reset)
        btn_lay.addWidget(self.btn_cancel)
        btn_lay.addStretch()
        lay.addLayout(btn_lay)
        
        # Separator
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setFixedHeight(2)
        sep.setStyleSheet("background: #ccc;")
        lay.addWidget(sep)
        
        # Active Filters Label
        lbl_active = QLabel("Aktif Filtreler")
        lbl_active.setFixedHeight(18)
        lbl_active.setStyleSheet("font-weight: bold; font-size: 12px;")
        lay.addWidget(lbl_active)
        
        # Chips container - sabit yükseklik
        self.chips_container = QWidget()
        self.chips_container.setFixedHeight(60)
        self.chips_lay = QGridLayout(self.chips_container)
        self.chips_lay.setContentsMargins(0, 0, 0, 0)
        self.chips_lay.setSpacing(4)
        self._chip_row = 0
        self._chip_col = 0
        self._max_cols = 2
        lay.addWidget(self.chips_container)
        
    def _init_forms(self):
        # 1. Uzantı
        f_ext = QWidget()
        l_ext = QVBoxLayout(f_ext)
        l_ext.setContentsMargins(0, 0, 0, 0)
        l_ext.setSpacing(4)
        lbl_ext = QLabel("Uzantılar (örn: jpg, png):")
        lbl_ext.setToolTip("Virgülle ayrılmış dosya uzantıları girin.")
        ext_input = QLineEdit()
        ext_input.setToolTip("Örnek: jpg, png, txt")
        ext_input.setPlaceholderText("jpg, png, pdf, docx...")
        
        # Yaygın uzantılar bilgisi
        ext_info = QLabel("Yaygın: jpg, png, gif, pdf, docx, xlsx, txt, mp3, mp4, zip")
        ext_info.setStyleSheet("color: #888888; font-size: 9px;")
        
        l_ext.addWidget(lbl_ext)
        l_ext.addWidget(ext_input)
        l_ext.addWidget(ext_info)
        l_ext.addStretch()
        self._add_stack("Uzantı", f_ext)
        
        # 2. Dosya Adı
        f_name = QWidget()
        l_name = QVBoxLayout(f_name)
        l_name.setContentsMargins(0, 0, 0, 0)
        l_name.setSpacing(3)
        lbl_name = QLabel("Arama Metni:")
        lbl_name.setToolTip("Dosya adında aranacak metin.")
        name_input = QLineEdit()
        name_input.setToolTip("Dosya adında aranacak kelimeyi girin.")
        cb_case = QCheckBox("Harf Duyarlı")
        cb_case.setToolTip("ABC ile abc farklı kabul edilir.")
        cb_exact = QCheckBox("Tam Eşleşme")
        cb_exact.setToolTip("Dosya adı tam olarak girilen metin olmalı.")
        cb_invert = QCheckBox("Tersini Al")
        cb_invert.setToolTip("Metni İÇERMEYEN dosyalar gösterilir.")
        l_name.addWidget(lbl_name)
        l_name.addWidget(name_input)
        l_name.addWidget(cb_case)
        l_name.addWidget(cb_exact)
        l_name.addWidget(cb_invert)
        l_name.addStretch()
        self._add_stack("Dosya Adı", f_name)
        
        # 3. Metin (İçerik)
        f_content = QWidget()
        l_content = QVBoxLayout(f_content)
        l_content.setContentsMargins(0, 0, 0, 0)
        l_content.setSpacing(6)
        lbl_content = QLabel("Dosya İçeriği (Metin):")
        lbl_content.setToolTip("Dosyanın içinde aranacak metin.")
        content_input = QLineEdit()
        content_input.setToolTip("Dosya içeriğinde aranacak kelimeyi girin.")
        cb_content_case = QCheckBox("Büyük/Küçük Harf Duyarlı")
        cb_content_case.setToolTip("İşaretlenirse, harf duyarlılığı aktif olur.")
        l_content.addWidget(lbl_content)
        l_content.addWidget(content_input)
        l_content.addWidget(cb_content_case)
        l_content.addStretch()
        self._add_stack("Metin", f_content)
        
        # 4. Regex
        f_regex = QWidget()
        l_regex = QVBoxLayout(f_regex)
        l_regex.setContentsMargins(0, 0, 0, 0)
        l_regex.setSpacing(6)
        lbl_regex = QLabel("Regular Expression:")
        lbl_regex.setToolTip("Gelişmiş desen eşleştirme için regex deseni girin.")
        regex_input = QLineEdit()
        regex_input.setToolTip("Örnek: ^image_\\d+\\.png$")
        l_regex.addWidget(lbl_regex)
        l_regex.addWidget(regex_input)
        l_regex.addStretch()
        self._add_stack("Regex", f_regex)
        
        # 5. Metin Yok
        f_nocontent = QWidget()
        l_nocontent = QVBoxLayout(f_nocontent)
        l_nocontent.setContentsMargins(0, 0, 0, 0)
        l_nocontent.setSpacing(6)
        lbl_nocontent = QLabel("İçermeyen Metin:")
        lbl_nocontent.setToolTip("Dosya içeriğinde OLMAMASI gereken metin.")
        nocontent_input = QLineEdit()
        nocontent_input.setToolTip("Bu metni içermeyen dosyalar gösterilecek.")
        l_nocontent.addWidget(lbl_nocontent)
        l_nocontent.addWidget(nocontent_input)
        l_nocontent.addStretch()
        self._add_stack("Metin Yok", f_nocontent)
        
        # 6. Boyut
        f_size = QWidget()
        l_size = QVBoxLayout(f_size)
        l_size.setContentsMargins(0, 0, 0, 0)
        l_size.setSpacing(4)
        
        lbl_op = QLabel("Operatör:")
        cb_op = QComboBox()
        cb_op.addItems(["> Büyük", "< Küçük", "= Eşit"])
        cb_op.setToolTip("Karşılaştırma şekli")
        
        lbl_val = QLabel("Değer:")
        sb_val = QDoubleSpinBox()
        sb_val.setRange(0, 999999)
        sb_val.setToolTip("Boyut değeri")
        
        lbl_unit = QLabel("Birim:")
        cb_unit = QComboBox()
        cb_unit.addItems(["MB", "KB", "GB", "Byte"])
        cb_unit.setToolTip("Boyut birimi")
        
        l_size.addWidget(lbl_op)
        l_size.addWidget(cb_op)
        l_size.addWidget(lbl_val)
        l_size.addWidget(sb_val)
        l_size.addWidget(lbl_unit)
        l_size.addWidget(cb_unit)
        l_size.addStretch()
        self._add_stack("Boyut", f_size)
        
        # 7. Boş Dosya
        f_empty = QWidget()
        l_empty = QVBoxLayout(f_empty)
        l_empty.setContentsMargins(0, 0, 0, 0)
        l_empty.setSpacing(6)
        lbl_empty = QLabel("Boş dosyaları (0 byte) göster.")
        lbl_empty.setToolTip("Hiç içeriği olmayan dosyaları filtreler.")
        l_empty.addWidget(lbl_empty)
        l_empty.addStretch()
        self._add_stack("Boş Dosya", f_empty)
        
        # 8. Tarih (Oluşturma)
        f_date = QWidget()
        l_date = QVBoxLayout(f_date)
        l_date.setContentsMargins(0, 0, 0, 0)
        l_date.setSpacing(6)
        
        lbl_start = QLabel("Başlangıç:")
        lbl_start.setToolTip("Tarih aralığının başlangıcı.")
        de_start = QDateEdit()
        de_start.setToolTip("Başlangıç tarihini seçin.")
        de_start.setCalendarPopup(True)
        de_start.setDate(QDate.currentDate())
        
        lbl_end = QLabel("Bitiş:")
        lbl_end.setToolTip("Tarih aralığının bitişi.")
        de_end = QDateEdit()
        de_end.setToolTip("Bitiş tarihini seçin.")
        de_end.setCalendarPopup(True)
        de_end.setDate(QDate.currentDate())
        
        l_date.addWidget(lbl_start)
        l_date.addWidget(de_start)
        l_date.addWidget(lbl_end)
        l_date.addWidget(de_end)
        l_date.addStretch()
        self._add_stack("Oluşturma Tarihi", f_date)
        
        # 9. Tarih (Değişiklik)
        f_date2 = QWidget()
        l_date2 = QVBoxLayout(f_date2)
        l_date2.setContentsMargins(0, 0, 0, 0)
        l_date2.setSpacing(6)
        
        lbl_start2 = QLabel("Başlangıç:")
        lbl_start2.setToolTip("Tarih aralığının başlangıcı.")
        de_start2 = QDateEdit()
        de_start2.setToolTip("Başlangıç tarihini seçin.")
        de_start2.setCalendarPopup(True)
        de_start2.setDate(QDate.currentDate())
        
        lbl_end2 = QLabel("Bitiş:")
        lbl_end2.setToolTip("Tarih aralığının bitişi.")
        de_end2 = QDateEdit()
        de_end2.setToolTip("Bitiş tarihini seçin.")
        de_end2.setCalendarPopup(True)
        de_end2.setDate(QDate.currentDate())
        
        l_date2.addWidget(lbl_start2)
        l_date2.addWidget(de_start2)
        l_date2.addWidget(lbl_end2)
        l_date2.addWidget(de_end2)
        l_date2.addStretch()
        self._add_stack("Değişiklik Tarihi", f_date2)

        # 10. Şifreli
        f_bool = QWidget()
        l_bool = QVBoxLayout(f_bool)
        l_bool.setContentsMargins(0, 0, 0, 0)
        l_bool.setSpacing(6)
        lbl_enc = QLabel("Şifreli dosyaları filtreler.")
        lbl_enc.setToolTip("Windows'ta şifreli olarak işaretlenmiş dosyaları bulur.")
        l_bool.addWidget(lbl_enc)
        l_bool.addStretch()
        self._add_stack("Şifreli", f_bool)
        
        # 11. Gizli
        f_hidden = QWidget()
        l_hidden = QVBoxLayout(f_hidden)
        l_hidden.setContentsMargins(0, 0, 0, 0)
        l_hidden.setSpacing(6)
        lbl_hid = QLabel("Gizli dosyaları göster.")
        lbl_hid.setToolTip("Windows'ta gizli olarak işaretlenmiş dosyaları bulur.")
        l_hidden.addWidget(lbl_hid)
        l_hidden.addStretch()
        self._add_stack("Gizli", f_hidden)
        
        # Default placeholder
        f_def = QWidget()
        l_def = QVBoxLayout(f_def)
        l_def.setContentsMargins(0, 0, 0, 0)
        l_def.addWidget(QLabel("Soldan bir filtre seçiniz."))
        l_def.addStretch()
        self.stack.addWidget(f_def)

    def _add_stack(self, name, widget):
        idx = self.stack.addWidget(widget)
        self.forms[name] = idx

    def show_form(self, name):
        self._current_filter_type = name
        self.header_lbl.setText(f"{name} Ayarları")
        if name in self.forms:
            self.stack.setCurrentIndex(self.forms[name])
        else:
            self.stack.setCurrentIndex(self.stack.count()-1)
    
    def _on_add_filter(self):
        """Called when 'Filtre Ekle' button is clicked."""
        if not self._current_filter_type:
            return
        if len(self.active_filters) >= self.MAX_FILTERS:
            return
        
        # Generate unique filter ID
        import uuid
        filter_id = str(uuid.uuid4())[:8]
        
        # Get description based on filter type
        desc = self._get_filter_description()
        if not desc:
            return
        
        # Create chip
        chip = FilterChip(filter_id, desc)
        chip.removed.connect(self._on_remove_filter)
        
        # Add to grid (flow-like)
        self.chips_lay.addWidget(chip, self._chip_row, self._chip_col)
        self._chip_col += 1
        if self._chip_col >= self._max_cols:
            self._chip_col = 0
            self._chip_row += 1
        
        self.active_filters[filter_id] = {
            "type": self._current_filter_type,
            "chip": chip,
            "desc": desc,
            "row": self._chip_row if self._chip_col > 0 else self._chip_row - 1,
            "col": (self._chip_col - 1) if self._chip_col > 0 else self._max_cols - 1
        }
        
        # Emit signal
        self.filter_added.emit(self._current_filter_type, filter_id, {"desc": desc})
    
    def _on_remove_filter(self, filter_id):
        """Called when X button on chip is clicked."""
        if filter_id in self.active_filters:
            chip = self.active_filters[filter_id]["chip"]
            self.chips_lay.removeWidget(chip)
            chip.deleteLater()
            del self.active_filters[filter_id]
            self.filter_removed.emit(filter_id)
    
    def _get_filter_description(self) -> str:
        """Get short description based on current filter type and form values."""
        ft = self._current_filter_type
        if ft == "Uzantı":
            return f"Uzantı: .txt"  # TODO: Get from form
        elif ft == "Dosya Adı":
            return f"Ad: 'rapor'"
        elif ft == "Boyut":
            return f"Boyut: >10MB"
        elif ft == "Regex":
            return f"Regex: .*"
        elif ft == "Metin":
            return f"İçerik: 'abc'"
        elif ft == "Metin Yok":
            return f"İçermez: 'xyz'"
        elif ft == "Boş Dosya":
            return f"Boş: 0B"
        elif ft == "Oluşturma Tarihi":
            return f"Oluşturma: ..."
        elif ft == "Değişiklik Tarihi":
            return f"Değişiklik: ..."
        elif ft == "Şifreli":
            return f"Şifreli"
        elif ft == "Gizli":
            return f"Gizli"
        return ft
    
    def _on_reset(self):
        """Reset form to defaults."""
        pass
    
    def _on_cancel(self):
        """Cancel and show default."""
        self._current_filter_type = None
        self.header_lbl.setText("Filtre Ayarları")
        self.stack.setCurrentIndex(self.stack.count() - 1)

# =============================================================================
# FILTERS PANEL
# =============================================================================

class FiltersPanel(QFrame):
    filter_toggled = pyqtSignal(str, bool)
    
    FILTERS = ["Uzantı", "Dosya Adı", "Metin", "Metin Yok", "Boyut", "Regex",
               "Boş Dosya", "Oluşturma Tarihi", "Değişiklik Tarihi",
               "Şifreli", "Gizli"]
    
    TOOLTIPS = {
        "Uzantı": "Dosyaları uzantılarına göre filtreler.",
        "Dosya Adı": "Dosya adında metin arar.",
        "Metin": "Dosya içeriğinde metin arar.",
        "Regex": "Gelişmiş desen eşleştirme.",
        "Metin Yok": "İçeriğinde metin bulunmayan dosyaları bulur.",
        "Boyut": "Dosya boyutuna göre filtreler.",
        "Boş Dosya": "0 byte boyutundaki dosyaları bulur.",
        "Oluşturma Tarihi": "Oluşturulma tarihine göre filtreler.",
        "Değişiklik Tarihi": "Son değişiklik tarihine göre filtreler.",
        "Şifreli": "Şifreli dosyaları bulur.",
        "Gizli": "Gizli dosyaları bulur.",
    }
    
    def __init__(self):
        super().__init__()
        self.setObjectName("FiltersPanel")
        self._build()
    
    def _build(self):
        main_lay = QHBoxLayout(self)
        main_lay.setContentsMargins(8, 8, 0, 8)
        main_lay.setSpacing(0)
        
        # Container for buttons - FIXED WIDTH to prevent resizing issues
        # Button 160px + padding = ~180px
        container = QWidget()
        container.setFixedWidth(180)
        lay = QVBoxLayout(container)
        lay.setContentsMargins(0, 0, 8, 0)
        lay.setSpacing(3)
        
        lbl = QLabel("Filters")
        lbl.setObjectName("SectionHeader")
        lay.addWidget(lbl)
        
        self._btn_group = QButtonGroup(self)
        self._btn_group.setExclusive(False)
        self._btn_group.buttonToggled.connect(self._on_group_toggled)
        
        for f in self.FILTERS:
            b = QPushButton(f)
            b.setObjectName("ListBtn")
            b.setCheckable(True)
            b.setFixedHeight(22)
            b.setToolTip(self.TOOLTIPS.get(f, ""))
            b.toggled.connect(lambda chk, name=f: self.filter_toggled.emit(name, chk))
            lay.addWidget(b)
            self._btn_group.addButton(b)
        
        main_lay.addWidget(container)
        
        # Gradient line immediately after buttons
        main_lay.addWidget(GradientLine())
        
        # Right Side: Settings UI
        self.settings_panel = FilterSettingsPanel()
        main_lay.addWidget(self.settings_panel, 1)

    def _on_group_toggled(self, btn, checked):
        if checked:
            # Show settings UI
            self.settings_panel.show_form(btn.text())

            for b in self._btn_group.buttons():
                if b != btn and b.isChecked():
                    b.setChecked(False)
            
            # Auto uncheck after 1 second
            QTimer.singleShot(1000, lambda: btn.setChecked(False) if btn.isChecked() else None)

# =============================================================================
# ACTION SETTINGS UI (RIGHT SIDE - like FilterSettingsPanel)
# =============================================================================

class ActionSettingsPanel(QWidget):
    action_requested = pyqtSignal(str, dict)  # action_key, settings
    
    def __init__(self):
        super().__init__()
        self.forms = {}
        self._current_action = None
        self._build()

    def _build(self):
        # Dinamik genişlik - minimum tanımlı
        self.setMinimumWidth(250)
        
        lay = QVBoxLayout(self)
        lay.setContentsMargins(12, 8, 12, 8)
        lay.setSpacing(8)
        
        # Header - sabit yükseklik
        self.header_lbl = QLabel("Aksiyon Ayarları")
        self.header_lbl.setFixedHeight(20)
        self.header_lbl.setStyleSheet("font-weight: bold; font-size: 13px; color: #333;")
        lay.addWidget(self.header_lbl)
        
        # Stack - sabit yükseklik
        self.stack = QStackedWidget()
        self.stack.setFixedHeight(140)
        lay.addWidget(self.stack)
        
        # Forms
        self._init_forms()
        
        # Buttons - sabit boyutlar
        btn_lay = QHBoxLayout()
        btn_lay.setContentsMargins(0, 0, 0, 0)
        btn_lay.setSpacing(6)
        
        self.btn_apply = QPushButton("Uygula")
        self.btn_apply.setFixedWidth(70)
        self.btn_apply.setFixedHeight(24)
        self.btn_apply.clicked.connect(self._on_apply)
        
        self.btn_reset = QPushButton("Sıfırla")
        self.btn_reset.setFixedWidth(60)
        self.btn_reset.setFixedHeight(24)
        
        self.btn_cancel = QPushButton("İptal")
        self.btn_cancel.setFixedWidth(50)
        self.btn_cancel.setFixedHeight(24)
        self.btn_cancel.clicked.connect(self._on_cancel)
        
        btn_lay.addWidget(self.btn_apply)
        btn_lay.addWidget(self.btn_reset)
        btn_lay.addWidget(self.btn_cancel)
        btn_lay.addStretch()
        lay.addLayout(btn_lay)
        
        # Separator
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setFixedHeight(2)
        sep.setStyleSheet("background: #ccc;")
        lay.addWidget(sep)
        
        # Active Actions Label
        lbl_active = QLabel("Aktif Aksiyonlar")
        lbl_active.setFixedHeight(18)
        lbl_active.setStyleSheet("font-weight: bold; font-size: 12px;")
        lay.addWidget(lbl_active)
        
        # Chips container - sabit yükseklik
        self.chips_container = QWidget()
        self.chips_container.setFixedHeight(60)
        self.chips_lay = QGridLayout(self.chips_container)
        self.chips_lay.setContentsMargins(0, 0, 0, 0)
        self.chips_lay.setSpacing(4)
        lay.addWidget(self.chips_container)

    def _init_forms(self):
        # Sıralı Adlandırma
        f1 = QWidget()
        l1 = QVBoxLayout(f1)
        l1.setContentsMargins(0,0,0,0)
        l1.setSpacing(4)
        l1.addWidget(QLabel("Desen: (örn: Dosya_{n})"))
        inp1 = QLineEdit()
        l1.addWidget(inp1)
        l1.addWidget(QLabel("Başlangıç:"))
        sp1 = QSpinBox()
        l1.addWidget(sp1)
        l1.addStretch()
        self._add_stack("seq_rename", f1)
        
        # Ön/Son Ek
        f2 = QWidget()
        l2 = QVBoxLayout(f2)
        l2.setContentsMargins(0,0,0,0)
        l2.setSpacing(4)
        l2.addWidget(QLabel("Ön Ek:"))
        inp2a = QLineEdit()
        l2.addWidget(inp2a)
        l2.addWidget(QLabel("Son Ek:"))
        inp2b = QLineEdit()
        l2.addWidget(inp2b)
        l2.addStretch()
        self._add_stack("prefix_suffix", f2)
        
        # Bul/Değiştir
        f3 = QWidget()
        l3 = QVBoxLayout(f3)
        l3.setContentsMargins(0,0,0,0)
        l3.setSpacing(4)
        l3.addWidget(QLabel("Bul:"))
        inp3a = QLineEdit()
        l3.addWidget(inp3a)
        l3.addWidget(QLabel("Değiştir:"))
        inp3b = QLineEdit()
        l3.addWidget(inp3b)
        l3.addStretch()
        self._add_stack("find_replace", f3)
        
        # Uzantı Değiştir
        f4 = QWidget()
        l4 = QVBoxLayout(f4)
        l4.setContentsMargins(0,0,0,0)
        l4.setSpacing(4)
        l4.addWidget(QLabel("Yeni Uzantı:"))
        inp4 = QLineEdit()
        l4.addWidget(inp4)
        l4.addStretch()
        self._add_stack("change_ext", f4)
        
        # Default for others
        for key in ["copy", "tag", "flatten", "secure_del", "merge", "csv", "excel"]:
            f = QWidget()
            l = QVBoxLayout(f)
            l.setContentsMargins(0,0,0,0)
            l.addWidget(QLabel("Bu aksiyon için ayar yok."))
            l.addStretch()
            self._add_stack(key, f)
        
        # Default placeholder
        f_def = QWidget()
        l_def = QVBoxLayout(f_def)
        l_def.setContentsMargins(0,0,0,0)
        l_def.addWidget(QLabel("Soldan bir aksiyon seçiniz."))
        l_def.addStretch()
        self.stack.addWidget(f_def)

    def _add_stack(self, key, widget):
        idx = self.stack.addWidget(widget)
        self.forms[key] = idx

    def show_form(self, action_key, display_name):
        self._current_action = action_key
        self.header_lbl.setText(f"{display_name} Ayarları")
        if action_key in self.forms:
            self.stack.setCurrentIndex(self.forms[action_key])
        else:
            self.stack.setCurrentIndex(self.stack.count()-1)
    
    def _on_apply(self):
        if self._current_action:
            self.action_requested.emit(self._current_action, {})
    
    def _on_cancel(self):
        self._current_action = None
        self.header_lbl.setText("Aksiyon Ayarları")
        self.stack.setCurrentIndex(self.stack.count() - 1)

# =============================================================================
# ACTIONS PANEL
# =============================================================================


class ActionsPanel(QFrame):
    action_clicked = pyqtSignal(str)
    
    ACTIONS = [
        ("Sıralı Adlandırma", "seq_rename"),
        ("Ön/Son Ek", "prefix_suffix"),
        ("Bul/Değiştir", "find_replace"),
        ("Uzantı Değiştir", "change_ext"),
        ("Kopyala", "copy"),
        ("Etiket", "tag"),
        ("Tek Klasör", "flatten"),
        ("Güvenli Sil", "secure_del"),
        ("Metin Birleştir", "merge"),
        ("CSV Rapor", "csv"),
        ("Excel Rapor", "excel"),
    ]
    
    TOOLTIPS = {
        "Sıralı Adlandırma": "Dosyaları sıralı numara ile yeniden adlandırır.",
        "Ön/Son Ek": "Dosya adlarına ön ek veya son ek ekler.",
        "Bul/Değiştir": "Dosya adlarında metin bulur ve değiştirir.",
        "Uzantı Değiştir": "Dosya uzantılarını değiştirir.",
        "Kopyala": "Seçili dosyaları belirtilen konuma kopyalar.",
        "Etiket": "Dosyalara etiket ekler.",
        "Tek Klasör": "Alt klasörlerdeki dosyaları tek klasöre toplar.",
        "Güvenli Sil": "Dosyaları güvenli şekilde kalıcı olarak siler.",
        "Metin Birleştir": "Birden fazla metin dosyasını birleştirir.",
        "CSV Rapor": "Dosya listesini CSV formatında dışa aktarır.",
        "Excel Rapor": "Dosya listesini Excel formatında dışa aktarır.",
    }
    
    def __init__(self):
        super().__init__()
        self.setObjectName("ActionsPanel")
        self._build()
    
    def _build(self):
        main_lay = QHBoxLayout(self)
        main_lay.setContentsMargins(8, 8, 0, 8)
        main_lay.setSpacing(0)
        
        # Container for buttons - FIXED WIDTH
        container = QWidget()
        container.setFixedWidth(180)
        lay = QVBoxLayout(container)
        lay.setContentsMargins(0, 0, 8, 0)
        lay.setSpacing(3)
        
        lbl = QLabel("Actions")
        lbl.setObjectName("SectionHeader")
        lay.addWidget(lbl)
        
        self._btn_group = QButtonGroup(self)
        self._btn_group.setExclusive(False)
        self._btn_group.buttonToggled.connect(self._on_group_toggled)
        
        for display, key in self.ACTIONS:
            b = QPushButton(display)
            b.setObjectName("ListBtn")
            b.setCheckable(True)
            b.setFixedHeight(22)
            b.setToolTip(self.TOOLTIPS.get(display, ""))
            # Note: We rely on clicked to trigger action, but check state handles visual
            b.clicked.connect(lambda _, k=key: self.action_clicked.emit(k))
            lay.addWidget(b)
            self._btn_group.addButton(b)
        
        main_lay.addWidget(container)
        
        # Gradient line
        main_lay.addWidget(GradientLine())
        
        # Right Side: Settings UI (left aligned)
        self.settings_panel = ActionSettingsPanel()
        main_lay.addWidget(self.settings_panel)
        
        # Push everything to left
        main_lay.addStretch(1)
        
    def _on_group_toggled(self, btn, checked):
        if checked:
            # Find the action key for this button
            action_key = None
            for display, key in self.ACTIONS:
                if display == btn.text():
                    action_key = key
                    break
            
            if action_key:
                self.settings_panel.show_form(action_key, btn.text())
            
            for b in self._btn_group.buttons():
                if b != btn and b.isChecked():
                    b.setChecked(False)
            
            # Auto uncheck after 1 second
            QTimer.singleShot(1000, lambda: btn.setChecked(False) if btn.isChecked() else None)

    def reset_selection(self):
        """Uncheck any selected action button."""
        # Just uncheck all, since setExclusive is False it's safe
        for b in self._btn_group.buttons():
            b.setChecked(False)


# =============================================================================
# PREVIEW PANEL
# =============================================================================

class PreviewPanel(QFrame):
    exec_action = pyqtSignal(str, dict)
    
    ACTION_NAMES = {
        "seq_rename": "Sıralı Adlandırma",
        "prefix_suffix": "Ön/Son Ek",
        "find_replace": "Bul/Değiştir",
        "change_ext": "Uzantı Değiştir",
        "copy": "Kopyala",
        "tag": "Etiket",
        "flatten": "Tek Klasör",
        "secure_del": "Güvenli Sil",
        "merge": "Metin Birleştir",
        "csv": "CSV Rapor",
        "excel": "Excel Rapor",
    }
    
    def __init__(self):
        super().__init__()
        self.setObjectName("PreviewPanel")
        self._mode = "preview"
        self._action_pages = {}
        self._build()
    
    def _build(self):
        lay = QVBoxLayout(self)
        lay.setContentsMargins(8, 8, 8, 8)
        lay.setSpacing(5)
        
        self._title = QLabel("File Preview")
        self._title.setObjectName("SectionHeader")
        lay.addWidget(self._title)
        
        # Header line removed

        
        self._stack = QStackedWidget()
        
        self._preview_page = self._make_preview()
        self._stack.addWidget(self._preview_page)
        
        for key, name in self.ACTION_NAMES.items():
            page = self._make_action(key, name)
            self._action_pages[key] = page
            self._stack.addWidget(page)
        
        lay.addWidget(self._stack, 1)
    
    def _make_preview(self):
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(5)
        
        self._placeholder = QLabel("Select a file")
        self._placeholder.setObjectName("PlaceholderLabel")
        self._placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.addWidget(self._placeholder, 1)
        
        self._info = QWidget()
        self._info.hide()
        ilayout = QVBoxLayout(self._info)
        ilayout.setContentsMargins(0, 0, 0, 0)
        ilayout.setSpacing(5)
        
        self._icon = QLabel()
        self._icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ilayout.addWidget(self._icon)
        
        form = QFormLayout()
        form.setSpacing(3)
        self._f_name = QLabel("-")
        self._f_name.setWordWrap(True)
        self._f_type = QLabel("-")
        self._f_size = QLabel("-")
        self._f_modified = QLabel("-")
        self._f_path = QLabel("-")
        self._f_path.setWordWrap(True)
        self._f_path.setObjectName("PathLabel")
        form.addRow("<b>Name:</b>", self._f_name)
        form.addRow("<b>Type:</b>", self._f_type)
        form.addRow("<b>Size:</b>", self._f_size)
        form.addRow("<b>Mod:</b>", self._f_modified)
        form.addRow("<b>Path:</b>", self._f_path)
        ilayout.addLayout(form)
        
        self._text = QTextEdit()
        self._text.setReadOnly(True)
        self._text.setMaximumHeight(60)
        self._text.hide()
        ilayout.addWidget(self._text)
        
        ilayout.addStretch()
        lay.addWidget(self._info)
        return w
    
    def _make_action(self, key, name):
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(5)
        
        form = QFormLayout()
        form.setSpacing(4)
        
        if key == "seq_rename":
            w._pattern = QLineEdit()
            w._pattern.setPlaceholderText("File_{n}")
            form.addRow("Pattern:", w._pattern)
            w._start = QSpinBox()
            w._start.setRange(0, 99999)
            w._start.setValue(1)
            form.addRow("Start:", w._start)
        elif key == "prefix_suffix":
            w._prefix = QLineEdit()
            form.addRow("Prefix:", w._prefix)
            w._suffix = QLineEdit()
            form.addRow("Suffix:", w._suffix)
        elif key == "find_replace":
            w._find = QLineEdit()
            form.addRow("Find:", w._find)
            w._repl = QLineEdit()
            form.addRow("Replace:", w._repl)
        elif key == "change_ext":
            w._from = QLineEdit()
            form.addRow("From:", w._from)
            w._to = QLineEdit()
            form.addRow("To:", w._to)
        elif key == "secure_del":
            note = QLabel("⚠️ Delete!")
            form.addRow(note)
            w._passes = QSpinBox()
            w._passes.setRange(1, 10)
            w._passes.setValue(3)
            form.addRow("Passes:", w._passes)
        else:
            note = QLabel(f"'{name}'")
            note.setObjectName("PlaceholderLabel")
            form.addRow(note)
        
        lay.addLayout(form)
        lay.addStretch()
        
        btns = QHBoxLayout()
        cancel = QPushButton("X")
        cancel.setFixedWidth(30)
        cancel.clicked.connect(self.show_preview)
        btns.addWidget(cancel)
        btns.addStretch()
        exe = QPushButton("Run")
        exe.setFixedWidth(40)
        exe.clicked.connect(lambda: self.exec_action.emit(key, {}))
        btns.addWidget(exe)
        lay.addLayout(btns)
        
        return w
    
    def show_preview(self):
        self._mode = "preview"
        self._title.setText("File Preview")
        self._stack.setCurrentIndex(0)
    
    def show_action(self, key):
        if key in self._action_pages:
            self._mode = "action"
            self._title.setText(self.ACTION_NAMES.get(key, key))
            self._stack.setCurrentWidget(self._action_pages[key])
    
    def update_file_preview(self, path: str):
        if self._mode != "preview":
            self.show_preview()
        
        try:
            p = Path(path)
            if not p.exists():
                self._show_placeholder("Not found")
                return
            
            self._placeholder.hide()
            self._info.show()
            self._f_name.setText(p.name)
            
            if p.is_dir():
                # Folders: show placeholder, not details
                self._show_placeholder("Dosya seçiniz")
                return
            else:
                ext = p.suffix.upper()[1:] if p.suffix else "FILE"
                self._f_type.setText(ext)
                try:
                    stat = p.stat()
                    size = stat.st_size
                    for unit in ['B', 'KB', 'MB', 'GB']:
                        if size < 1024:
                            self._f_size.setText(f"{size:.1f} {unit}")
                            break
                        size /= 1024
                    mtime = datetime.fromtimestamp(stat.st_mtime)
                    self._f_modified.setText(mtime.strftime("%m-%d %H:%M"))
                except:
                    self._f_size.setText("—")
                    self._f_modified.setText("—")
                
                self._icon.setPixmap(QIcon("icons/file-lines-solid.svg").pixmap(28, 28))
                
                text_exts = ['.txt', '.py', '.md', '.json', '.xml', '.html', '.css', '.js']
                if p.suffix.lower() in text_exts:
                    try:
                        self._text.setText(p.read_text(encoding='utf-8', errors='ignore')[:500])
                        self._text.show()
                    except:
                        self._text.hide()
                else:
                    self._text.hide()
            
            self._f_path.setText(str(p))
        except Exception as e:
            self._show_placeholder(f"Error")
    
    def _show_placeholder(self, text: str):
        self._info.hide()
        self._placeholder.setText(text)
        self._placeholder.show()


# =============================================================================
# MAIN WINDOW - RESPONSIVE LAYOUT
# =============================================================================
# Stretch ratios:
#   Source: 1 (min 200px)
#   Filters: 2 (min 320px) 
#   Preview: 1 (min 200px)
#   Actions: spans Filters + Preview
# =============================================================================

class MainWindow(QMainWindow):
    # Minimum widths for panels
    SOURCE_MIN = 200
    FILTERS_MIN = 320
    PREVIEW_MIN = 200
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File-Architect-Pro")
        self.resize(1000, 700)  # Larger default window
        self.setMinimumSize(800, 500)  # Minimum size
        self._build()
        self._connect()
    
    def _build(self):
        central = QWidget()
        self.setCentralWidget(central)
        
        outer = QVBoxLayout(central)
        outer.setContentsMargins(12, 12, 12, 12)
        outer.setSpacing(0)
        
        # Grid layout with stretch factors
        grid = QGridLayout()
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setHorizontalSpacing(10)
        grid.setVerticalSpacing(10)
        
        # Source: Column 0, Row 0-1 (spans 2 rows)
        self._source = SourcePanel()
        self._source.setMinimumWidth(self.SOURCE_MIN)
        grid.addWidget(self._source, 0, 0, 2, 1)
        
        # Filters: Column 1, Row 0
        self._filters = FiltersPanel()
        self._filters.setMinimumWidth(self.FILTERS_MIN)
        grid.addWidget(self._filters, 0, 1)
        
        # Preview: Column 2, Row 0
        self._preview = PreviewPanel()
        self._preview.setMinimumWidth(self.PREVIEW_MIN)
        grid.addWidget(self._preview, 0, 2)
        
        # Actions: Column 1-2, Row 1 (spans 2 columns)
        self._actions = ActionsPanel()
        grid.addWidget(self._actions, 1, 1, 1, 2)
        
        # Column stretch factors (proportional widths)
        # Source : Filters : Preview = 1 : 2 : 1
        grid.setColumnStretch(0, 1)  # Source
        grid.setColumnStretch(1, 2)  # Filters (wider)
        grid.setColumnStretch(2, 1)  # Preview (same as Source)
        
        # Row stretch factors
        grid.setRowStretch(0, 3)   # Filters row (daha az)
        grid.setRowStretch(1, 9)   # Actions row (daha fazla)
        
        outer.addLayout(grid)
    
    def _connect(self):
        self._source.selection_changed.connect(self._preview.update_file_preview)
        self._source.delete_requested.connect(self._on_del)
        self._actions.action_clicked.connect(self._on_action)
        self._preview.exec_action.connect(self._on_exec)
    
    def _on_del(self, p):
        import shutil
        path = Path(p)
        if not path.exists():
            return
        
        # Confirmation dialog
        if path.is_dir():
            msg = f"Klasör ve içindeki tüm dosyalar silinecek:\n{p}\n\nDevam etmek istiyor musunuz?"
        else:
            msg = f"Dosya silinecek:\n{p}\n\nDevam etmek istiyor musunuz?"
        
        reply = QMessageBox.question(
            self, "Silme Onayı", msg,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                if path.is_dir():
                    shutil.rmtree(path)
                else:
                    path.unlink()
                # Refresh tree
                self._source._model.setRootPath(self._source._model.rootPath())
            except Exception as e:
                QMessageBox.warning(self, "Hata", f"Silinemedi:\n{e}")
    
    def _on_action(self, key):
        # Actions now handled in ActionsPanel's settings_panel
        pass
    
    def _on_exec(self, key, settings):
        print(f"Execute: {key}")


# =============================================================================
# ENTRY
# =============================================================================

def main():
    app = QApplication(sys.argv)
    
    # Use Fusion style to avoid system-specific blue highlights
    app.setStyle("Fusion")
    
    # Force palette to remove all blue
    pal = app.palette()
    pal.setColor(QPalette.ColorRole.Highlight, QColor("#D7D6D2"))
    pal.setColor(QPalette.ColorRole.HighlightedText, QColor("#444444"))
    pal.setColor(QPalette.ColorRole.Base, QColor("#F9F8F2"))
    app.setPalette(pal)
    
    app.setStyleSheet(STYLE_SHEET)
    
    win = MainWindow()
    win.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
