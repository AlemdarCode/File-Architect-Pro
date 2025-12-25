"""
File-Architect-Pro - Responsive Layout
Düzeltme: 
1. Aksiyon Ayarları (Alt Panel) artık tam genişliğe yayılıyor ve dinamik büyüyor.
2. Filtre etiketlerindeki (Chip) silme butonu kırmızı oval tasarım (X) ile değiştirildi.
"""

import sys
from pathlib import Path
from datetime import datetime
from PyQt6.QtCore import (
    Qt, pyqtSignal, QModelIndex, QDir, QSize, QTimer, 
    QRect, QEvent, QFileInfo, QItemSelection, QDate,
    QRegularExpression, QSortFilterProxyModel
)
from PyQt6.QtGui import (
    QIcon, QPainter, QAbstractFileIconProvider, 
    QFileSystemModel, QColor, QPen, QPalette,
    QLinearGradient, QBrush, QRegularExpressionValidator,
    QIntValidator, QPixmap
)
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTreeView, QLabel, QPushButton, QFrame, QFileDialog,
    QStyledItemDelegate, QStyleOptionViewItem, QStyle,
    QSizePolicy, QStackedWidget, QTextEdit,
    QLineEdit, QSpinBox, QDoubleSpinBox, QFormLayout, QMessageBox, QGridLayout,
    QButtonGroup, QCheckBox, QComboBox, QDateEdit, QScrollArea, QProgressBar,
    QTabWidget, QTabBar
)
from proxymodel import PreviewProxyModel
from workers import FastScannerThread, ActionRunnerThread


# =============================================================================
# GLOBAL TRANSLATION SYSTEM
# =============================================================================

_current_language = "tr"
_translations_cache = {}

def _init_global_translations():
    """Global çeviri sözlüğünü başlat"""
    global _translations_cache, _current_language
    
    if _current_language == "tr":
        _translations_cache = {
            # QMessageBox Başlıkları
            "msg_title_info": "Bilgi",
            "msg_title_warning": "Uyarı",
            "msg_title_error": "Hata",
            "msg_title_success": "Başarılı",
            "msg_title_confirm": "Onay",
            "msg_title_hide": "Gizle",
            "msg_title_delete_confirm": "Silme Onayı",
            "msg_title_security_warning": "Güvenlik Uyarısı",
            "msg_title_operation_forbidden": "İşlem Yasaklandı",
            "msg_title_invalid_extension": "Hatalı Uzantı",
            "msg_title_completed_with_errors": "İşlem Tamamlandı (Hatalı)",
            
            # QMessageBox Mesajları
            "msg_settings_applied": "Ayarlar başarıyla uygulandı!",
            "msg_select_filter_first": "Lütfen önce soldan bir filtre tipi seçiniz!",
            "msg_max_filters": "En fazla {0} filtre ekleyebilirsiniz!",
            "msg_filter_exists": "Bu filtre zaten eklenmiş!\n\n{0}",
            "msg_extension_empty": "Uzantı boş olamaz!",
            "msg_no_valid_extension": "Geçerli uzantı bulunamadı!",
            "msg_invalid_regex": "Geçersiz regex deseni!",
            "msg_pattern_empty": "Desen boş olamaz!",
            "msg_search_text_empty": "Aranacak metin boş olamaz!",
            "msg_target_folder_empty": "Hedef klasör seçilmedi!",
            "msg_output_path_empty": "Çıktı yolu giriniz!",
            "msg_max_actions": "En fazla 3 aksiyon eklenebilir!",
            "msg_no_files_to_process": "İşlem yapılacak dosya bulunamadı!",
            "msg_no_files": "İşlenecek dosya yok!",
            "msg_all_operations_success": "Tüm işlemler başarıyla tamamlandı.",
            "msg_some_operations_failed": "Bazı işlemler başarısız oldu:\n{0}",
            "msg_and_more_errors": "\n... ve {0} hata daha.",
            "msg_file_in_use": "Dosya kullanımda veya izin yok:\n{0}",
            "msg_delete_failed": "Silinemedi:\n{0}",
            "msg_security_delete_disabled": "Sol panelden doğrudan silme işlemi, veri kaybını önlemek için devre dışı bırakılmıştır.\nDosyaları silmek için lütfen Aksiyonlar sekmesini veya Dosya Gezgini'ni kullanın.",
            "msg_delete_folder_confirm": "Klasör ve içindeki tüm dosyalar silinecek:\n{0}\n\nDevam etmek istiyor musunuz?",
            "msg_delete_file_confirm": "Dosya silinecek:\n{0}\n\nDevam etmek istiyor musunuz?",
            "msg_root_drive_forbidden": "Kritik Hata: Kök sürücüler (C:\\, D:\\ vb.) üzerinde hiçbir silme veya gizleme işlemi yapılamaz!\n\nBu işlem sistem güvenliği için kalıcı olarak engellenmiştir.",
            "msg_hide_item_confirm": "Bu öğeyi listeden gizlemek istiyor musunuz?\n(Dosya diskten silinmeyecek, sadece bu görünümden kalkacak)\n\n{0}",
            "msg_processing": "İşleniyor...",
            
            # Validasyon Mesajları
            "msg_invalid_empty_extension": "'{0}' geçersiz (boş uzantı)",
            "msg_invalid_double_dot": "'{0}' geçersiz (çift nokta)",
            "msg_invalid_char": "'{0}' geçersiz karakter içeriyor: '{1}'"
        }
    else:  # English
        _translations_cache = {
            # QMessageBox Titles
            "msg_title_info": "Information",
            "msg_title_warning": "Warning",
            "msg_title_error": "Error",
            "msg_title_success": "Success",
            "msg_title_confirm": "Confirm",
            "msg_title_hide": "Hide",
            "msg_title_delete_confirm": "Delete Confirmation",
            "msg_title_security_warning": "Security Warning",
            "msg_title_operation_forbidden": "Operation Forbidden",
            "msg_title_invalid_extension": "Invalid Extension",
            "msg_title_completed_with_errors": "Completed with Errors",
            
            # QMessageBox Messages
            "msg_settings_applied": "Settings applied successfully!",
            "msg_select_filter_first": "Please select a filter type from the left first!",
            "msg_max_filters": "You can add up to {0} filters!",
            "msg_filter_exists": "This filter already exists!\n\n{0}",
            "msg_extension_empty": "Extension cannot be empty!",
            "msg_no_valid_extension": "No valid extension found!",
            "msg_invalid_regex": "Invalid regex pattern!",
            "msg_pattern_empty": "Pattern cannot be empty!",
            "msg_search_text_empty": "Search text cannot be empty!",
            "msg_target_folder_empty": "Target folder not selected!",
            "msg_output_path_empty": "Please enter an output path!",
            "msg_max_actions": "Maximum 3 actions can be added!",
            "msg_no_files_to_process": "No files found to process!",
            "msg_no_files": "No files to process!",
            "msg_all_operations_success": "All operations completed successfully.",
            "msg_some_operations_failed": "Some operations failed:\n{0}",
            "msg_and_more_errors": "\n... and {0} more errors.",
            "msg_file_in_use": "File is in use or permission denied:\n{0}",
            "msg_delete_failed": "Could not delete:\n{0}",
            "msg_security_delete_disabled": "Direct deletion from the left panel is disabled to prevent data loss.\nTo delete files, please use the Actions tab or File Explorer.",
            "msg_delete_folder_confirm": "The folder and all its contents will be deleted:\n{0}\n\nDo you want to continue?",
            "msg_delete_file_confirm": "The file will be deleted:\n{0}\n\nDo you want to continue?",
            "msg_root_drive_forbidden": "Critical Error: No delete or hide operations can be performed on root drives (C:\\, D:\\ etc.)!\n\nThis operation is permanently blocked for system security.",
            "msg_hide_item_confirm": "Do you want to hide this item from the list?\n(The file won't be deleted from disk, only hidden from this view)\n\n{0}",
            "msg_processing": "Processing...",
            
            # Validation Messages
            "msg_invalid_empty_extension": "'{0}' is invalid (empty extension)",
            "msg_invalid_double_dot": "'{0}' is invalid (double dot)",
            "msg_invalid_char": "'{0}' contains invalid character: '{1}'"
        }

def set_language(lang_code):
    """Dil ayarını güncelle"""
    global _current_language
    _current_language = lang_code
    _init_global_translations()

def tr(key, *args):
    """Global çeviri fonksiyonu"""
    text = _translations_cache.get(key, key)
    if args:
        for i, arg in enumerate(args):
            text = text.replace("{" + str(i) + "}", str(arg))
    return text

# Başlangıç çevirilerini yükle
_init_global_translations()


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

QTreeView {
    show-decoration-selected: 0;
    outline: none;
    border: none;
}

QTreeView::branch {
    background: transparent;
    border: none;
    outline: none;
}

QTreeView::item {
    border: none;
    outline: none;
}

QTreeView::branch:has-siblings:!adjoins-item {
    border-image: url(icons/vline.svg) 0;
}

QTreeView::branch:has-siblings:adjoins-item {
    border-image: url(icons/branch-more.svg) 0;
}

QTreeView::branch:!has-children:!has-siblings:adjoins-item {
    border-image: url(icons/branch-end.svg) 0;
}

QTreeView::branch:has-children:!has-siblings:closed,
QTreeView::branch:closed:has-children:has-siblings {
    border-image: url(icons/branch-more.svg) 0;
}

QTreeView::branch:open:has-children:!has-siblings,
QTreeView::branch:open:has-children:has-siblings {
    border-image: url(icons/branch-more.svg) 0;
}

/* Klasör olmayan ve kardeşi olan (Aradaki dosya) için kesin kural */
QTreeView::branch:!has-children:has-siblings:adjoins-item {
    border-image: url(icons/branch-more.svg) 0;
}

QTreeView::branch:open:has-children:!has-siblings,
QTreeView::branch:open:has-children:has-siblings {
    border-image: url(icons/branch-more.svg) 0;
}


QPushButton {
    background-color: #D7D6D2;
    color: #444444;
    border: 1px solid #C8C8C4;
    border-radius: 3px;
    padding: 1px 8px;
    min-height: 20px;
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

QLineEdit, QComboBox, QDateEdit {
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

/* ============================================================================
   MODERN SPINBOX TASARIMI
   ============================================================================ */

QFrame#ModernSpinBox {
    background-color: #FFFFFF;
    border: 1px solid #D7D6D2;
    border-radius: 4px;
    padding: 0px;
}

QLineEdit#SpinInput {
    border: none;
    background: transparent;
    color: #333;
    font-size: 12px;
    font-weight: normal; 
    padding-left: 8px;   
    margin: 0px;
}

QPushButton#SpinBtnUp, QPushButton#SpinBtnDown {
    border: none;
    background-color: #F5F5F5;
    color: #555;
    font-size: 12px;
    font-weight: bold;
    font-family: Arial; 
    margin: 0px;
    padding: 0px;
    padding-bottom: 2px;
    text-align: center;
    border-left: 1px solid #D7D6D2;
}

QPushButton#SpinBtnUp {
    border-top-right-radius: 4px;
    border-bottom: 1px solid #D7D6D2;
}

QPushButton#SpinBtnDown {
    border-bottom-right-radius: 4px;
    border-top: none; 
}

QPushButton#SpinBtnUp:hover, QPushButton#SpinBtnDown:hover {
    background-color: #E0E0E0;
    color: #000;
}

QPushButton#SpinBtnUp:pressed, QPushButton#SpinBtnDown:pressed {
    background-color: #CCCCCC;
}

/* ============================================================================
   DİĞER BİLEŞENLER
   ============================================================================ */

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

QComboBox QAbstractItemView {
    background-color: #FFFFFF;
    color: #333333;
    border: 1px solid #CCCCCC;
    selection-background-color: #E8E8E8;
    selection-color: #333333;
}

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

QMessageBox {
    background-color: #F9F8F2;
}
QMessageBox QLabel {
    color: #333333;
}
QMessageBox QPushButton {
    min-width: 80px;
}

/* ============================================================================
   CHECKBOX TASARIMI
   ============================================================================ */

QCheckBox {
    spacing: 6px;
    color: #333333;
}

QCheckBox::indicator {
    width: 14px;
    height: 14px;
    border: 2px solid #999999;
    border-radius: 2px;
    background-color: #FFFFFF;
}

QCheckBox::indicator:hover {
    border-color: #666666;
}

QCheckBox::indicator:checked {
    background-color: #FFFFFF;
    border-color: #555555;
    image: url(icons/check-solid.svg);
}

QCheckBox::indicator:checked:hover {
    border-color: #444444;
}

/* ============================================================================
   PROGRESS BAR & TASK ITEM
   ============================================================================ */

QProgressBar {
    border: 1px solid #D7D6D2;
    border-radius: 2px;
    background-color: #FFFFFF;
    text-align: center;
    height: 18px;
}

QProgressBar::chunk {
    background-color: #3B82F6;
    width: 2px;
}

QFrame#TaskItem {
    background-color: #D7D6D2;
    border-radius: 4px;
    border: 1px solid #C8C8C4;
}

QFrame#TaskItem:hover {
    background-color: #C8C8C4;
}
"""


# =============================================================================
# GRADIENT LINE WIDGET
# =============================================================================

class GradientLine(QWidget):
    def __init__(self, color="#D8D7D3", width=2):
        super().__init__()
        self._color = QColor(color)
        self._width = width
        self.setFixedWidth(width + 4)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        h = self.height()
        w = self.width()
        x = w // 2
        # Daha kısa çizgi (Margin ekle)
        margin = h * 0.15 # %15 üstten/alttan boşluk
        
        gradient = QLinearGradient(0, margin, 0, h - margin)
        color_transparent = QColor(self._color)
        color_transparent.setAlpha(0)
        gradient.setColorAt(0.0, color_transparent)
        gradient.setColorAt(0.2, self._color) # Daha yumuşak geçiş
        gradient.setColorAt(0.8, self._color)
        gradient.setColorAt(1.0, color_transparent)
        
        pen = QPen(QBrush(gradient), self._width)
        painter.setPen(pen)
        painter.drawLine(x, int(margin), x, int(h - margin))


# =============================================================================
# CUSTOM WIDGETS (MODERN SPINBOX)
# =============================================================================

class ModernSpinBox(QFrame):
    valueChanged = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("ModernSpinBox")
        self._value = 0
        self._min = 0
        self._max = 999999
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        self.input = QLineEdit()
        self.input.setText("0")
        self.input.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.input.setObjectName("SpinInput")
        # Sadece sayı girişi için validator
        self.input.setValidator(QIntValidator(self._min, self._max))
        self.input.editingFinished.connect(self._on_editing_finished)
        layout.addWidget(self.input, 1)
        
        btn_container = QWidget()
        btn_container.setFixedWidth(15) 
        vlayout = QVBoxLayout(btn_container)
        vlayout.setContentsMargins(0, 0, 0, 0)
        vlayout.setSpacing(0)
        
        self.btn_up = QPushButton("+")
        self.btn_up.setObjectName("SpinBtnUp")
        self.btn_up.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_up.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        self.btn_up.clicked.connect(self.stepUp)
        vlayout.addWidget(self.btn_up)
        
        self.btn_down = QPushButton("-")
        self.btn_down.setObjectName("SpinBtnDown")
        self.btn_down.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_down.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        self.btn_down.clicked.connect(self.stepDown)
        vlayout.addWidget(self.btn_down)
        
        layout.addWidget(btn_container)
        self.setFixedHeight(28)

    def value(self):
        try:
            return int(self.input.text())
        except:
            return 0

    def setValue(self, val):
        val = max(self._min, min(self._max, val))
        self._value = val
        self.input.setText(str(val))
        self.valueChanged.emit(val)

    def setRange(self, min_val, max_val):
        self._min = min_val
        self._max = max_val

    def stepUp(self):
        self.setValue(self.value() + 1)

    def stepDown(self):
        self.setValue(self.value() - 1)
        
    def _on_editing_finished(self):
        self.setValue(self.value())


# =============================================================================
# ICON PROVIDER
# =============================================================================

class IconProvider(QAbstractFileIconProvider):
    def __init__(self):
        super().__init__()
        self._color = QColor("#444444") # Default
        self._cache = {}
        self._load_icons()
        
    def set_color(self, color):
        self._color = QColor(color)
        self._cache.clear()
        self._load_icons()

    def _load_icons(self):
        self._folder = self._colorize("icons/folder-open-solid.svg")
        self._file = self._colorize("icons/file-lines-solid.svg")
        self._image = self._colorize("icons/image-solid.svg")
        self._music = self._colorize("icons/music-solid.svg")
        
        # Extensions Set (Hızlı Lookup)
        self._img_exts = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'svg', 'webp'}
        self._av_exts = {'mp3', 'wav', 'flac', 'm4a', 'ogg', 'mp4', 'avi', 'mkv', 'mov'}
        
    @staticmethod
    def make_icon(path, color="#444444"):
        """Verilen path ve renkte QIcon oluşturur (Güvenli Mod)"""
        try:
            # Geçici çözüm: Boyama yapmadan direkt ikonu döndür (Çökme testi)
            if not Path(path).exists(): return QIcon()
            return QIcon(path)
        except Exception as e:
            print(f"make_icon error: {e}")
            return QIcon()

    def _colorize(self, path):
        if not Path(path).exists(): return QIcon()
        pix = QPixmap(path)
        if pix.isNull(): return QIcon()
        
        # Create a new pixmap with the target color
        colored = QPixmap(pix.size())
        colored.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(colored)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.drawPixmap(0, 0, pix)
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
        painter.fillRect(colored.rect(), self._color)
        painter.end()
        
        return QIcon(colored)

    def icon(self, info) -> QIcon:
        if isinstance(info, QAbstractFileIconProvider.IconType):
            return self._folder if info == QAbstractFileIconProvider.IconType.Folder else self._file
            
        if isinstance(info, QFileInfo):
            if info.isDir():
                return self._folder
                
            # Hızlı Cache Lookup
            ext = info.suffix().lower()
            if not ext: return self._file # Uzantısız dosyalar
            
            if ext in self._cache:
                return self._cache[ext]
            
            icon = self._file
            if ext in self._img_exts:
                icon = self._image
            elif ext in self._av_exts:
                icon = self._music
            
            self._cache[ext] = icon
            return icon
            
        return self._file

    def get_icon(self, path):
        """Harici kullanım için ikon boyama ve döndürme"""
        return self._colorize(path)

class TreeDelegate(QStyledItemDelegate):
    delete_clicked = pyqtSignal(QModelIndex)
    ROW_HEIGHT = 26
    
    def __init__(self, tree_view, model):
        super().__init__(tree_view)
        self._tree = tree_view
        self._model = model
        self.set_color("#444444") # Initial color

    def set_color(self, color):
        # Renk bilgisini sakla
        self._current_color = color
        self._xicon = self._colorize("icons/xmark-solid.svg", color)
        if self._xicon.isNull():
             self._xicon = QIcon.fromTheme("edit-delete")
             
    def _colorize(self, path, color):
        if not Path(path).exists(): return QIcon()
        pix = QPixmap(path)
        if pix.isNull(): return QIcon()
        colored = QPixmap(pix.size())
        colored.fill(Qt.GlobalColor.transparent)
        painter = QPainter(colored)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        painter.drawPixmap(0, 0, pix)
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
        painter.fillRect(colored.rect(), QColor(color))
        painter.end()
        return QIcon(colored)
    
    def paint(self, painter, option, index):
        painter.save()
        
        # İçerik alanı (sağdaki silme butonu için yer aç)
        content_rect = QRect(option.rect)
        content_rect.setRight(content_rect.right() - 20)
        
        opt = QStyleOptionViewItem(option)
        opt.rect = content_rect
        super().paint(painter, opt, index)
        
        # Silme butonu çizimi
        xr = self._x_icon_rect(option.rect)
        # Mouse üzerindeyse tam opak, değilse daha belirgin (%70)
        opacity = 1.0 if (option.state & QStyle.StateFlag.State_MouseOver) else 0.7
        painter.setOpacity(opacity)
        self._xicon.paint(painter, xr)
        painter.restore()
    
    def _x_rect(self, rect: QRect) -> QRect:
        sz = 20
        # Dikey ortalama için ROW_HEIGHT/2 yerine rect merkezi kullan
        return QRect(rect.right() - sz - 2, rect.center().y() - sz // 2, sz, sz)
    
    def _x_icon_rect(self, rect: QRect) -> QRect:
        sz = 11
        return QRect(rect.right() - sz - 6, rect.center().y() - sz // 2, sz, sz)
    
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
# SETTINGS TAB WIDGET
# =============================================================================

class AppSettingsWidget(QWidget):
    theme_changed = pyqtSignal(str)
    language_changed = pyqtSignal(str) # tr, en
    
    def __init__(self):
        super().__init__()
        self._build()
        
    def _build(self):
        lay = QVBoxLayout(self)
        lay.setContentsMargins(16, 20, 16, 20)
        lay.setSpacing(20)
        lay.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # Başlık
        self.header_lbl = QLabel("Uygulama Ayarları")
        self.header_lbl.setStyleSheet("font-size: 16px; font-weight: bold; color: #333;")
        lay.addWidget(self.header_lbl)
        
        # Tema Seçimi
        grp_theme = QWidget()
        l_theme = QVBoxLayout(grp_theme)
        l_theme.setContentsMargins(0, 0, 0, 0)
        l_theme.setSpacing(8)
        
        self.lbl_theme = QLabel("Görünüm Teması:")
        l_theme.addWidget(self.lbl_theme)
        self.combo_theme = QComboBox()
        self.combo_theme.addItems(["Açık (Light)", "Koyu (Dark)", "Sistem"])
        # self.combo_theme.currentTextChanged.connect(self.theme_changed.emit) # Manuel uygula
        l_theme.addWidget(self.combo_theme)
        lay.addWidget(grp_theme)
        
        # Dil Seçimi
        grp_lang = QWidget()
        l_lang = QVBoxLayout(grp_lang)
        l_lang.setContentsMargins(0, 0, 0, 0)
        l_lang.setSpacing(8)
        
        self.lbl_lang = QLabel("Dil (Language):")
        l_lang.addWidget(self.lbl_lang)
        self.combo_lang = QComboBox()
        self.combo_lang.addItems(["Türkçe", "English"])
        l_lang.addWidget(self.combo_lang)
        lay.addWidget(grp_lang)
        
        # Separator
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("background-color: #D7D6D2;")
        lay.addWidget(sep)
        
        # Uygula Butonu
        self.btn_apply = QPushButton("Ayarları Uygula")
        self.btn_apply.setFixedHeight(30)
        self.btn_apply.setStyleSheet("""
            QPushButton {
                background-color: #3B82F6;
                color: white;
                font-weight: bold;
                border-radius: 4px;
            }
            QPushButton:hover { background-color: #2563EB; }
            QPushButton:pressed { background-color: #1D4ED8; }
        """)
        self.btn_apply.clicked.connect(self._on_apply)
        lay.addWidget(self.btn_apply)
        
        # Hakkında
        lbl_about = QLabel("File-Architect-Pro\nv1.0.0")
        lbl_about.setStyleSheet("color: #666; font-size: 11px;")
        lbl_about.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.addWidget(lbl_about)
        
        lay.addStretch()

    def _on_apply(self):
        # Temayı uygula
        theme_text = self.combo_theme.currentText()
        if "Açık" in theme_text:
            self.theme_changed.emit("light")
        elif "Koyu" in theme_text:
            self.theme_changed.emit("dark")
        elif "Sistem" in theme_text:
            self.theme_changed.emit("system")
            
        # Dil ayarı
        lang_text = self.combo_lang.currentText()
        if "English" in lang_text:
            self.language_changed.emit("en")
        else:
            self.language_changed.emit("tr")
        
        QMessageBox.information(self, tr("msg_title_info"), tr("msg_settings_applied"))

    def update_texts(self, t):
        if "app_settings" in t: self.header_lbl.setText(t["app_settings"])
        if "theme_label" in t: self.lbl_theme.setText(t["theme_label"])
        if "lang_label" in t: self.lbl_lang.setText(t["lang_label"])
        if "apply_settings" in t: self.btn_apply.setText(t["apply_settings"])
        
        # ComboBox items
        if "theme_items" in t:
            current = self.combo_theme.currentIndex()
            self.combo_theme.clear()
            self.combo_theme.addItems(t["theme_items"])
            self.combo_theme.setCurrentIndex(current)



# =============================================================================
# SOURCE PANEL (TABBED)
# =============================================================================

class SourceProxyModel(QSortFilterProxyModel):
    def __init__(self, hidden_files):
        super().__init__()
        self.hidden_files = hidden_files # Reference to set
        
    def filterAcceptsRow(self, source_row, source_parent):
        source_model = self.sourceModel()
        if not source_model: return True
        index = source_model.index(source_row, 0, source_parent)
        path = source_model.filePath(index)
        
        # Windows path normalization to match hidden set
        import os
        try:
            norm = os.path.normpath(path)
            if norm in self.hidden_files:
                return False
        except: pass
            
        return True

class SourcePanel(QFrame):
    file_selected = pyqtSignal(str)
    dir_selected = pyqtSignal(str)
    delete_requested = pyqtSignal(str)
    selection_changed = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.setObjectName("SourcePanel")
        self._root = None
        self._hidden_files = set() # Gizlenen dosyalar (Sanal silme)
        self._build()
    
    def _build(self):
        # Ana Layout (Sadece TabWidget Barındırır)
        main_lay = QVBoxLayout(self)
        main_lay.setContentsMargins(0, 0, 0, 0)
        main_lay.setSpacing(0)
        
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.TabPosition.North)
        self.tabs.setStyleSheet("""
            QTabWidget::pane { border: none; border-top: 1px solid #D7D6D2; }
            QTabBar::tab {
                background: #E7E6E2;
                border: 1px solid #D7D6D2;
                border-bottom: none;
                padding: 6px 12px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                color: #555;
            }
            QTabBar::tab:selected {
                background: #F9F8F2;
                border-bottom: 1px solid #F9F8F2; /* Kenarlığı gizle */
                font-weight: bold;
                color: #333;
                margin-bottom: -1px; /* Pane üzerine bin */
            }
            QTabBar::tab:hover:!selected {
                background: #F0EFEB;
            }
        """)
        
        # --- TAB 1: FILES (Mevcut İçerik) ---
        self.files_tab = QWidget()
        lay = QVBoxLayout(self.files_tab)
        lay.setContentsMargins(8, 8, 8, 8)
        lay.setSpacing(6)
        
        hdr = QHBoxLayout()
        hdr.setSpacing(6)
        lbl = QLabel("Source Directory")
        lbl.setObjectName("SectionHeader")
        hdr.addWidget(lbl)
        hdr.addStretch()
        
        # Yenileme butonu
        btn_refresh = QPushButton()
        btn_refresh.setObjectName("BrowseBtn")
        btn_refresh.setIcon(QIcon("icons/arrows-rotate-solid.svg"))
        btn_refresh.setIconSize(QSize(14, 14))
        btn_refresh.setFixedWidth(32)
        btn_refresh.setToolTip("Yenile")
        btn_refresh.clicked.connect(self._refresh)
        self.btn_refresh = btn_refresh # Make it accessible for theme changes
        hdr.addWidget(btn_refresh)
        
        # Browse butonu
        self.btn_browse = QPushButton("Browse")
        self.btn_browse.setObjectName("BrowseBtn")
        self.btn_browse.setIcon(QIcon("icons/folder-open-solid.svg"))
        self.btn_browse.setIconSize(QSize(14, 14))
        self.btn_browse.clicked.connect(self._browse)
        hdr.addWidget(self.btn_browse)
        lay.addLayout(hdr)
        
        # Placeholder - klasör seçilmeden önce gösterilir
        self._placeholder = QLabel("Lütfen bir klasör seçin")
        self._placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._placeholder.setStyleSheet("color: #888; font-size: 11px;")
        lay.addWidget(self._placeholder, 1)
        
        self._tree = QTreeView()
        self._tree.setHeaderHidden(True)
        self._tree.setIndentation(24)
        self._tree.setAnimated(False)
        self._tree.setMouseTracking(True)
        self._tree.setRootIsDecorated(True)  # Kök düğümleri de bağla (Tree Lines)
        self._tree.setUniformRowHeights(True)
        self._tree.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self._tree.hide()
        
        self._icons = IconProvider()
        self._model = QFileSystemModel()
        self._model.setOption(QFileSystemModel.Option.DontWatchForChanges, False)
        self._model.setIconProvider(self._icons)
        self._model.setFilter(QDir.Filter.AllDirs | QDir.Filter.Files | QDir.Filter.NoDotAndDotDot)
        
        # Proxy Model Kurulumu (Gizleme Özelliği İçin)
        self._proxy_model = SourceProxyModel(self._hidden_files)
        self._proxy_model.setSourceModel(self._model)
        self._tree.setModel(self._proxy_model)
        
        for c in range(1, 4): self._tree.setColumnHidden(c, True)
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
        
        # --- TAB 2: SETTINGS ---
        self.settings_tab = AppSettingsWidget()
        
        # Add Tabs
        self.tabs.addTab(self.files_tab, "Dosyalar")
        self.tabs.addTab(self.settings_tab, "Ayarlar")
        
        # Set Tab Icons
        self.tabs.setTabIcon(0, QIcon("icons/folder-open-solid.svg"))
        
        main_lay.addWidget(self.tabs)
    
    def update_texts(self, t):
        if hasattr(self, '_placeholder') and "placeholder_select_folder" in t:
            self._placeholder.setText(t["placeholder_select_folder"])
        if hasattr(self, '_path_lbl') and "no_folder_selected" in t:
            # Sadece varsayılan metinse güncelle
            if "No folder" in self._path_lbl.text() or "Klasör" in self._path_lbl.text():
                self._path_lbl.setText(t["no_folder_selected"])
    
    def _refresh(self):
        """Klasörü yenile (Güvenli)"""
        if self._root and self._root.exists():
            # Debounce: Çoklu tıklamayı önle
            if hasattr(self, 'btn_refresh'):
                self.btn_refresh.setEnabled(False)
            
            # Watcher açık olduğu için sadece path'i tekrar set edelim
            # Bu, index'i zorla günceller
            current_path = str(self._root)
            QTimer.singleShot(100, lambda: self._do_refresh(current_path))
    
    def _do_refresh(self, path):
        """Yenileme işlemini tamamla"""
        try:
            idx = self._model.setRootPath(path)
            # Proxy Index'e çevir
            if hasattr(self, '_proxy_model'):
                idx = self._proxy_model.mapFromSource(idx)
            self._tree.setRootIndex(idx)
        except Exception as e:
            print(f"Source refresh error: {e}")
        finally:
            if hasattr(self, 'btn_refresh'):
                self.btn_refresh.setEnabled(True)
    
    def _browse(self):
        p = QFileDialog.getExistingDirectory(self, "Select Folder", str(Path.home()))
        if p: self.set_root(p)

    def set_icon_color(self, color):
        """İkon rengini güncelle ve modeli yenile"""
        # Yeni provider oluşturarak cache sorununu aş
        new_provider = IconProvider()
        new_provider.set_color(color)
        self._model.setIconProvider(new_provider)
        self._icons = new_provider # Referansı güncelle
        
        # Delegate rengini de güncelle
        self._delegate.set_color(color)
        
        # Görünümü zorla yenile
        self._tree.viewport().update()





    def set_root(self, path: str):
        try:
            self._root = Path(path)
            idx = self._model.setRootPath(path)
            
            # Proxy Index'e çevir
            if hasattr(self, '_proxy_model'):
                proxy_idx = self._proxy_model.mapFromSource(idx)
                self._tree.setRootIndex(proxy_idx)
            else:
                 self._tree.setRootIndex(idx)
                 
            self._path_lbl.setText(path)
            
            # Placeholder'ı gizle, TreeView'ı göster
            self._placeholder.hide()
            self._tree.show()
            
            print(f"DEBUG: Root set to {path}") # Debugging
            
            # Klasör değişince gizlenenler listesini temizle
            self._hidden_files.clear()
            self._proxy_model.invalidateFilter()
            
            self.dir_selected.emit(path)
            # Not: expand işlemi source index ile çalışır (model üzerinde), o yüzden idx kullan
            QTimer.singleShot(100, lambda: self._expand(idx, 10))
        except Exception as e:
            self._path_lbl.setText(str(e))
    
    def _expand(self, parent, depth):
        if depth <= 0 or not parent.isValid(): return
        
        # Veriyi yükle (Source Index)
        if self._model.canFetchMore(parent): self._model.fetchMore(parent)
        
        # Görünümü genişlet (Proxy Index Gerekir)
        proxy_idx = parent
        if hasattr(self, '_proxy_model'):
            proxy_idx = self._proxy_model.mapFromSource(parent)
            
        if proxy_idx.isValid():
            self._tree.expand(proxy_idx)
        
        # Alt klasörleri gez (Source Index)
        for r in range(self._model.rowCount(parent)):
            ch = self._model.index(r, 0, parent)
            if ch.isValid() and self._model.isDir(ch):
                self._expand(ch, depth - 1)
    
    def _on_expand(self, idx):
        # idx Proxy Index gelir
        source_idx = idx
        if hasattr(self, '_proxy_model'):
             source_idx = self._proxy_model.mapToSource(idx)
             
        if self._model.canFetchMore(source_idx): self._model.fetchMore(source_idx)
        QTimer.singleShot(50, lambda: self._expand_children(source_idx))
    
    def _expand_children(self, parent):
        # parent Source Index
        for r in range(self._model.rowCount(parent)):
            ch = self._model.index(r, 0, parent)
            if ch.isValid() and self._model.isDir(ch):
                if self._model.canFetchMore(ch): self._model.fetchMore(ch)
                
                # Görünümü genişlet (Proxy Index)
                proxy_ch = ch
                if hasattr(self, '_proxy_model'):
                    proxy_ch = self._proxy_model.mapFromSource(ch)
                
                if proxy_ch.isValid():
                    self._tree.expand(proxy_ch)
    
    def _on_selection_changed(self, selected: QItemSelection, deselected: QItemSelection):
        indexes = selected.indexes()
        if indexes:
            idx = indexes[0]
            # Proxy Index ise Source Index'e çevir
            if hasattr(self, '_proxy_model'):
                 idx = self._proxy_model.mapToSource(idx)
                 
            path = self._model.filePath(idx)
            if path: self.selection_changed.emit(path)
    
    def _on_del(self, idx):
        # idx Proxy Index olabilir, source index'e çevir
        real_idx = idx
        if hasattr(self, '_proxy_model'):
             real_idx = self._proxy_model.mapToSource(idx)
             
        p = self._model.filePath(real_idx)
        if p:
            # KESİN GÜVENLİK KONTROLÜ: Kök Sürücüleri Engelle
            # Kullanıcı "c diskinin tamamı silinmesin" dediği için bu kontrol şart.
            from pathlib import Path
            try:
                path_obj = Path(p)
                # Kök dizin kontrolü (C:\, D:\ vb.)
                # anchor (örn: 'C:\') ile path aynıysa bu bir kök dizindir.
                if path_obj.anchor == str(path_obj) or len(path_obj.parts) <= 1:
                     QMessageBox.critical(self, tr("msg_title_operation_forbidden"), 
                        tr("msg_root_drive_forbidden"))
                     return
            except: pass

            # Onay İste
            reply = QMessageBox.question(
                self, tr("msg_title_hide"), 
                tr("msg_hide_item_confirm", p),
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                import os
                try:
                    norm_p = os.path.normpath(p)
                    self._hidden_files.add(norm_p)
                    self._proxy_model.invalidateFilter()
                except Exception as e:
                    print(f"Hide error: {e}")


# =============================================================================
# FILTER CHIP WIDGET (MODIFIED - RED PILL X)
# =============================================================================

class FilterChip(QWidget):
    removed = pyqtSignal(str)
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
        
        # Kırmızı Oval X Butonu - X işareti içeride
        btn_x = QPushButton("✕")
        btn_x.setFixedSize(20, 20)
        btn_x.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_x.setStyleSheet("""
            QPushButton {
                background-color: #E53935; 
                border: none;
                border-radius: 10px;
                color: white;
                font-weight: bold;
                font-family: Arial;
                font-size: 11px;
                padding: 0px;
            }
            QPushButton:hover {
                background-color: #C62828;
            }
            QPushButton:pressed {
                background-color: #B71C1C;
            }
        """)
        btn_x.clicked.connect(lambda: self.removed.emit(self.filter_id))
        lay.addWidget(btn_x)
        
        self.setStyleSheet("background: #F5F5F5; border: 1px solid #DDD; border-radius: 4px;")

# =============================================================================
# FILTER SETTINGS UI
# =============================================================================

class FilterSettingsPanel(QWidget):
    filter_added = pyqtSignal(str, str, dict)  # filter_type, filter_id, filter_data
    filter_removed = pyqtSignal(str)  # filter_id
    MAX_FILTERS = 5
    
    def __init__(self):
        super().__init__()
        self.forms = {}
        self.active_filters = {}  # {filter_id: {type, chip, desc, data, row, col}}
        self._current_filter_type = None
        self._build()
    def _build(self):
        self.setMinimumWidth(200)  # Minimum genişlik (dinamik küçülme için)
        self.setMaximumWidth(350)  # Maximum genişlik
        lay = QVBoxLayout(self)
        lay.setContentsMargins(10, 4, 8, 4)
        lay.setSpacing(4)
        self.header_lbl = QLabel("Filtre Ayarları")
        self.header_lbl.setFixedHeight(20)
        self.header_lbl.setStyleSheet("font-weight: bold; font-size: 13px; color: #333;")
        lay.addWidget(self.header_lbl)
        self.stack = QStackedWidget()
        self.stack.setFixedHeight(140)
        lay.addWidget(self.stack)
        self._init_forms()
        btn_lay = QHBoxLayout()
        btn_lay.setContentsMargins(0, 0, 0, 0)
        btn_lay.setSpacing(4)
        self.btn_add = QPushButton("Filtre Ekle")
        self.btn_add.setMinimumWidth(50)
        self.btn_add.setFixedHeight(24)
        self.btn_add.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.btn_add.clicked.connect(self._on_add_filter)
        self.btn_reset = QPushButton("Sıfırla")
        self.btn_reset.setMinimumWidth(40)
        self.btn_reset.setFixedHeight(24)
        self.btn_reset.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.btn_reset.clicked.connect(self._on_reset)
        self.btn_cancel = QPushButton("İptal")
        self.btn_cancel.setMinimumWidth(35)
        self.btn_cancel.setFixedHeight(24)
        self.btn_cancel.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.btn_cancel.clicked.connect(self._on_cancel)
        btn_lay.addWidget(self.btn_add, 2)  # Filtre Ekle
        btn_lay.addWidget(self.btn_reset, 2)  # Sıfırla - aynı genişlikte
        btn_lay.addWidget(self.btn_cancel, 1)  # İptal - daha küçük
        lay.addLayout(btn_lay)
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setFixedHeight(2)
        sep.setStyleSheet("background: #ccc;")
        lay.addWidget(sep)
        self.active_header_lbl = QLabel("Aktif Filtreler")
        self.active_header_lbl.setFixedHeight(18)
        self.active_header_lbl.setStyleSheet("font-weight: bold; font-size: 12px;")
        lay.addWidget(self.active_header_lbl)
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
        # Form widget'larını sakla
        self.form_widgets = {}
        
        # Uzantı formu
        f_ext = QWidget()
        l_ext = QVBoxLayout(f_ext)
        l_ext.setContentsMargins(0, 0, 0, 0)
        l_ext.setSpacing(4)
        lbl_ext = QLabel("Uzantılar (örn: jpg, png):")
        self.ext_input = QLineEdit()
        self.ext_input.setPlaceholderText("jpg, png, pdf, docx...")
        ext_info = QLabel("Yaygın: jpg, png, gif, pdf, docx, xlsx, txt, mp3, mp4, zip")
        ext_info.setStyleSheet("color: #888888; font-size: 9px;")
        l_ext.addWidget(lbl_ext)
        l_ext.addWidget(self.ext_input)
        l_ext.addWidget(ext_info)
        l_ext.addStretch()
        self.form_widgets["Uzantı"] = {"input": self.ext_input}
        self._add_stack("Uzantı", f_ext)
        
        # Dosya Adı formu
        f_name = QWidget()
        l_name = QVBoxLayout(f_name)
        l_name.setContentsMargins(0, 0, 0, 0)
        l_name.setSpacing(3)
        lbl_name = QLabel("Arama Metni:")
        self.name_input = QLineEdit()
        self.cb_case = QCheckBox("Harf Duyarlı")
        self.cb_exact = QCheckBox("Tam Eşleşme")
        self.cb_invert = QCheckBox("Tersini Al")
        l_name.addWidget(lbl_name)
        l_name.addWidget(self.name_input)
        l_name.addWidget(self.cb_case)
        l_name.addWidget(self.cb_exact)
        l_name.addWidget(self.cb_invert)
        l_name.addStretch()
        self.form_widgets["Dosya Adı"] = {"input": self.name_input, "case": self.cb_case, "exact": self.cb_exact, "invert": self.cb_invert}
        self._add_stack("Dosya Adı", f_name)
        
        # Metin formu
        f_content = QWidget()
        l_content = QVBoxLayout(f_content)
        l_content.setContentsMargins(0, 0, 0, 0)
        l_content.setSpacing(6)
        lbl_content = QLabel("Dosya İçeriği (Metin):")
        self.content_input = QLineEdit()
        self.cb_content_case = QCheckBox("Büyük/Küçük Harf Duyarlı")
        l_content.addWidget(lbl_content)
        l_content.addWidget(self.content_input)
        l_content.addWidget(self.cb_content_case)
        l_content.addStretch()
        self.form_widgets["Metin"] = {"input": self.content_input, "case": self.cb_content_case}
        self._add_stack("Metin", f_content)
        
        # Regex formu
        f_regex = QWidget()
        l_regex = QVBoxLayout(f_regex)
        l_regex.setContentsMargins(0, 0, 0, 0)
        l_regex.setSpacing(6)
        lbl_regex = QLabel("Regular Expression:")
        self.regex_input = QLineEdit()
        l_regex.addWidget(lbl_regex)
        l_regex.addWidget(self.regex_input)
        l_regex.addStretch()
        self.form_widgets["Regex"] = {"input": self.regex_input}
        self._add_stack("Regex", f_regex)
        
        # Metin Yok formu
        f_nocontent = QWidget()
        l_nocontent = QVBoxLayout(f_nocontent)
        l_nocontent.setContentsMargins(0, 0, 0, 0)
        l_nocontent.setSpacing(6)
        lbl_nocontent = QLabel("İçermeyen Metin:")
        self.nocontent_input = QLineEdit()
        l_nocontent.addWidget(lbl_nocontent)
        l_nocontent.addWidget(self.nocontent_input)
        l_nocontent.addStretch()
        self.form_widgets["Metin Yok"] = {"input": self.nocontent_input}
        self._add_stack("Metin Yok", f_nocontent)
        
        # Boyut formu
        f_size = QWidget()
        l_size = QVBoxLayout(f_size)
        l_size.setContentsMargins(0, 0, 0, 0)
        l_size.setSpacing(4)
        lbl_op = QLabel("Operatör:")
        self.size_op = QComboBox()
        self.size_op.addItems(["> Büyük", "< Küçük", "= Eşit"])
        lbl_val = QLabel("Değer:")
        self.size_val = ModernSpinBox() 
        self.size_val.setRange(0, 999999)
        lbl_unit = QLabel("Birim:")
        self.size_unit = QComboBox()
        self.size_unit.addItems(["MB", "KB", "GB", "Byte"])
        l_size.addWidget(lbl_op)
        l_size.addWidget(self.size_op)
        l_size.addWidget(lbl_val)
        l_size.addWidget(self.size_val)
        l_size.addWidget(lbl_unit)
        l_size.addWidget(self.size_unit)
        l_size.addStretch()
        self.form_widgets["Boyut"] = {"op": self.size_op, "val": self.size_val, "unit": self.size_unit}
        self._add_stack("Boyut", f_size)
        
        # Boş Dosya formu
        f_empty = QWidget()
        l_empty = QVBoxLayout(f_empty)
        l_empty.setContentsMargins(0, 0, 0, 0)
        l_empty.setSpacing(6)
        lbl_empty = QLabel("Boş dosyaları (0 byte) göster.")
        l_empty.addWidget(lbl_empty)
        l_empty.addStretch()
        self.form_widgets["Boş Dosya"] = {}
        self._add_stack("Boş Dosya", f_empty)
        
        # Oluşturma Tarihi formu
        f_date = QWidget()
        l_date = QVBoxLayout(f_date)
        l_date.setContentsMargins(0, 0, 0, 0)
        l_date.setSpacing(6)
        lbl_start = QLabel("Başlangıç:")
        self.date_start = QDateEdit()
        self.date_start.setCalendarPopup(True)
        self.date_start.setDate(QDate.currentDate())
        lbl_end = QLabel("Bitiş:")
        self.date_end = QDateEdit()
        self.date_end.setCalendarPopup(True)
        self.date_end.setDate(QDate.currentDate())
        l_date.addWidget(lbl_start)
        l_date.addWidget(self.date_start)
        l_date.addWidget(lbl_end)
        l_date.addWidget(self.date_end)
        l_date.addStretch()
        self.form_widgets["Oluşturma Tarihi"] = {"start": self.date_start, "end": self.date_end}
        self._add_stack("Oluşturma Tarihi", f_date)
        
        # Değişiklik Tarihi formu
        f_date2 = QWidget()
        l_date2 = QVBoxLayout(f_date2)
        l_date2.setContentsMargins(0, 0, 0, 0)
        l_date2.setSpacing(6)
        lbl_start2 = QLabel("Başlangıç:")
        self.mod_date_start = QDateEdit()
        self.mod_date_start.setCalendarPopup(True)
        self.mod_date_start.setDate(QDate.currentDate())
        lbl_end2 = QLabel("Bitiş:")
        self.mod_date_end = QDateEdit()
        self.mod_date_end.setCalendarPopup(True)
        self.mod_date_end.setDate(QDate.currentDate())
        l_date2.addWidget(lbl_start2)
        l_date2.addWidget(self.mod_date_start)
        l_date2.addWidget(lbl_end2)
        l_date2.addWidget(self.mod_date_end)
        l_date2.addStretch()
        self.form_widgets["Değişiklik Tarihi"] = {"start": self.mod_date_start, "end": self.mod_date_end}
        self._add_stack("Değişiklik Tarihi", f_date2)

        # Şifreli formu
        f_bool = QWidget()
        l_bool = QVBoxLayout(f_bool)
        l_bool.setContentsMargins(0, 0, 0, 0)
        l_bool.setSpacing(6)
        lbl_enc = QLabel("Şifreli dosyaları filtreler.")
        l_bool.addWidget(lbl_enc)
        l_bool.addStretch()
        self.form_widgets["Şifreli"] = {}
        self._add_stack("Şifreli", f_bool)
        
        # Gizli formu
        f_hidden = QWidget()
        l_hidden = QVBoxLayout(f_hidden)
        l_hidden.setContentsMargins(0, 0, 0, 0)
        l_hidden.setSpacing(6)
        lbl_hid = QLabel("Gizli dosyaları göster.")
        l_hidden.addWidget(lbl_hid)
        l_hidden.addStretch()
        self.form_widgets["Gizli"] = {}
        self._add_stack("Gizli", f_hidden)
        
        # Varsayılan form
        f_def = QWidget()
        l_def = QVBoxLayout(f_def)
        l_def.setContentsMargins(0, 0, 0, 0)
        self.placeholder_lbl = QLabel("Soldan bir filtre seçiniz.")
        l_def.addWidget(self.placeholder_lbl)
        l_def.addStretch()
        self.stack.addWidget(f_def)
        self.stack.setCurrentIndex(self.stack.count() - 1) # Varsayılan olarak bunu göster

    def _add_stack(self, name, widget):
        idx = self.stack.addWidget(widget)
        self.forms[name] = idx

    def show_form(self, name):
        # Önceki formu temizle
        if self._current_filter_type and self._current_filter_type != name:
            self._reset_form(self._current_filter_type)
        
        self._current_filter_type = name
        self.header_lbl.setText(f"{name} Ayarları")
        
        # Tarihleri bugüne ayarla
        if name in ["Oluşturma Tarihi", "Değişiklik Tarihi"]:
            self._reset_dates_to_today(name)
        
        if name in self.forms:
            self.stack.setCurrentIndex(self.forms[name])
        else:
            self.stack.setCurrentIndex(self.stack.count()-1)
    
    def _reset_dates_to_today(self, filter_type):
        """Tarihleri bugüne ayarla"""
        today = QDate.currentDate()
        if filter_type == "Oluşturma Tarihi":
            self.date_start.setDate(today)
            self.date_end.setDate(today)
        elif filter_type == "Değişiklik Tarihi":
            self.mod_date_start.setDate(today)
            self.mod_date_end.setDate(today)
    
    def _reset_form(self, filter_type):
        """Belirli bir form türünü sıfırla"""
        if filter_type not in self.form_widgets:
            return
        widgets = self.form_widgets[filter_type]
        if "input" in widgets:
            widgets["input"].clear()
        if "case" in widgets:
            widgets["case"].setChecked(False)
        if "exact" in widgets:
            widgets["exact"].setChecked(False)
        if "invert" in widgets:
            widgets["invert"].setChecked(False)
        if "val" in widgets:
            widgets["val"].setValue(0)
        if "op" in widgets:
            widgets["op"].setCurrentIndex(0)
        if "unit" in widgets:
            widgets["unit"].setCurrentIndex(0)
        if "start" in widgets:
            widgets["start"].setDate(QDate.currentDate())
        if "end" in widgets:
            widgets["end"].setDate(QDate.currentDate())
    
    def _on_add_filter(self):
        if not self._current_filter_type:
            QMessageBox.warning(self, tr("msg_title_error"), tr("msg_select_filter_first"))
            return
        
        # Maksimum filtre sayısı kontrolü
        if len(self.active_filters) >= self.MAX_FILTERS:
            QMessageBox.warning(self, tr("msg_title_warning"), tr("msg_max_filters", self.MAX_FILTERS))
            return
        
        # Filtre verilerini al
        filter_data = self._get_filter_data()
        if filter_data is None:
            return
        
        desc = filter_data.get("desc", "")
        if not desc:
            return
        
        # Aynı filtre türü ve değerinin daha önce eklenip eklenmediğini kontrol et
        for existing_filter in self.active_filters.values():
            if existing_filter["type"] == self._current_filter_type:
                # Aynı tür filtre mevcut - değerleri karşılaştır
                if self._is_duplicate_filter(existing_filter["data"], filter_data):
                    QMessageBox.warning(self, tr("msg_title_warning"), tr("msg_filter_exists", desc))
                    return
        
        import uuid
        filter_id = str(uuid.uuid4())[:8]
        
        chip = FilterChip(filter_id, desc)
        chip.removed.connect(self._on_remove_filter)
        self.chips_lay.addWidget(chip, self._chip_row, self._chip_col)
        self._chip_col += 1
        if self._chip_col >= self._max_cols:
            self._chip_col = 0
            self._chip_row += 1
        
        self.active_filters[filter_id] = {
            "type": self._current_filter_type,
            "chip": chip,
            "desc": desc,
            "data": filter_data,
            "row": self._chip_row if self._chip_col > 0 else self._chip_row - 1,
            "col": (self._chip_col - 1) if self._chip_col > 0 else self._max_cols - 1
        }
        
        # Sinyal emit et
        self.filter_added.emit(self._current_filter_type, filter_id, filter_data)
        
        # Formu temizle (metin kutularını boşalt)
        self._on_reset()
    
    def _on_remove_filter(self, filter_id):
        if filter_id in self.active_filters:
            chip = self.active_filters[filter_id]["chip"]
            self.chips_lay.removeWidget(chip)
            chip.deleteLater()
            del self.active_filters[filter_id]
            self._reorganize_chips()
            self.filter_removed.emit(filter_id)
    
    def _reorganize_chips(self):
        """Chip'leri yeniden düzenle"""
        # Mevcut tüm chip'leri kaldır ve yeniden ekle
        self._chip_row = 0
        self._chip_col = 0
        for filter_id, data in self.active_filters.items():
            chip = data["chip"]
            self.chips_lay.removeWidget(chip)
            self.chips_lay.addWidget(chip, self._chip_row, self._chip_col)
            data["row"] = self._chip_row
            data["col"] = self._chip_col
            self._chip_col += 1
            if self._chip_col >= self._max_cols:
                self._chip_col = 0
                self._chip_row += 1
    
    def _is_duplicate_filter(self, existing_data: dict, new_data: dict) -> bool:
        """İki filtre verisinin aynı olup olmadığını kontrol et"""
        ft = self._current_filter_type
        
        if ft == "Uzantı":
            # Uzantıları normalize edip karşılaştır
            existing_exts = set(existing_data.get("extensions", []))
            new_exts = set(new_data.get("extensions", []))
            return existing_exts == new_exts
        elif ft == "Dosya Adı":
            return existing_data.get("text", "") == new_data.get("text", "")
        elif ft == "Metin":
            return existing_data.get("text", "") == new_data.get("text", "")
        elif ft == "Regex":
            return existing_data.get("pattern", "") == new_data.get("pattern", "")
        elif ft == "Metin Yok":
            return existing_data.get("text", "") == new_data.get("text", "")
        elif ft == "Boyut":
            return (existing_data.get("op") == new_data.get("op") and
                    existing_data.get("value") == new_data.get("value") and
                    existing_data.get("unit") == new_data.get("unit"))
        elif ft in ["Boş Dosya", "Şifreli", "Gizli"]:
            # Bu türler için aynı türde sadece bir tane olabilir
            return True
        elif ft in ["Oluşturma Tarihi", "Değişiklik Tarihi"]:
            return (existing_data.get("start") == new_data.get("start") and
                    existing_data.get("end") == new_data.get("end"))
        
        return False
    
    def _get_filter_data(self) -> dict:
        """Filtre verilerini yapılandırılmış olarak döndür"""
        ft = self._current_filter_type
        data = {"type": ft}
        
        if ft == "Uzantı":
            val = self.ext_input.text().strip()
            if not val:
                QMessageBox.warning(self, tr("msg_title_warning"), tr("msg_extension_empty"))
                return None
            
            # Uzantı validasyonu
            raw_extensions = [ext.strip() for ext in val.split(',') if ext.strip()]
            extensions = []
            errors = []
            
            for ext in raw_extensions:
                # Hatalı formatları kontrol et
                clean_ext = ext.lstrip('.')
                
                # Boş uzantı kontrolü
                if not clean_ext:
                    errors.append(tr("msg_invalid_empty_extension", ext))
                    continue
                
                # Çift nokta kontrolü (..txt gibi)
                if '..' in ext or ext.startswith('..'):
                    errors.append(tr("msg_invalid_double_dot", ext))
                    continue
                
                # Özel karakter kontrolü
                invalid_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|', ' ']
                has_invalid = False
                for char in invalid_chars:
                    if char in clean_ext:
                        errors.append(tr("msg_invalid_char", ext, char))
                        has_invalid = True
                        break
                
                if not has_invalid:
                    extensions.append(clean_ext.lower())
            
            if errors:
                QMessageBox.warning(self, tr("msg_title_invalid_extension"), "\n".join(errors))
                return None
            
            if not extensions:
                QMessageBox.warning(self, tr("msg_title_warning"), tr("msg_no_valid_extension"))
                return None
            
            data["extensions"] = extensions
            # Temiz uzantıları göster
            data["desc"] = f"Uzantı: {', '.join(extensions)}"
            
        elif ft == "Dosya Adı":
            val = self.name_input.text().strip()
            if not val:
                return None
            data["text"] = val
            data["case_sensitive"] = self.cb_case.isChecked()
            data["exact_match"] = self.cb_exact.isChecked()
            data["invert"] = self.cb_invert.isChecked()
            data["desc"] = f"Ad: '{val}'"
            
        elif ft == "Metin":
            val = self.content_input.text().strip()
            if not val:
                return None
            data["text"] = val
            data["case_sensitive"] = self.cb_content_case.isChecked()
            data["desc"] = f"İçerik: '{val}'"
            
        elif ft == "Regex":
            val = self.regex_input.text().strip()
            if not val:
                return None
            # Regex'i doğrula
            import re
            try:
                re.compile(val)
            except re.error:
                QMessageBox.warning(self, tr("msg_title_error"), tr("msg_invalid_regex"))
                return None
            data["pattern"] = val
            data["desc"] = f"Regex: {val}"
            
        elif ft == "Metin Yok":
            val = self.nocontent_input.text().strip()
            if not val:
                return None
            data["text"] = val
            data["desc"] = f"İçermez: '{val}'"
            
        elif ft == "Boyut":
            op_text = self.size_op.currentText()
            op = op_text[0]  # >, <, =
            val = self.size_val.value()
            unit = self.size_unit.currentText()
            data["op"] = op
            data["value"] = val
            data["unit"] = unit
            data["desc"] = f"Boyut: {op}{val}{unit}"
            
        elif ft == "Boş Dosya":
            data["desc"] = "Boş: 0B"
            
        elif ft == "Oluşturma Tarihi":
            start = self.date_start.date()
            end = self.date_end.date()
            data["start"] = start.toString("yyyy-MM-dd")
            data["end"] = end.toString("yyyy-MM-dd")
            data["desc"] = f"Oluşturma: {start.toString('dd.MM.yyyy')}-{end.toString('dd.MM.yyyy')}"
            
        elif ft == "Değişiklik Tarihi":
            start = self.mod_date_start.date()
            end = self.mod_date_end.date()
            data["start"] = start.toString("yyyy-MM-dd")
            data["end"] = end.toString("yyyy-MM-dd")
            data["desc"] = f"Değişiklik: {start.toString('dd.MM.yyyy')}-{end.toString('dd.MM.yyyy')}"
            
        elif ft == "Şifreli":
            data["desc"] = "Şifreli"
            
        elif ft == "Gizli":
            data["desc"] = "Gizli"
        
        else:
            data["desc"] = ft
        
        return data
    
    def _get_filter_description(self) -> str:
        ft = self._current_filter_type
        if ft == "Uzantı":
            val = self.ext_input.text().strip()
            if not val: return ""
            return f"Uzantı: {val}"
        elif ft == "Dosya Adı":
            val = self.name_input.text().strip()
            if not val: return ""
            return f"Ad: '{val}'"
        elif ft == "Boyut":
            op = self.size_op.currentText()[0]  # >, <, =
            val = self.size_val.value()
            unit = self.size_unit.currentText()
            return f"Boyut: {op}{val}{unit}"
        elif ft == "Regex":
            val = self.regex_input.text().strip()
            if not val: return ""
            return f"Regex: {val}"
        elif ft == "Metin":
            val = self.content_input.text().strip()
            if not val: return ""
            return f"İçerik: '{val}'"
        elif ft == "Metin Yok":
            val = self.nocontent_input.text().strip()
            if not val: return ""
            return f"İçermez: '{val}'"
        elif ft == "Boş Dosya":
            return "Boş: 0B"
        elif ft == "Oluşturma Tarihi":
            start = self.date_start.date().toString("dd.MM.yyyy")
            end = self.date_end.date().toString("dd.MM.yyyy")
            return f"Oluşturma: {start}-{end}"
        elif ft == "Değişiklik Tarihi":
            start = self.mod_date_start.date().toString("dd.MM.yyyy")
            end = self.mod_date_end.date().toString("dd.MM.yyyy")
            return f"Değişiklik: {start}-{end}"
        elif ft == "Şifreli":
            return "Şifreli"
        elif ft == "Gizli":
            return "Gizli"
        return ft
    
    def _on_reset(self):
        """Mevcut formu sıfırla"""
        ft = self._current_filter_type
        if not ft:
            return
        # Tüm metin inputlarını temizle
        if ft in self.form_widgets:
            widgets = self.form_widgets[ft]
            if "input" in widgets:
                widgets["input"].clear()
            if "case" in widgets:
                widgets["case"].setChecked(False)
            if "exact" in widgets:
                widgets["exact"].setChecked(False)
            if "invert" in widgets:
                widgets["invert"].setChecked(False)
            if "val" in widgets:
                widgets["val"].setValue(0)
            if "op" in widgets:
                widgets["op"].setCurrentIndex(0)
            if "unit" in widgets:
                widgets["unit"].setCurrentIndex(0)
            if "start" in widgets:
                widgets["start"].setDate(QDate.currentDate())
            if "end" in widgets:
                widgets["end"].setDate(QDate.currentDate())
    
    def _on_cancel(self):
        """Formu kapat ve varsayılan görünüme dön"""
        self._on_reset()  # Önce formu sıfırla
        self._current_filter_type = None
        self.header_lbl.setText("Filtre Ayarları")
    def update_texts(self, t):
        if hasattr(self, 'placeholder_lbl') and "placeholder_select_filter" in t:
             self.placeholder_lbl.setText(t["placeholder_select_filter"])
        if hasattr(self, 'active_header_lbl') and "label_active_filters" in t:
             self.active_header_lbl.setText(t["label_active_filters"])

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
        main_lay.setContentsMargins(8, 8, 8, 8)
        main_lay.setSpacing(0)
        main_lay.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop) # Bloğu tepeye yasla
        container = QWidget()
        container.setFixedWidth(160) # Oran düzenlendi (Aksiyon ile aynı)
        lay = QVBoxLayout(container)
        lay.setContentsMargins(0, 0, 8, 0)
        lay.setSpacing(4) # Boşluklar biraz daha açıldı
        # Alignment kaldırıldı - Dinamik uzama için
        
        self.header_lbl = QLabel("Filters")
        self.header_lbl.setFixedHeight(24) # Başlık konumu sabit kalsın
        self.header_lbl.setObjectName("SectionHeader")
        lay.addWidget(self.header_lbl, 0)
        
        self._btn_group = QButtonGroup(self)
        self._btn_group.setExclusive(True)  # Sadece biri seçili olabilir
        self._btn_group.buttonToggled.connect(self._on_group_toggled)
        for f in self.FILTERS:
            b = QPushButton(f)
            b.setProperty("filter_key", f)
            b.setObjectName("ListBtn")
            b.setCheckable(True)
            b.setMinimumHeight(24)
            # Dikeyde dinamik uzama sağla
            b.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            b.setToolTip(self.TOOLTIPS.get(f, ""))
            lay.addWidget(b, 1) # Her buton eşit stretch alsın
            self._btn_group.addButton(b)
            
        main_lay.addWidget(container)
        main_lay.addWidget(GradientLine())
        self.settings_panel = FilterSettingsPanel()
        main_lay.addWidget(self.settings_panel, 1)  # Stretch factor 1 - dinamik genişleme
        
        # İlk butonu varsayılan olarak aktif yap (Initialization sorununu çözer)
        # if self._btn_group.buttons():
        #     self._btn_group.buttons()[0].setChecked(True)

    def _on_group_toggled(self, btn, checked):
        if checked:
            self.settings_panel.show_form(btn.text())

    def update_texts(self, t):
        if hasattr(self, 'header_lbl'):
             if "filter_panel_header" in t:
                 self.header_lbl.setText(t["filter_panel_header"])
        
        for b in self._btn_group.buttons():
            key = b.property("filter_key")
            # key örn: "Uzantı" -> dict key: "filter_Uzantı"
            dict_key = f"filter_{key}"
            if key and dict_key in t:
                b.setText(t[dict_key])

# =============================================================================
# ACTION SETTINGS UI
# =============================================================================

class ActionSettingsPanel(QWidget):
    action_requested = pyqtSignal(str, dict)
    def __init__(self):
        super().__init__()
        self.forms = {}
        self._current_action = None
        self._build()
    def _build(self):
        self.setMinimumWidth(200) # Filtre ile aynı min genişlik
        self.setMaximumWidth(350) 
        lay = QVBoxLayout(self)
        lay.setContentsMargins(10, 4, 8, 4) 
        lay.setSpacing(4) 
        lay.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        
        self.header_lbl = QLabel("Aksiyon Ayarları")
        self.header_lbl.setFixedHeight(20)
        self.header_lbl.setStyleSheet("font-weight: bold; font-size: 13px; color: #333;")
        lay.addWidget(self.header_lbl)
        
        self.stack = QStackedWidget()
        self.stack.setMinimumHeight(150) # İçerik sığsın diye biraz esnek bıraktık (Filtre'de 140'tı)
        # self.stack.setFixedHeight(150) # İsterseniz sabitleyebilirsiniz ama aksiyonlar daha karmaşık olabilir
        lay.addWidget(self.stack)
        
        self._init_forms()
        
        # Action Buttons Layout (Matching Reference: Uygula, Sıfırla, İptal)
        btn_lay = QHBoxLayout()
        btn_lay.setContentsMargins(0, 0, 0, 0)
        btn_lay.setSpacing(4)
        
        self.btn_apply = QPushButton("Uygula")
        self.btn_apply.setMinimumWidth(50)
        self.btn_apply.setFixedHeight(24)
        self.btn_apply.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.btn_apply.clicked.connect(self._on_apply)
        
        self.btn_reset = QPushButton("Sıfırla")
        self.btn_reset.setMinimumWidth(40)
        self.btn_reset.setFixedHeight(24)
        self.btn_reset.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.btn_reset.clicked.connect(self._on_reset)
        
        self.btn_cancel = QPushButton("İptal")
        self.btn_cancel.setMinimumWidth(35)
        self.btn_cancel.setFixedHeight(24)
        self.btn_cancel.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.btn_cancel.clicked.connect(self._on_cancel)
        
        btn_lay.addWidget(self.btn_apply, 2)
        btn_lay.addWidget(self.btn_reset, 2)
        btn_lay.addWidget(self.btn_cancel, 1)
        
        lay.addLayout(btn_lay)
        lay.addStretch(1) # Alt kısmı boşlukla doldur

    def _init_forms(self):
        # 1. Sıralı Adlandırma
        f1 = QWidget()
        l1 = QVBoxLayout(f1)
        l1.setContentsMargins(0,0,0,0)
        l1.setSpacing(6)
        
        l1.addWidget(QLabel("Desen: (örn: Tatil_{n})"))
        h_inp1 = QHBoxLayout()
        self.seq_pattern = QLineEdit()
        self.seq_pattern.setPlaceholderText("Dosya_{n}")
        self.seq_pattern.setMinimumWidth(120)
        h_inp1.addWidget(self.seq_pattern)
        l1.addLayout(h_inp1)
        
        grid1 = QGridLayout()
        grid1.addWidget(QLabel("Başlangıç:"), 0, 0)
        self.seq_start = ModernSpinBox()
        self.seq_start.setValue(1)
        grid1.addWidget(self.seq_start, 0, 1)
        
        grid1.addWidget(QLabel("Artış:"), 1, 0)
        self.seq_step = ModernSpinBox()
        self.seq_step.setValue(1)
        grid1.addWidget(self.seq_step, 1, 1)
        
        grid1.addWidget(QLabel("Basamak:"), 2, 0)
        self.seq_pad = ModernSpinBox()
        self.seq_pad.setValue(3) # 001
        self.seq_pad.setRange(1, 10)
        grid1.addWidget(self.seq_pad, 2, 1)
        l1.addLayout(grid1)
        l1.addStretch()
        self._add_stack("seq_rename", f1)
        
        # 2. Ön/Son Ek
        f2 = QWidget()
        l2 = QVBoxLayout(f2)
        l2.setContentsMargins(0,0,0,0)
        l2.setSpacing(6)
        l2.addWidget(QLabel("Ön Ek:"))
        self.prefix_inp = QLineEdit()
        l2.addWidget(self.prefix_inp)
        l2.addWidget(QLabel("Son Ek:"))
        self.suffix_inp = QLineEdit()
        l2.addWidget(self.suffix_inp)
        l2.addStretch()
        self._add_stack("prefix_suffix", f2)
        
        # 3. Bul/Değiştir
        f3 = QWidget()
        l3 = QVBoxLayout(f3)
        l3.setContentsMargins(0,0,0,0)
        l3.setSpacing(6)
        l3.addWidget(QLabel("Bul:"))
        self.find_inp = QLineEdit()
        l3.addWidget(self.find_inp)
        l3.addWidget(QLabel("Değiştir:"))
        self.replace_inp = QLineEdit()
        l3.addWidget(self.replace_inp)
        self.find_case = QCheckBox("Büyük/Küçük Harf Duyarlı")
        l3.addWidget(self.find_case)
        l3.addStretch()
        self._add_stack("find_replace", f3)
        
        # 4. Uzantı Değiştir (Basit tutuldu)
        f4 = QWidget()
        l4 = QVBoxLayout(f4)
        l4.setContentsMargins(0,0,0,0)
        l4.setSpacing(6)
        l4.addWidget(QLabel("Yeni Uzantı:"))
        self.ext_inp = QLineEdit()
        l4.addWidget(self.ext_inp)
        l4.addStretch()
        self._add_stack("change_ext", f4)
        
        # 5. Kopyala
        f_copy = QWidget()
        l_copy = QVBoxLayout(f_copy)
        l_copy.setContentsMargins(0,0,0,0)
        l_copy.setSpacing(6)
        l_copy.addWidget(QLabel("Hedef Klasör:"))
        h_copy = QHBoxLayout()
        self.copy_path_inp = QLineEdit()
        btn_browse = QPushButton()
        btn_browse.setFixedSize(26, 26)
        btn_browse.setIcon(QIcon("icons/folder-open-solid.svg"))
        btn_browse.clicked.connect(self._on_browse_copy)
        h_copy.addWidget(self.copy_path_inp)
        h_copy.addWidget(btn_browse)
        l_copy.addLayout(h_copy)
        
        l_copy.addWidget(QLabel("Çakışma Yönetimi:"))
        self.copy_conflict = QComboBox()
        self.copy_conflict.addItems(["Üzerine Yaz", "Atla", "Kopya Oluştur"])
        l_copy.addWidget(self.copy_conflict)
        l_copy.addStretch()
        self._add_stack("copy", f_copy)

        # 6. Etiket (Yeni)
        f_tag = QWidget()
        l_tag = QVBoxLayout(f_tag)
        l_tag.setContentsMargins(0,0,0,0)
        l_tag.addWidget(QLabel("Etiket Metni:"))
        self.tag_text = QLineEdit()
        l_tag.addWidget(self.tag_text)
        
        l_tag.addWidget(QLabel("Renk:"))
        self.tag_color = QComboBox()
        self.tag_color.addItems(["Kırmızı", "Yeşil", "Mavi", "Sarı", "Gri"])
        l_tag.addWidget(self.tag_color)
        
        l_tag.addWidget(QLabel("Uygulama:"))
        self.tag_scope = QComboBox()
        self.tag_scope.addItems(["Dosya Sistemi", "Metadata"])
        l_tag.addWidget(self.tag_scope)
        l_tag.addStretch()
        self._add_stack("tag", f_tag)
        
        # 7. Tek Klasör (Flatten)
        f_flat = QWidget()
        l_flat = QVBoxLayout(f_flat)
        l_flat.setContentsMargins(0,0,0,0)
        l_flat.addWidget(QLabel("Derinlik (0=Sınırsız):"))
        self.flat_depth = ModernSpinBox()
        self.flat_depth.setRange(0, 50)
        l_flat.addWidget(self.flat_depth)
        
        self.flat_del_empty = QCheckBox("Boş klasörleri sil")
        l_flat.addWidget(self.flat_del_empty)
        
        l_flat.addWidget(QLabel("İsim Çakışması:"))
        self.flat_conflict = QComboBox()
        self.flat_conflict.addItems(["Yeniden Adlandır", "Üzerine Yaz", "Atla"])
        l_flat.addWidget(self.flat_conflict)
        l_flat.addStretch()
        self._add_stack("flatten", f_flat)
        
        # 8. Güvenli Sil
        f_del = QWidget()
        l_del = QVBoxLayout(f_del)
        l_del.setContentsMargins(0,0,0,0)
        l_del.addWidget(QLabel("Yöntem:"))
        self.sdel_method = QComboBox()
        self.sdel_method.addItems(["NIST 800-88 Clear (1-Pass)", "NIST 800-88 Purge (3-Pass Random)", "Zero Fill (1-Pass)"])
        l_del.addWidget(self.sdel_method)
        
        self.sdel_verify = QCheckBox("Silme işlemini doğrula")
        l_del.addWidget(self.sdel_verify)
        l_del.addStretch()
        self._add_stack("secure_del", f_del)
        
        # 9. Metin Birleştir
        f_merge = QWidget()
        l_merge = QVBoxLayout(f_merge)
        l_merge.setContentsMargins(0,0,0,0)
        l_merge.addWidget(QLabel("Ayraç:"))
        self.merge_sep = QComboBox()
        self.merge_sep.addItems(["Satır Sonu (\\n)", "Virgül", "Boşluk"])
        l_merge.addWidget(self.merge_sep)
        
        l_merge.addWidget(QLabel("Sıralama:"))
        self.merge_sort = QComboBox()
        self.merge_sort.addItems(["Dosya Adı", "Tarih", "Boyut"])
        l_merge.addWidget(self.merge_sort)
        
        l_merge.addWidget(QLabel("Çıktı Dosya Adı:"))
        self.merge_output = QLineEdit("merged_output.txt")
        l_merge.addWidget(self.merge_output)
        l_merge.addStretch()
        self._add_stack("merge", f_merge)
        
        # 10. Raporlama (CSV/Excel)
        f_rep = QWidget()
        l_rep = QVBoxLayout(f_rep)
        l_rep.setContentsMargins(0,0,0,0)
        l_rep.addWidget(QLabel("Sütunlar:"))
        
        self.rep_cols = []
        for col in ["Dosya Adı", "Yol", "Boyut", "Tarih", "Hash"]:
             cb = QCheckBox(col)
             cb.setChecked(True)
             l_rep.addWidget(cb)
             self.rep_cols.append(cb)
        
        l_rep.addWidget(QLabel("Ayırıcı (CSV):"))
        self.rep_sep = QComboBox()
        self.rep_sep.addItems(["Virgül (,)", "Noktalı Virgül (;)"])
        l_rep.addWidget(self.rep_sep)
        
        l_rep.addWidget(QLabel("Kodlama:"))
        self.rep_enc = QComboBox()
        self.rep_enc.addItems(["UTF-8", "ANSI", "UTF-16"])
        l_rep.addWidget(self.rep_enc)
        
        l_rep.addWidget(QLabel("Çıktı Yolu:"))
        rep_path_lay = QHBoxLayout()
        self.rep_path_inp = QLineEdit(str(Path.home() / "Desktop" / "Rapor.csv"))
        rep_path_lay.addWidget(self.rep_path_inp)
        btn_rep_browse = QPushButton("...")
        btn_rep_browse.setFixedWidth(30)
        btn_rep_browse.clicked.connect(self._on_browse_report_path)
        rep_path_lay.addWidget(btn_rep_browse)
        l_rep.addLayout(rep_path_lay)
        
        l_rep.addStretch()
        self._add_stack("csv", f_rep)
        self._add_stack("excel", f_rep) # Reuse same form widget for Excel
        
        f_def = QWidget()
        l_def = QVBoxLayout(f_def)
        l_def.setContentsMargins(0,0,0,0)
        self.placeholder_lbl = QLabel("Soldan bir aksiyon seçiniz.")
        l_def.addWidget(self.placeholder_lbl)
        l_def.addStretch()
        self.stack.addWidget(f_def)
        self.stack.setCurrentIndex(self.stack.count() - 1) # Varsayılan olarak bunu göster

    def _on_browse_copy(self):
        p = QFileDialog.getExistingDirectory(self, "Hedef Klasör Seç", str(Path.home()))
        if p:
            self.copy_path_inp.setText(p)

    def _on_browse_report_path(self):
        p, _ = QFileDialog.getSaveFileName(self, "Rapor Kaydet", str(Path.home() / "Desktop" / "Rapor.csv"), "CSV Files (*.csv);;All Files (*)")
        if p:
            self.rep_path_inp.setText(p)

    def _add_stack(self, key, widget):
        idx = self.stack.addWidget(widget)
        self.forms[key] = idx

    def show_form(self, action_key, display_name):
        self._on_reset() # Önceki formu temizle
        self._current_action = action_key
        self.header_lbl.setText(f"{display_name} Ayarları")
        if action_key in self.forms:
            self.stack.setCurrentIndex(self.forms[action_key])
        else:
            self.stack.setCurrentIndex(self.stack.count()-1)
    
    
    def _on_apply(self):
        if self._current_action:
            data = self._get_action_data(self._current_action)
            if data is not None:
                self.action_requested.emit(self._current_action, data)
                self._on_reset() # Başarılı ise formu temizle
    
    def load_from_data(self, key, data):
        """Mevcut veriyi forma yükle"""
        if key not in self.forms:
            return
            
        self.stack.setCurrentIndex(self.forms[key])
        
        # Helper to set combo box text safely
        def set_combo(combo, text):
            idx = combo.findText(text)
            if idx >= 0: combo.setCurrentIndex(idx)
            
        if key == "seq_rename":
            self.seq_pattern.setText(data.get("pattern", ""))
            self.seq_start.setValue(data.get("start", 1))
            self.seq_step.setValue(data.get("step", 1))
            self.seq_pad.setValue(data.get("pad", 3))
        elif key == "prefix_suffix":
            self.prefix_inp.setText(data.get("prefix", ""))
            self.suffix_inp.setText(data.get("suffix", ""))
        elif key == "find_replace":
            self.find_inp.setText(data.get("find", ""))
            self.replace_inp.setText(data.get("replace", ""))
            self.find_case.setChecked(data.get("case", False))
        elif key == "change_ext":
            self.ext_inp.setText(data.get("new_ext", ""))
        elif key == "copy":
            self.copy_path_inp.setText(data.get("target", ""))
            set_combo(self.copy_conflict, data.get("conflict", ""))
        elif key == "tag":
            self.tag_text.setText(data.get("text", ""))
            set_combo(self.tag_color, data.get("color", ""))
            set_combo(self.tag_scope, data.get("scope", ""))
        elif key == "flatten":
            self.flat_depth.setValue(data.get("depth", 0))
            self.flat_del_empty.setChecked(data.get("del_empty", False))
            set_combo(self.flat_conflict, data.get("conflict", ""))
        elif key == "secure_del":
            set_combo(self.sdel_method, data.get("method", ""))
            self.sdel_verify.setChecked(data.get("verify", False))
        elif key == "merge":
            set_combo(self.merge_sep, data.get("sep", ""))
            set_combo(self.merge_sort, data.get("sort", ""))
            self.merge_output.setText(data.get("output", ""))
        elif key in ["csv", "excel"]:
            cols = data.get("columns", [])
            for cb in self.rep_cols:
                cb.setChecked(cb.text() in cols)
            set_combo(self.rep_sep, data.get("sep", ""))
            set_combo(self.rep_enc, data.get("encoding", ""))
            self.rep_path_inp.setText(data.get("output_path", ""))
            
    def _get_action_data(self, key):
        """Formdaki verileri topla ve doğrula"""
        data = {}
        if key == "seq_rename":
            data["pattern"] = self.seq_pattern.text()
            data["start"] = self.seq_start.value()
            data["step"] = self.seq_step.value()
            data["pad"] = self.seq_pad.value()
            if not data["pattern"]:
                QMessageBox.warning(self, tr("msg_title_warning"), tr("msg_pattern_empty"))
                return None
        elif key == "prefix_suffix":
            data["prefix"] = self.prefix_inp.text()
            data["suffix"] = self.suffix_inp.text()
            if not data["prefix"] and not data["suffix"]:
                return None
        elif key == "find_replace":
            data["find"] = self.find_inp.text()
            data["replace"] = self.replace_inp.text()
            data["case"] = self.find_case.isChecked()
            if not data["find"]:
                QMessageBox.warning(self, tr("msg_title_warning"), tr("msg_search_text_empty"))
                return None
        elif key == "change_ext":
            data["new_ext"] = self.ext_inp.text()
            if not data["new_ext"]: return None
        elif key == "copy":
            data["target"] = self.copy_path_inp.text()
            data["conflict"] = self.copy_conflict.currentText()
            if not data["target"]:
                QMessageBox.warning(self, tr("msg_title_warning"), tr("msg_target_folder_empty"))
                return None
        elif key == "tag":
            data["text"] = self.tag_text.text()
            data["color"] = self.tag_color.currentText()
            data["scope"] = self.tag_scope.currentText()
        elif key == "flatten":
            data["depth"] = self.flat_depth.value()
            data["del_empty"] = self.flat_del_empty.isChecked()
            data["conflict"] = self.flat_conflict.currentText()
        elif key == "secure_del":
            data["method"] = self.sdel_method.currentText()
            data["verify"] = self.sdel_verify.isChecked()
        elif key == "merge":
            data["sep"] = self.merge_sep.currentText()
            data["sort"] = self.merge_sort.currentText()
            data["output"] = self.merge_output.text()
        elif key in ["csv", "excel"]:
            cols = [cb.text() for cb in self.rep_cols if cb.isChecked()]
            data["columns"] = cols
            data["sep"] = self.rep_sep.currentText()
            data["encoding"] = self.rep_enc.currentText()
            data["output_path"] = self.rep_path_inp.text()
            if not data["output_path"]:
                 QMessageBox.warning(self, tr("msg_title_warning"), tr("msg_output_path_empty"))
                 return None
            
        return data

    def _on_reset(self):
        """Mevcut aksiyon formunu sıfırla"""
        current_widget = self.stack.currentWidget()
        if current_widget:
            for child in current_widget.findChildren(QLineEdit):
                child.clear()
            for child in current_widget.findChildren(ModernSpinBox):
                child.setValue(0)
            for child in current_widget.findChildren(QCheckBox):
                child.setChecked(False)
            for child in current_widget.findChildren(QComboBox):
                child.setCurrentIndex(0)
    
    def _on_cancel(self):
        self._on_reset()  # Önce formu sıfırla
        self._current_action = None
        self.header_lbl.setText("Aksiyon Ayarları")
        self.stack.setCurrentIndex(self.stack.count() - 1)

    def update_texts(self, t):
        if hasattr(self, 'placeholder_lbl') and "placeholder_select_action" in t:
             self.placeholder_lbl.setText(t["placeholder_select_action"])
        if hasattr(self, 'header_lbl') and "action_settings_header" in t:
             self.header_lbl.setText(t["action_settings_header"])

# =============================================================================
# ACTIVE ACTIONS PANEL (NEW)
# =============================================================================

class TaskItem(QFrame):
    removed = pyqtSignal(int)
    edit_requested = pyqtSignal(int)
    
    def __init__(self, index, text, key, data):
        super().__init__()
        self.setObjectName("TaskItem")
        self.index = index
        self.action_key = key
        self.action_data = data
        self.setFixedHeight(30)
        
        lay = QHBoxLayout(self)
        lay.setContentsMargins(8, 0, 4, 0)
        lay.setSpacing(8)
        
        self.lbl = QLabel(f"{index}. {text}")
        self.lbl.setStyleSheet("font-weight: bold; font-size: 11px;")
        lay.addWidget(self.lbl, 1)
        
        # Action Icons
        self.btn_edit = QPushButton()
        self.btn_edit.setFixedSize(20, 20)
        self.btn_edit.setToolTip("Düzenle")
        self.btn_edit.setIcon(QIcon("icons/edit-solid.svg"))
        self.btn_edit.setIconSize(QSize(14, 14))
        self.btn_edit.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_edit.setStyleSheet("QPushButton { border: none; background: transparent; } QPushButton:hover { opacity: 0.7; }")
        self.btn_edit.clicked.connect(lambda: self.edit_requested.emit(self.index))
        
        self.btn_del = QPushButton()
        self.btn_del.setFixedSize(20, 20)
        self.btn_del.setToolTip("Kaldır")
        self.btn_del.setIcon(QIcon("icons/xmark-solid.svg"))
        self.btn_del.setIconSize(QSize(12, 12))
        self.btn_del.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_del.setStyleSheet("QPushButton { border: none; background: transparent; color: #888; } QPushButton:hover { color: red; }")
        self.btn_del.clicked.connect(lambda: self.removed.emit(self.index))
        
        lay.addWidget(self.btn_edit)
        lay.addWidget(self.btn_del)
        
    def update_display(self, text):
        self.lbl.setText(f"{self.index}. {text}")

class ActiveActionsPanel(QWidget):
    run_requested = pyqtSignal()
    edit_requested = pyqtSignal(int)
    
    def __init__(self):
        super().__init__()
        self._build()
        
    def _build(self):
        lay = QVBoxLayout(self)
        lay.setContentsMargins(12, 8, 12, 10)
        lay.setSpacing(8)
        
        self.header_lbl = QLabel("Aktif Aksiyonlar")
        self.header_lbl.setFixedHeight(20) # Diğer başlıklarla aynı (20px)
        self.header_lbl.setStyleSheet("font-weight: bold; font-size: 13px;")
        lay.addWidget(self.header_lbl)
        
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll.setStyleSheet("background: transparent;")
        
        self.container = QWidget()
        self.container.setStyleSheet("background: transparent;")
        self.task_lay = QVBoxLayout(self.container)
        self.task_lay.setContentsMargins(0, 0, 0, 0)
        self.task_lay.setSpacing(4)
        self.task_lay.addStretch()
        
        self.scroll.setWidget(self.container)
        lay.addWidget(self.scroll, 1)
        
        # Placeholder for no actions
        self._no_action_lbl = QLabel("Aksiyon Yok")
        self._no_action_lbl.setObjectName("NoActionLabel")
        self._no_action_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._no_action_lbl.setStyleSheet("color: #888; font-size: 11px;")
        lay.addWidget(self._no_action_lbl)

        # Separator Line
        self.sep = QFrame()
        self.sep.setFrameShape(QFrame.Shape.HLine)
        self.sep.setFixedHeight(1)
        self.sep.setStyleSheet("background-color: #D7D6D2;")
        lay.addWidget(self.sep)
        
        # Progress Section
        self.prog_container = QWidget()
        prog_lay = QVBoxLayout(self.prog_container)
        prog_lay.setContentsMargins(0, 0, 0, 0)
        prog_lay.setSpacing(4)
        
        status_lay = QHBoxLayout()
        lbl_prog = QLabel("İlerleme (Toplam İşlem)")
        lbl_prog.setStyleSheet("font-size: 11px; color: #555;")
        self.lbl_status = QLabel("0/0 Tamamlandı")
        self.lbl_status.setStyleSheet("font-size: 11px; color: #333; font-weight: bold;")
        status_lay.addWidget(lbl_prog)
        status_lay.addStretch()
        status_lay.addWidget(self.lbl_status)
        prog_lay.addLayout(status_lay)
        
        self.progress = QProgressBar()
        self.progress.setValue(0)
        prog_lay.addWidget(self.progress)
        
        lay.addWidget(self.prog_container)
        self.prog_container.hide() # Start hidden
        
        # Run Button Logic (New)
        # ---------------------------------------------------------------------
        self.btn_run_all = QPushButton("Tümünü Başlat")
        self.btn_run_all.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_run_all.setFixedHeight(35) # Fix height permanently
        self.btn_run_all.setStyleSheet("""
            QPushButton {
                background-color: #3B82F6;
                color: white;
                font-weight: bold;
                border-radius: 4px;
                padding: 6px;
            }
            QPushButton:hover { background-color: #2563EB; }
            QPushButton:pressed { background-color: #1D4ED8; }
            QPushButton:disabled { background-color: #3B82F6; opacity: 0.7; color: white; }
        """)
        self.btn_run_all.clicked.connect(self.run_requested.emit)
        lay.addWidget(self.btn_run_all)
        
        self._icon_color = "#444444" # Default setting
        
        # Panel görünürlüğünü başlat
        self.update_panel_visibility()

    def set_icon_color(self, color):
        """Aktif ve gelecek görevlerin ikon rengini ayarlar"""
        self._icon_color = color
        # Mevcut görevleri güncelle
        for i in range(self.task_lay.count()):
            w = self.task_lay.itemAt(i).widget()
            if isinstance(w, TaskItem):
                w.btn_edit.setIcon(IconProvider.make_icon("icons/edit-solid.svg", color))
                w.btn_del.setIcon(IconProvider.make_icon("icons/xmark-solid.svg", color))
        
    def add_task(self, key, data, text, item_count=0):
        try:
            # Re-index existing tasks
            current_tasks = []
            for i in range(self.task_lay.count() - 1): # Exclude stretch
                widget = self.task_lay.itemAt(i).widget()
                if isinstance(widget, TaskItem):
                    current_tasks.append(widget)
            
            new_index = len(current_tasks) + 1
            item = TaskItem(new_index, text, key, data)
            # Apply current theme color to icons
            item.btn_edit.setIcon(IconProvider.make_icon("icons/edit-solid.svg", self._icon_color))
            item.btn_del.setIcon(IconProvider.make_icon("icons/xmark-solid.svg", self._icon_color))
            
            item.removed.connect(self.remove_task)
            item.edit_requested.connect(self.edit_requested.emit)
            self.task_lay.insertWidget(self.task_lay.count() - 1, item) # Insert before stretch
            
            # Update indices of existing tasks
            for i, task_item in enumerate(current_tasks):
                task_item.index = i + 1
                task_item.update_display(task_item.lbl.text().split('. ', 1)[1]) # Update label text
            
            self.update_panel_visibility()
        except Exception as e:
            print(f"add_task error: {e}")
            import traceback
            traceback.print_exc()
    
    def update_task(self, index, key, data, text):
        for i in range(self.task_lay.count()):
            w = self.task_lay.itemAt(i).widget()
            if isinstance(w, TaskItem) and w.index == index:
                w.action_key = key
                w.action_data = data
                w.update_display(text)
                break
        
        # Görev güncellendiğinde de progress sıfırlanmalı
        self.reset_progress()
        
    def remove_task(self, index):
        # find and delete
        widget_to_remove = None
        for i in range(self.task_lay.count()):
            w = self.task_lay.itemAt(i).widget()
            if isinstance(w, TaskItem) and w.index == index:
                widget_to_remove = w
                break
        
        if widget_to_remove:
            self.task_lay.removeWidget(widget_to_remove)
            widget_to_remove.deleteLater()
            
            # Re-index remaining tasks
            current_tasks = []
            for i in range(self.task_lay.count() - 1): # Exclude stretch
                widget = self.task_lay.itemAt(i).widget()
                if isinstance(widget, TaskItem):
                    current_tasks.append(widget)
            
            for i, task_item in enumerate(current_tasks):
                task_item.index = i + 1
                task_item.update_display(task_item.lbl.text().split('. ', 1)[1]) # Update label text
        
        QTimer.singleShot(50, self.update_panel_visibility)

    def set_progress(self, current, total, status_msg=""):
        self.lbl_status.setText(f"{current}/{total} Tamamlandı")
        if total > 0:
            val = int((current / total) * 100)
            self.progress.setValue(val)
        
        # Progress bar only appears if there is a task
        if total > 0:
            self.prog_container.show()
            self.sep.show()
        if total > 0 and current >= total:
             self.btn_run_all.setEnabled(False)
             self.btn_run_all.setText("İşlem Tamamlandı")
             # Keep it Blue as requested ("hep mavi olsun")
             self.btn_run_all.setStyleSheet("""
                QPushButton {
                    background-color: #3B82F6; 
                    color: white; 
                    font-weight: bold; 
                    border-radius: 4px; 
                    padding: 6px;
                }
                QPushButton:disabled { background-color: #3B82F6; opacity: 1.0; color: white; }
            """)
            
    def reset_progress(self):
        self.progress.setValue(0)
        self.lbl_status.setText("0/0 Tamamlandı")
        self.prog_container.hide()
        self.sep.hide()
        
        # Reset Button
        self.btn_run_all.setEnabled(True)
        self.btn_run_all.setText(f"{self.get_task_count()} Aksiyonu Başlat")
        self.btn_run_all.setStyleSheet("""
                QPushButton {
                    background-color: #3B82F6;
                    color: white;
                    font-weight: bold;
                    border-radius: 4px;
                    padding: 6px;
                }
                QPushButton:hover { background-color: #2563EB; }
                QPushButton:pressed { background-color: #1D4ED8; }
                QPushButton:disabled { background-color: #3B82F6; opacity: 0.7; color: white; }
            """)

    def update_panel_visibility(self):
        """Aktif görev yoksa paneli tamamen gizle yerine 'Görev yok' placeholder'ı göster"""
        count = self.get_task_count()
        if count == 0:
            self.btn_run_all.setEnabled(False)
            self.btn_run_all.setText(getattr(self, 'tr_no_action', 'Aksiyon Yok'))
            self.btn_run_all.setStyleSheet("""
                QPushButton {
                    background-color: #3B82F6;
                    color: white;
                    font-weight: bold;
                    border-radius: 4px;
                    padding: 6px;
                }
                QPushButton:disabled {
                    background-color: #3B82F6; /* Keep Blue */
                    color: white;
                    opacity: 0.7; /* Dim it slightly */
                }
            """)
            self._no_action_lbl.show()
            self.scroll.hide()
            self.sep.hide()
            self.prog_container.hide()
        else:
            self.reset_progress() # Listede değişiklik olduğunda resetle
            self.btn_run_all.setEnabled(True)
            self.btn_run_all.setText(f"{count} {getattr(self, 'tr_run', 'Aksiyonu Başlat')}")
            # Style is set in reset_progress, but let's ensure it's correct here too if needed
            # reset_progress handles the BLUE style.
            self._no_action_lbl.hide()
            self.scroll.show()
            self.sep.show() # Show separator if tasks are present
            
    def get_task_count(self):
        count = 0
        for i in range(self.task_lay.count()):
            if isinstance(self.task_lay.itemAt(i).widget(), TaskItem):
                count += 1
        return count
        
    def update_texts(self, t):
         if hasattr(self, '_no_action_lbl') and "placeholder_no_actions" in t:
             self._no_action_lbl.setText(t["placeholder_no_actions"])
             self.tr_no_action = t["placeholder_no_actions"]
         
         if "btn_run_actions" in t:
             self.tr_run = t["btn_run_actions"]
         
         if hasattr(self, 'header_lbl') and "active_actions_header" in t:
             self.header_lbl.setText(t["active_actions_header"])
             
         self.update_panel_visibility()

# =============================================================================
# ACTIONS PANEL (MODIFIED - LAYOUT STRETCH REMOVED)
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
        main_lay.setContentsMargins(0, 0, 0, 0)
        main_lay.setSpacing(0)
        
        # 1. BÖLÜM: Butonlar ve Ayarlar (Sol Yarı)
        # ---------------------------------------------------------------------
        self.settings_container = QWidget()
        self.settings_container.setMinimumWidth(400) # Filtre paneli ile AYNI min genişlik
        settings_lay = QHBoxLayout(self.settings_container)
        settings_lay.setContentsMargins(8, 8, 8, 8) # Filtre paneli ile aynı margin
        settings_lay.setSpacing(0)
        settings_lay.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop) # Sola yasla (Tam ekranda kaymayı önler)
        
        self.left_container = QWidget()
        self.left_container.setFixedWidth(160)
        left_lay = QVBoxLayout(self.left_container)
        left_lay.setContentsMargins(0, 0, 8, 0)
        left_lay.setSpacing(4)
        
        lbl_actions = QLabel("Actions")
        lbl_actions.setFixedHeight(24) 
        lbl_actions.setObjectName("SectionHeader")
        left_lay.addWidget(lbl_actions, 0)
        
        self._btn_group = QButtonGroup(self)
        self._btn_group.setExclusive(True)
        self._btn_group.buttonToggled.connect(self._on_group_toggled)
        
        for display, key in self.ACTIONS:
            b = QPushButton(display)
            b.setObjectName("ListBtn")
            b.setCheckable(True)
            b.setMinimumHeight(24)
            b.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            b.setToolTip(self.TOOLTIPS.get(display, ""))
            b.setProperty("action_key", key) # Dil desteği için anahtar
            b.clicked.connect(lambda _, k=key: self.action_clicked.emit(k))
            left_lay.addWidget(b, 1)
            self._btn_group.addButton(b)
            
        settings_lay.addWidget(self.left_container)
        settings_lay.addWidget(GradientLine())
        
        self.settings_panel = ActionSettingsPanel()
        settings_lay.addWidget(self.settings_panel, 1)
        
        main_lay.addWidget(self.settings_container, 1) # Stretch 1
        
        # Ortadaki düşey çizgi (Filtre/Preview ayrımıyla aynı hzada olacak)
        main_lay.addWidget(GradientLine())
        
        # 2. BÖLÜM: Aktif Aksiyonlar (Sağ Yarı)
        # ---------------------------------------------------------------------
        self.active_container = QWidget()
        active_lay = QHBoxLayout(self.active_container)
        active_lay.setContentsMargins(8, 8, 8, 8) # Preview paneli ile aynı margin
        # active_lay.setAlignment... removed to allow expansion
        
        self.active_panel = ActiveActionsPanel()
        active_lay.addWidget(self.active_panel)
        
        main_lay.addWidget(self.active_container, 1) # Stretch 1 (50/50 bölünme)
        
    def _on_group_toggled(self, btn, checked):
        if checked:
            action_key = None
            for display, key in self.ACTIONS:
                if display == btn.text():
                    action_key = key
                    break
            if action_key:
                self.settings_panel.show_form(action_key, btn.text())

    def reset_selection(self):
        for b in self._btn_group.buttons():
            b.setChecked(False)

    def update_texts(self, t):
        """Aksiyon butonlarının metinlerini güncelle"""
        for b in self._btn_group.buttons():
            key = b.property("action_key")
            # Dictionary key format: "action_<key>"
            dict_key = f"action_{key}"
            if key and dict_key in t:
                b.setText(t[dict_key])

# =============================================================================
# PREVIEW PANEL (MODIFIED - FILE LIST WITH FILTERING)
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
        self._mode = "file_list"  # file_list, file_preview, action
        self._action_pages = {}
        self._root_path = None
        self._active_filters = {}  # {filter_id: filter_data}
        self._all_files = []  # Tüm dosyalar
        self._filtered_files = []  # Filtrelenmiş dosyalar
        self._is_refreshing = False  # Concurrent refresh prevention
        self._build()
    
    def _build(self):
        lay = QVBoxLayout(self)
        lay.setContentsMargins(8, 8, 8, 8)
        lay.setSpacing(5)
        
        # Header with title and count
        header_lay = QHBoxLayout()
        self._title = QLabel("File Preview")
        self._title.setObjectName("SectionHeader")
        header_lay.addWidget(self._title)
        header_lay.addStretch()
        self._count_label = QLabel("")
        self._count_label.setObjectName("PreviewCountLabel")
        self._count_label.setStyleSheet("") # Clear hardcoded style
        header_lay.addWidget(self._count_label)
        lay.addLayout(header_lay)
        
        self._stack = QStackedWidget()
        
        # File List Page (yeni)
        self._file_list_page = self._make_file_list()
        self._stack.addWidget(self._file_list_page)
        
        # File Preview Page (mevcut)
        self._preview_page = self._make_preview()
        self._stack.addWidget(self._preview_page)
        
        # Action Pages
        for key, name in self.ACTION_NAMES.items():
            page = self._make_action(key, name)
            self._action_pages[key] = page
            self._stack.addWidget(page)
        
        lay.addWidget(self._stack, 1)
    
    def _make_file_list(self):
        """Dosya listesi sayfası oluştur"""
        w = QWidget()
        w.setStyleSheet("background: transparent;")
        lay = QVBoxLayout(w)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(5)
        
        # Görünüm seçeneği
        view_options = QHBoxLayout()
        view_options.setContentsMargins(0, 0, 0, 4)
        self._tree_view_cb = QCheckBox("Klasör Yapısı")
        self._tree_view_cb.setStyleSheet("font-size: 10px; color: #666;")
        self._tree_view_cb.toggled.connect(self._on_view_mode_changed)
        view_options.addWidget(self._tree_view_cb)
        view_options.addStretch()
        lay.addLayout(view_options)
        
        # Placeholder
        self._list_placeholder = QLabel("Klasör seçiniz")
        self._list_placeholder.setObjectName("PlaceholderLabel")
        self._list_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._list_placeholder.setStyleSheet("color: #888; font-size: 11px; background: transparent; border: none;")
        lay.addWidget(self._list_placeholder)
        
        # File list (ScrollArea içinde) - düz liste
        self._file_list_scroll = QScrollArea()
        self._file_list_container = QWidget()
        self._file_list_container.setStyleSheet("background: transparent;")
        self._file_list_scroll.setWidget(self._file_list_container)
        self._file_list_scroll.setWidgetResizable(True)
        self._file_list_scroll.setStyleSheet("QScrollArea { border: none; background: transparent; } QWidget { background: transparent; }")
        self._file_list_scroll.hide()
        
        self._file_list_layout = QVBoxLayout(self._file_list_container)
        self._file_list_layout.setContentsMargins(0, 0, 0, 0)
        self._file_list_layout.setSpacing(2)
        self._file_list_layout.addStretch()
        
        lay.addWidget(self._file_list_scroll, 1)
        
        # TreeView (klasör yapısı)
        self._preview_tree = QTreeView()
        self._preview_tree.setObjectName("PreviewTree")
        self._preview_tree.setHeaderHidden(True)
        self._preview_tree.setIndentation(20)
        self._preview_tree.setAnimated(True)
        self._preview_tree.setMouseTracking(True)
        self._preview_tree.setRootIsDecorated(True)  # Ağaç işaretlerini göster
        self._preview_tree.setUniformRowHeights(True)
        self._preview_tree.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self._preview_tree.doubleClicked.connect(self._on_tree_item_double_clicked)
        self._preview_tree.hide()
        
        self._preview_model = QFileSystemModel()
        # Stabilite için izlemeyi kapat
        self._preview_model.setOption(QFileSystemModel.Option.DontWatchForChanges, False)
        self._preview_icon_provider = IconProvider()
        self._preview_model.setIconProvider(self._preview_icon_provider)
        self._preview_model.setFilter(QDir.Filter.AllDirs | QDir.Filter.Files | QDir.Filter.NoDotAndDotDot)
        self._preview_model.directoryLoaded.connect(self._on_directory_loaded)
        
        # Proxy Model (Filtreleme Katmanı)
        self._proxy_model = PreviewProxyModel()
        self._proxy_model.setSourceModel(self._preview_model)
        
        self._preview_tree.setModel(self._proxy_model)
        for c in range(1, 4): self._preview_tree.setColumnHidden(c, True)
        
        lay.addWidget(self._preview_tree, 1)
        
        # Tarama durumu göstergesi
        self._scanning_label = QLabel("Taranıyor...")
        self._scanning_label.setStyleSheet("background: rgba(0,0,0,150); color: white; padding: 5px; border-radius: 4px;")
        self._scanning_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._scanning_label.hide()
        # Overlay gibi göstermek için layouta eklemiyoruz, resizeEvent ile konumlandıracağız ama şimdilik layoutta
        # Veya basitçe status bar gibi alta ekleyelim
        lay.addWidget(self._scanning_label, 0, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
        
        self._scanner_thread = None
        
        return w
    
    def _on_view_mode_changed(self, is_tree_view: bool):
        """Görünüm modu değiştiğinde çağrılır"""
        if is_tree_view:
            self._file_list_scroll.hide()
            self._list_placeholder.setText("Klasör yapısı yükleniyor...")
            self._list_placeholder.show()
            self._preview_tree.hide()
            
            if self._root_path:
                # Model'in root path'ini ayarla
                self._preview_model.setRootPath(self._root_path)
                self._attempt_set_root_index(0)
            else:
                self._list_placeholder.setText("Klasör seçiniz")
                self._list_placeholder.show()
        else:
            # Liste moduna geç
            self._preview_tree.hide()
            self._list_placeholder.hide()
            self._file_list_scroll.show()
            self._apply_filters()

    def _attempt_set_root_index(self, attempt_count=0):
        """Klasör ağacının kök dizinini ayarlamaya çalışır (Asenkron yükleme için tekrar dener)"""
        if not self._root_path or not self._tree_view_cb.isChecked():
            return

        idx = self._preview_model.index(self._root_path)
        if idx.isValid():
            proxy_idx = self._proxy_model.mapFromSource(idx)
            if proxy_idx.isValid():
                self._preview_tree.setRootIndex(proxy_idx)
                self._preview_tree.show()
                self._list_placeholder.hide()
                # Başarılı olduğunda recursive genişletmeyi başlat
                self._recursive_expand(proxy_idx)
                return

        # Başarısızsa tekrar dene (Maksimum 20 deneme - 2 saniye)
        if attempt_count < 20:
            QTimer.singleShot(100, lambda: self._attempt_set_root_index(attempt_count + 1))
        else:
            # Hala başarısızsa (zaman aşımı)
            self._list_placeholder.setText("Klasör yapısı yüklenemedi (Zaman aşımı)")
            
    def update_texts(self, t):
        if hasattr(self, '_list_placeholder') and "placeholder_select_folder" in t:
             # Eğer şu an "Klasör seçiniz" yazıyorsa güncelle, başka bir şey yazıyorsa (Scanning vb) dokunma
             # Basitçe her zaman güncellemek yerine state kontrolü yapılabilir ama şimdilik çevirelim
             # Varsayılan metin ise güncelle
             if "Klasör" in self._list_placeholder.text() or "Select" in self._list_placeholder.text() or "seçiniz" in self._list_placeholder.text():
                 self._list_placeholder.setText(t["placeholder_select_folder"])
    
    def _recursive_expand(self, index):
        """Dizini ve tüm alt dizinleri recursive olarak genişletir"""
        if not index.isValid():
            return
            
        self._preview_tree.expand(index)
        source_idx = self._proxy_model.mapToSource(index)
        
        # Daha fazla veri çekilebiliyorsa çek (Lazy loading'i tetikler)
        if self._preview_model.canFetchMore(source_idx):
            self._preview_model.fetchMore(source_idx)
            
        rows = self._proxy_model.rowCount(index)
        for i in range(rows):
            child_idx = self._proxy_model.index(i, 0, index)
            self._recursive_expand(child_idx)

    def _on_directory_loaded(self, path):
        """Klasör yüklendiğinde otomatik olarak genişlet"""
        if self._tree_view_cb.isChecked() and self._preview_tree.isVisible():
            source_index = self._preview_model.index(path)
            proxy_index = self._proxy_model.mapFromSource(source_index)
            if proxy_index.isValid():
                self._recursive_expand(proxy_index)

    def _on_tree_item_double_clicked(self, index):
        """Klasör çift tıklandığında alt klasörleri yükle"""
        if index.isValid():
            source_idx = self._proxy_model.mapToSource(index)
            if self._preview_model.isDir(source_idx):
                if self._preview_model.canFetchMore(source_idx):
                    self._preview_model.fetchMore(source_idx)
    
    def _apply_tree_filter(self):
        """TreeView için filtre uygula (basit isim filtreleri)"""
        # TreeView filtresi için name filter kullan
        if self._active_filters:
            patterns = []
            for filter_data in self._active_filters.values():
                if filter_data.get("type") == "Uzantı":
                    for ext in filter_data.get("extensions", []):
                        patterns.append(f"*.{ext}")
            
            if patterns:
                self._preview_model.setNameFilters(patterns)
                self._preview_model.setNameFilterDisables(False)
            else:
                self._preview_model.setNameFilters([])
        else:
            self._preview_model.setNameFilters([])

    def set_icon_color(self, color):
        """İkon sağlayıcı rengini güncelle"""
        # Yeni provider oluşturarak cache sorununu aş
        new_provider = IconProvider()
        new_provider.set_color(color)
        self._preview_model.setIconProvider(new_provider)
        self._preview_icon_provider = new_provider
        
        # Görünümü zorla yenile
        self._preview_tree.viewport().update()

    def reload_directory(self):
        """Dizini zorla yenile (Hem Tree hem Flat view)"""
        if self._root_path:
             # 1. Ağaç yapısını (QFileSystemModel) zorla yenile
             self._preview_model.setRootPath("")
             self._preview_model.setRootPath(self._root_path)
             
             # 2. Flat listeyi yenile (set_root_path taramayı başlatır)
             # Eğer set_root_path aynı yol ise işlem yapmıyorsa, _start_scan'ı bulmamız lazım.
             # Ancak genellikle set_root_path taramayı başlatır.
             self.set_root_path(self._root_path)
    
    def _on_scan_finished(self, whitelist_dirs, matched_files):
        """Tarama bittiğinde çağrılır"""
        self._scanning_label.hide()
        if hasattr(self, '_proxy_model'):
            # Whitelist'i güncelle (Sadece bu klasörler görünecek)
            self._proxy_model.set_whitelist(whitelist_dirs)
            
            # Ağacı genişletmeye başla (Kökten itibaren)
            if self._root_path:
                # Kök dizinin kendisi whitelistte olmayabilir (files.walk root'u dahil etmeyebilir bazen)
                # Ama root'tan fetchMore başlatmalıyız.
                root_idx = self._preview_model.index(self._root_path)
                if self._preview_model.canFetchMore(root_idx):
                    self._preview_model.fetchMore(root_idx)
                
                # Root zaten yüklüyse _on_directory_loaded tetiklenmez, manuel tetikle
                self._on_directory_loaded(self._root_path)
    
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
            w._start = ModernSpinBox()
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
            w._passes = ModernSpinBox()
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
        cancel.clicked.connect(self.show_file_list)
        btns.addWidget(cancel)
        btns.addStretch()
        exe = QPushButton("Run")
        exe.setFixedWidth(40)
        exe.clicked.connect(lambda: self.exec_action.emit(key, {}))
        btns.addWidget(exe)
        lay.addLayout(btns)
        return w
    
    def set_root_path(self, path: str):
        """Kaynak klasörü ayarla ve dosyaları listele"""
        # Yolu normalize et (Windows ters/düz çizgi farkını gider)
        import os
        path = os.path.normpath(path)
        
        # Prevent concurrent refresh
        if self._is_refreshing:
            print("DEBUG: Skipping set_root_path - already refreshing")
            return
            
        self._is_refreshing = True
        print(f"DEBUG: set_root_path called with {path}")
        
        try:
            # Aynı yol olsa bile - aynı yolu tekrar yüklemiyoruz (performans + stabilite)
            if hasattr(self, '_preview_model') and self._root_path:
                current_norm = os.path.normpath(self._root_path)
                if path == current_norm:
                    print("DEBUG: Same path (normalized), skipping reload")
                    self._is_refreshing = False
                    return
                 
            self._root_path = path

            # TreeView modeli için kök dizini ayarla
            if hasattr(self, '_preview_model'):
                self._preview_model.setRootPath(path)
                
            # Eğer ağaç görünümü aktifse, görünümü güncellemeye başla
            if hasattr(self, '_tree_view_cb') and self._tree_view_cb.isChecked():
                self._preview_tree.hide()
                self._list_placeholder.setText("Klasör taranıyor...")
                self._list_placeholder.show()
                self._attempt_set_root_index(0)
                
            self._scan_files()
            self._apply_filters()
            self.show_file_list()
            print("DEBUG: set_root_path complete")
        except Exception as e:
            print(f"ERROR in set_root_path: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self._is_refreshing = False

    def reload_directory(self):
        """Dizini ve listeyi güvenli biçimde yenile"""
        if self._is_refreshing:
            return
            
        self._is_refreshing = True
        # Modeli tamamen sıfırlamak (setRootPath("")) yerine
        # sadece taramayı ve arayüzü güncelleyeceğiz.
        # QFileSystemModel zaten dosya sistemi değişikliklerini otomatik algılar.
        QTimer.singleShot(200, self._do_reload_safe)
    
    def _do_reload_safe(self):
        """Yenilemeyi tamamla"""
        try:
            # 1. Dosya listesini yeniden tara (glob)
            self._scan_files()
            
            # 2. Sayacı güncelle
            if hasattr(self, '_count_label'):
                self._count_label.setText(f"{len(self._all_files)} Öğe")
            
            # 3. Filtreleri tekrar uygula
            self._apply_filters()
            
            # 4. Eğer TreeView açıksan kök dizini tazele (Resetlemeden)
            if hasattr(self, '_tree_view_cb') and self._tree_view_cb.isChecked():
                if self._root_path:
                    # Mevcut root path'i tekrar set etmek (eğer değişmediyse) bazen
                    # QFileSystemModel'i tetiklemez.
                    # Bu noktada en güvenli yöntem path'i korumaktır.
                    # QFileSystemModel arka planda watcher ile çalışır.
                    # Eğer watcher çalışmıyorsa (ki devre dışı bırakmış olabiliriz),
                    # Onu tekrar aktif etmemiz gerekebilir.
                    pass 
            else:
                # Liste görünümünü güncelle
                self.show_file_list()
                
        except Exception as e:
            print(f"_do_reload_safe error: {e}")
        finally:
            self._is_refreshing = False
    
    def _scan_files(self):
        """Kaynak klasördeki tüm dosyaları tara"""
        self._all_files = []
        if not self._root_path:
            return
        
        try:
            root = Path(self._root_path)
            if root.exists() and root.is_dir():
                # Recursive olarak tüm dosyaları bul
                for file_path in root.rglob("*"):
                    if file_path.is_file():
                        self._all_files.append(file_path)
        except Exception as e:
            print(f"Scan error: {e}")
    
    def add_filter(self, filter_id: str, filter_data: dict):
        """Filtre ekle ve listeyi güncelle"""
        self._active_filters[filter_id] = filter_data
        self._apply_filters()
    
    def remove_filter(self, filter_id: str):
        """Filtre kaldır ve listeyi güncelle"""
        if filter_id in self._active_filters:
            del self._active_filters[filter_id]
        self._apply_filters()
    
    def clear_filters(self):
        """Tüm filtreleri temizle"""
        self._active_filters.clear()
        self._apply_filters()
    
    def _apply_filters(self):
        """Aktif filtreleri uygula ve dosya listesini güncelle"""
        if not self._all_files:
            self._filtered_files = []
        elif not self._active_filters:
            # Filtre yoksa boş liste (Kullanıcı isteği)
            self._filtered_files = []
        else:
            # Filtreleri uygula (AND mantığı)
            self._filtered_files = []
            for file_path in self._all_files:
                if self._file_matches_filters(file_path):
                    self._filtered_files.append(file_path)
        
        if hasattr(self, '_proxy_model'):
            # Filtre verilerini güncelle (Model invalidate edilir - proxymodel.py içinde)
            self._proxy_model.set_filters(self._active_filters)
            
            # Scanner'ı şimdilik devre dışı bırakıyoruz (Native filter hızı test ediliyor)
            # self._scanning_label.show() ... (Removed for stability)
            self._scanning_label.hide()
            self._proxy_model.set_whitelist(None)

            # ÖNEMLİ: TreeView modundayken root index'i MUTLAKA ayarla (C: diskini engelle)
            if self._tree_view_cb.isChecked() and self._root_path:
                if self._preview_model.rootPath() != self._root_path:
                    self._preview_model.setRootPath(self._root_path)
                
                source_root = self._preview_model.index(self._root_path)
                proxy_root = self._proxy_model.mapFromSource(source_root)
                
                if proxy_root.isValid():
                    self._preview_tree.setRootIndex(proxy_root)
                    # Her durumda recursive expand yap (Filtre olsun olmasın)
                    QTimer.singleShot(50, lambda: self._recursive_expand(proxy_root))
                else:
                    self._attempt_set_root_index(0)

        self._update_file_list_ui()
    
    def _file_matches_filters(self, file_path: Path) -> bool:
        """Dosyanın filtrelere uyup uymadığını kontrol et
        
        Uzantı filtreleri: OR mantığı (herhangi birine uyması yeterli)
        Diğer filtreler: AND mantığı (hepsine uyması gerekli)
        """
        # Filtreleri türlerine göre grupla
        extension_filters = []
        other_filters = []
        
        for filter_data in self._active_filters.values():
            if filter_data.get("type") == "Uzantı":
                extension_filters.append(filter_data)
            else:
                other_filters.append(filter_data)
        
        # Uzantı filtresi varsa, en az birine uymalı (OR)
        if extension_filters:
            ext_match = False
            for filter_data in extension_filters:
                if self._file_matches_single_filter(file_path, filter_data):
                    ext_match = True
                    break
            if not ext_match:
                return False
        
        # Diğer filtreler için hepsine uymalı (AND)
        for filter_data in other_filters:
            if not self._file_matches_single_filter(file_path, filter_data):
                return False
        
        return True
    
    def _file_matches_single_filter(self, file_path: Path, filter_data: dict) -> bool:
        """Dosyanın tek bir filtreye uyup uymadığını kontrol et"""
        filter_type = filter_data.get("type", "")
        
        try:
            if filter_type == "Uzantı":
                extensions = filter_data.get("extensions", [])
                file_ext = file_path.suffix.lstrip('.').lower()
                return file_ext in extensions
            
            elif filter_type == "Dosya Adı":
                text = filter_data.get("text", "")
                case_sensitive = filter_data.get("case_sensitive", False)
                exact_match = filter_data.get("exact_match", False)
                invert = filter_data.get("invert", False)
                
                file_name = file_path.stem  # Uzantısız dosya adı
                
                if not case_sensitive:
                    file_name = file_name.lower()
                    text = text.lower()
                
                if exact_match:
                    match = file_name == text
                else:
                    match = text in file_name
                
                return not match if invert else match
            
            elif filter_type == "Boyut":
                op = filter_data.get("op", ">")
                value = filter_data.get("value", 0)
                unit = filter_data.get("unit", "MB")
                
                # Byte'a çevir
                multipliers = {"Byte": 1, "KB": 1024, "MB": 1024*1024, "GB": 1024*1024*1024}
                target_size = value * multipliers.get(unit, 1)
                
                file_size = file_path.stat().st_size
                
                if op == ">":
                    return file_size > target_size
                elif op == "<":
                    return file_size < target_size
                else:  # =
                    return file_size == target_size
            
            elif filter_type == "Boş Dosya":
                return file_path.stat().st_size == 0
            
            elif filter_type == "Regex":
                from workers import safe_regex_search
                pattern = filter_data.get("pattern", "")
                result = safe_regex_search(pattern, file_path.name, timeout=1.0)
                if result[0] == 'success':
                    return len(result[1]) > 0
                return False  # timeout veya hata durumunda
            
            elif filter_type == "Metin":
                # Dosya içeriğinde metin ara (Generator ile RAM-efficient)
                from workers import file_contains_text
                text = filter_data.get("text", "")
                case_sensitive = filter_data.get("case_sensitive", False)
                return file_contains_text(file_path, text, case_sensitive)
            
            elif filter_type == "Metin Yok":
                from workers import file_contains_text
                text = filter_data.get("text", "")
                return not file_contains_text(file_path, text, case_sensitive=False)
            
            elif filter_type == "Oluşturma Tarihi":
                start = filter_data.get("start", "")
                end = filter_data.get("end", "")
                ctime = datetime.fromtimestamp(file_path.stat().st_ctime)
                ctime_str = ctime.strftime("%Y-%m-%d")
                return start <= ctime_str <= end
            
            elif filter_type == "Değişiklik Tarihi":
                start = filter_data.get("start", "")
                end = filter_data.get("end", "")
                mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                mtime_str = mtime.strftime("%Y-%m-%d")
                return start <= mtime_str <= end
            
            elif filter_type == "Gizli":
                # Windows gizli dosya kontrolü
                import ctypes
                attrs = ctypes.windll.kernel32.GetFileAttributesW(str(file_path))
                return attrs != -1 and (attrs & 2)  # FILE_ATTRIBUTE_HIDDEN
            
            elif filter_type == "Şifreli":
                # Basit şifreleme kontrolü (genellikle uzantıya bakılır)
                encrypted_exts = ['.enc', '.encrypted', '.gpg', '.pgp', '.aes']
                return file_path.suffix.lower() in encrypted_exts
            
        except Exception as e:
            print(f"Filter error: {e}")
            return False
        
        return True
    
    def _update_file_list_ui(self):
        """Dosya listesi UI'ını güncelle"""
        # TreeView modundaysak sadece sayıyı güncelle ve çık
        if hasattr(self, '_tree_view_cb') and self._tree_view_cb.isChecked():
            # Dosya sayısını güncelle (Kullanıcının filtrenin çalıştığını anlaması için)
            if self._root_path:
                count = len(self._filtered_files)
                total = len(self._all_files)
                self._count_label.setText(f"{count} / {total} dosya")
            else:
                self._count_label.setText("")
            return
        
        # Mevcut öğeleri temizle
        while self._file_list_layout.count() > 1:  # stretch hariç
            item = self._file_list_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        if not self._root_path:
            self._list_placeholder.setText("Klasör seçiniz")
            self._list_placeholder.show()
            self._file_list_scroll.hide()
            self._count_label.setText("")
            return
        
        if not self._filtered_files:
            if self._active_filters:
                self._list_placeholder.setText("Filtreye uygun dosya bulunamadı")
            else:
                self._list_placeholder.setText("Bu klasörde dosya yok")
            self._list_placeholder.show()
            self._file_list_scroll.hide()
            self._count_label.setText(f"0 / {len(self._all_files)}")
            return
        
        self._list_placeholder.hide()
        self._file_list_scroll.show()
        
        # Dosya sayısını güncelle
        self._count_label.setText(f"{len(self._filtered_files)} / {len(self._all_files)} dosya")
        
        # Dosyaları listele (maksimum 100 göster performans için)
        display_files = self._filtered_files[:100]
        
        for file_path in display_files:
            item = self._create_file_item(file_path)
            self._file_list_layout.insertWidget(self._file_list_layout.count() - 1, item)
        
        if len(self._filtered_files) > 100:
            more_label = QLabel(f"... ve {len(self._filtered_files) - 100} dosya daha")
            more_label.setStyleSheet("color: #888; font-size: 10px; padding: 4px;")
            self._file_list_layout.insertWidget(self._file_list_layout.count() - 1, more_label)
    
    def _create_file_item(self, file_path: Path) -> QWidget:
        """Dosya liste öğesi oluştur"""
        item = QWidget()
        item.setStyleSheet("""
            QWidget { background: #F5F5F5; border-radius: 3px; padding: 2px; }
            QWidget:hover { background: #EAEAEA; }
        """)
        
        lay = QHBoxLayout(item)
        lay.setContentsMargins(6, 3, 6, 3)
        lay.setSpacing(6)
        
        # İkon
        icon_label = QLabel()
        ext = file_path.suffix.lower()
        if ext in ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.svg', '.webp']:
            icon = QIcon("icons/image-solid.svg")
        elif ext in ['.mp3', '.wav', '.flac', '.m4a', '.ogg']:
            icon = QIcon("icons/music-solid.svg")
        else:
            icon = QIcon("icons/file-lines-solid.svg")
        icon_label.setPixmap(icon.pixmap(14, 14))
        lay.addWidget(icon_label)
        
        # Dosya adı
        name_label = QLabel(file_path.name)
        name_label.setStyleSheet("font-size: 10px; color: #333;")
        name_label.setToolTip(str(file_path))
        lay.addWidget(name_label, 1)
        
        # Boyut
        try:
            size = file_path.stat().st_size
            size_text = self._format_size(size)
            size_label = QLabel(size_text)
            size_label.setStyleSheet("font-size: 9px; color: #888;")
            lay.addWidget(size_label)
        except:
            pass
        
        return item
    
    def _format_size(self, size: int) -> str:
        """Boyutu okunabilir formata çevir"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.0f} {unit}"
            size /= 1024
        return f"{size:.0f} TB"
    
    def show_file_list(self):
        """Dosya listesi görünümünü göster"""
        self._mode = "file_list"
        self._title.setText("File Preview")
        self._stack.setCurrentIndex(0)
    
    def show_preview(self):
        self._mode = "file_preview"
        self._title.setText("File Preview")
        self._stack.setCurrentIndex(1)
    
    def show_action(self, key):
        if key in self._action_pages:
            self._mode = "action"
            self._title.setText(self.ACTION_NAMES.get(key, key))
            idx = list(self._action_pages.keys()).index(key) + 2  # file_list ve preview sonra
            self._stack.setCurrentIndex(idx)
    
    def update_file_preview(self, path: str):
        if self._mode not in ["file_preview"]:
            # Dosya listesi modundayken seçim değişikliğini görmezden gel
            return
        try:
            p = Path(path)
            if not p.exists():
                self._show_placeholder("Not found")
                return
            self._placeholder.hide()
            self._info.show()
            self._f_name.setText(p.name)
            if p.is_dir():
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
                        # Sadece 500 karakter oku - tüm dosyayı yüklemeden
                        with open(p, 'r', encoding='utf-8', errors='ignore') as f:
                            self._text.setText(f.read(500))
                        self._text.show()
                    except: self._text.hide()
                else: self._text.hide()
            self._f_path.setText(str(p))
        except Exception as e:
            self._show_placeholder(f"Error")
    
    def _show_placeholder(self, text: str):
        self._info.hide()
        self._placeholder.setText(text)
        self._placeholder.show()

# =============================================================================
# MAIN WINDOW
# =============================================================================

class MainWindow(QMainWindow):
    # ==========================================================================
    # PANEL BOYUT AYARLARI
    # Source: Sol panel (klasör ağacı) - sola doğru genişletildi
    # Filters: Orta panel (filtre ayarları) - sabit boyut
    # Preview: Sağ panel (dosya önizleme) - sağa doğru genişletildi
    # ==========================================================================
    SOURCE_MIN = 300      # Source panel minimum genişlik (sola doğru genişletildi)
    FILTERS_MIN = 400     # Filters panel minimum genişlik (sabit)
    PREVIEW_MIN = 10
         # Preview panel minimum genişlik (sağa doğru genişletildi)
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File-Architect-Pro")
        self.resize(1300, 700)        # Ana pencere genişliği %30 artırıldı (1000 → 1300)
        self.setMinimumSize(1040, 500)  # Minimum genişlik de %30 artırıldı (800 → 1040)
        self._editing_task_index = None # Düzenlenmekte olan görev indeksi
        self._current_lang = "tr"  # Varsayılan dil
        self._translations = {}  # Çeviri sözlüğü cache
        self._init_translations()  # Çeviri sözlüğünü başlat
        self._build()
        self._connect()
    
    def _build(self):
        central = QWidget()
        self.setCentralWidget(central)
        outer = QVBoxLayout(central)
        outer.setContentsMargins(12, 12, 12, 12)
        outer.setSpacing(0)
        grid = QGridLayout()
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setHorizontalSpacing(10)
        grid.setVerticalSpacing(10)
        
        self._source = SourcePanel()
        self._source.setMinimumWidth(self.SOURCE_MIN)
        grid.addWidget(self._source, 0, 0, 2, 1)
        
        self._filters = FiltersPanel()
        self._filters.setMinimumWidth(self.FILTERS_MIN)
        grid.addWidget(self._filters, 0, 1)
        
        self._preview = PreviewPanel()
        self._preview.setMinimumWidth(self.PREVIEW_MIN + 60) 
        grid.addWidget(self._preview, 0, 2)
        
        self._actions = ActionsPanel()
        grid.addWidget(self._actions, 1, 1, 1, 2) # İki kolonu birden kapla
        
        # Genişlik oranları: 1 (Source) : 2 (Filters) : 2 (Preview)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 2)
        grid.setColumnStretch(2, 2)
        grid.setRowStretch(0, 3)
        grid.setRowStretch(1, 9)
        
        outer.addLayout(grid)
    
    def _connect(self):
        # Source panel bağlantıları
        self._source.dir_selected.connect(self._on_dir_selected)
        self._source.selection_changed.connect(self._preview.update_file_preview)
        self._source.delete_requested.connect(self._on_del)
        
        # Filtre paneli bağlantıları
        filter_settings = self._filters.settings_panel
        filter_settings.filter_added.connect(self._on_filter_added)
        filter_settings.filter_removed.connect(self._on_filter_removed)
        
        # Aksiyon paneli bağlantıları
        self._actions.action_clicked.connect(self._on_action)
        self._actions.settings_panel.action_requested.connect(self._on_action_requested)
        self._actions.active_panel.run_requested.connect(self._on_run_active_actions)
        self._actions.active_panel.edit_requested.connect(self._on_task_edit)
        # Theme Signal
        # Theme Signal
        self._source.settings_tab.theme_changed.connect(self._on_theme_changed)
        self._source.settings_tab.language_changed.connect(self._on_language_changed)

    def _on_language_changed(self, lang_code):
        """Dil değişikliğini uygula"""
        self._current_lang = lang_code
        set_language(lang_code)  # Global çevirileri güncelle
        self._init_translations()  # Lokal çevirileri güncelle
        self._update_ui_text()

    def _init_translations(self):
        """Çeviri sözlüğünü başlat"""
        if self._current_lang == "tr":
            self._translations = {
                # QMessageBox Başlıkları
                "msg_title_info": "Bilgi",
                "msg_title_warning": "Uyarı",
                "msg_title_error": "Hata",
                "msg_title_success": "Başarılı",
                "msg_title_confirm": "Onay",
                "msg_title_hide": "Gizle",
                "msg_title_delete_confirm": "Silme Onayı",
                "msg_title_security_warning": "Güvenlik Uyarısı",
                "msg_title_operation_forbidden": "İşlem Yasaklandı",
                "msg_title_invalid_extension": "Hatalı Uzantı",
                "msg_title_completed_with_errors": "İşlem Tamamlandı (Hatalı)",
                
                # QMessageBox Mesajları
                "msg_settings_applied": "Ayarlar başarıyla uygulandı!",
                "msg_select_filter_first": "Lütfen önce soldan bir filtre tipi seçiniz!",
                "msg_max_filters": "En fazla {0} filtre ekleyebilirsiniz!",
                "msg_filter_exists": "Bu filtre zaten eklenmiş!\n\n{0}",
                "msg_extension_empty": "Uzantı boş olamaz!",
                "msg_no_valid_extension": "Geçerli uzantı bulunamadı!",
                "msg_invalid_regex": "Geçersiz regex deseni!",
                "msg_pattern_empty": "Desen boş olamaz!",
                "msg_search_text_empty": "Aranacak metin boş olamaz!",
                "msg_target_folder_empty": "Hedef klasör seçilmedi!",
                "msg_output_path_empty": "Çıktı yolu giriniz!",
                "msg_max_actions": "En fazla 3 aksiyon eklenebilir!",
                "msg_no_files_to_process": "İşlem yapılacak dosya bulunamadı!",
                "msg_no_files": "İşlenecek dosya yok!",
                "msg_all_operations_success": "Tüm işlemler başarıyla tamamlandı.",
                "msg_some_operations_failed": "Bazı işlemler başarısız oldu:\n{0}",
                "msg_and_more_errors": "\n... ve {0} hata daha.",
                "msg_file_in_use": "Dosya kullanımda veya izin yok:\n{0}",
                "msg_delete_failed": "Silinemedi:\n{0}",
                "msg_security_delete_disabled": "Sol panelden doğrudan silme işlemi, veri kaybını önlemek için devre dışı bırakılmıştır.\nDosyaları silmek için lütfen Aksiyonlar sekmesini veya Dosya Gezgini'ni kullanın.",
                "msg_delete_folder_confirm": "Klasör ve içindeki tüm dosyalar silinecek:\n{0}\n\nDevam etmek istiyor musunuz?",
                "msg_delete_file_confirm": "Dosya silinecek:\n{0}\n\nDevam etmek istiyor musunuz?",
                "msg_root_drive_forbidden": "Kritik Hata: Kök sürücüler (C:\\, D:\\ vb.) üzerinde hiçbir silme veya gizleme işlemi yapılamaz!\n\nBu işlem sistem güvenliği için kalıcı olarak engellenmiştir.",
                "msg_hide_item_confirm": "Bu öğeyi listeden gizlemek istiyor musunuz?\n(Dosya diskten silinmeyecek, sadece bu görünümden kalkacak)\n\n{0}",
                "msg_processing": "İşleniyor...",
                
                # Validasyon Mesajları
                "msg_invalid_empty_extension": "'{0}' geçersiz (boş uzantı)",
                "msg_invalid_double_dot": "'{0}' geçersiz (çift nokta)",
                "msg_invalid_char": "'{0}' geçersiz karakter içeriyor: '{1}'"
            }
        else:  # English
            self._translations = {
                # QMessageBox Titles
                "msg_title_info": "Information",
                "msg_title_warning": "Warning",
                "msg_title_error": "Error",
                "msg_title_success": "Success",
                "msg_title_confirm": "Confirm",
                "msg_title_hide": "Hide",
                "msg_title_delete_confirm": "Delete Confirmation",
                "msg_title_security_warning": "Security Warning",
                "msg_title_operation_forbidden": "Operation Forbidden",
                "msg_title_invalid_extension": "Invalid Extension",
                "msg_title_completed_with_errors": "Completed with Errors",
                
                # QMessageBox Messages
                "msg_settings_applied": "Settings applied successfully!",
                "msg_select_filter_first": "Please select a filter type from the left first!",
                "msg_max_filters": "You can add up to {0} filters!",
                "msg_filter_exists": "This filter already exists!\n\n{0}",
                "msg_extension_empty": "Extension cannot be empty!",
                "msg_no_valid_extension": "No valid extension found!",
                "msg_invalid_regex": "Invalid regex pattern!",
                "msg_pattern_empty": "Pattern cannot be empty!",
                "msg_search_text_empty": "Search text cannot be empty!",
                "msg_target_folder_empty": "Target folder not selected!",
                "msg_output_path_empty": "Please enter an output path!",
                "msg_max_actions": "Maximum 3 actions can be added!",
                "msg_no_files_to_process": "No files found to process!",
                "msg_no_files": "No files to process!",
                "msg_all_operations_success": "All operations completed successfully.",
                "msg_some_operations_failed": "Some operations failed:\n{0}",
                "msg_and_more_errors": "\n... and {0} more errors.",
                "msg_file_in_use": "File is in use or permission denied:\n{0}",
                "msg_delete_failed": "Could not delete:\n{0}",
                "msg_security_delete_disabled": "Direct deletion from the left panel is disabled to prevent data loss.\nTo delete files, please use the Actions tab or File Explorer.",
                "msg_delete_folder_confirm": "The folder and all its contents will be deleted:\n{0}\n\nDo you want to continue?",
                "msg_delete_file_confirm": "The file will be deleted:\n{0}\n\nDo you want to continue?",
                "msg_root_drive_forbidden": "Critical Error: No delete or hide operations can be performed on root drives (C:\\, D:\\ etc.)!\n\nThis operation is permanently blocked for system security.",
                "msg_hide_item_confirm": "Do you want to hide this item from the list?\n(The file won't be deleted from disk, only hidden from this view)\n\n{0}",
                "msg_processing": "Processing...",
                
                # Validation Messages
                "msg_invalid_empty_extension": "'{0}' is invalid (empty extension)",
                "msg_invalid_double_dot": "'{0}' is invalid (double dot)",
                "msg_invalid_char": "'{0}' contains invalid character: '{1}'"
            }

    def _t(self, key, *args):
        """Çeviri yardımcı metodu"""
        text = self._translations.get(key, key)
        if args:
            for i, arg in enumerate(args):
                text = text.replace("{" + str(i) + "}", str(arg))
        return text

    def _update_ui_text(self):
        """Arayüz metinlerini güncelle"""
        print(f"DEBUG: Language update started for: {self._current_lang}")
        try:
            tr = {
                "source_tab_files": "Dosyalar", "source_tab_settings": "Ayarlar",
                "source_header": "Kaynak Klasör", "refresh_tooltip": "Yenile",
                "browse": "Gözat", "filter_header": "Filtre Ayarları",
                "filter_add": "Filtre Ekle", "filter_reset": "Sıfırla", "filter_cancel": "İptal",
                "actions_header": "Aksiyonlar", "active_actions": "Aktif Aksiyonlar",
                "preview_header": "Önizleme", "run_actions": "Tümünü Çalıştır",
                "export_excel": "Excel'e Aktar", "folder_structure": "Klasör Yapısı",
                "files_count": "Dosya", "apply_settings": "Ayarları Uygula"
            }
            
            en = {
                "source_tab_files": "Files", "source_tab_settings": "Settings",
                "source_header": "Source Directory", "refresh_tooltip": "Refresh",
                "browse": "Browse", "filter_header": "Filter Settings",
                "filter_add": "Add Filter", "filter_reset": "Reset", "filter_cancel": "Cancel",
                "actions_header": "Actions", "active_actions": "Active Actions",
                "preview_header": "Preview", "run_actions": "Run All Actions",
                "export_excel": "Export to Excel", "folder_structure": "Folder Structure",
                "files_count": "Items", "apply_settings": "Apply Settings"
            }
            
            t = tr if self._current_lang == "tr" else en
            
            # Aksiyon çevirilerini ekle (Dinamik)
            if self._current_lang == "tr":
                t.update({
                    "action_seq_rename": "Sıralı Adlandırma", "action_prefix_suffix": "Ön/Son Ek",
                    "action_find_replace": "Bul/Değiştir", "action_change_ext": "Uzantı Değiştir",
                    "action_copy": "Kopyala", "action_tag": "Etiket", "action_flatten": "Tek Klasör",
                    "action_secure_del": "Güvenli Sil", "action_merge": "Metin Birleştir",
                    "action_csv": "CSV Rapor", "action_excel": "Excel Rapor",
                    # Filters
                    "filter_panel_header": "Filtreler",
                    "filter_Uzantı": "Uzantı", "filter_Dosya Adı": "Dosya Adı", "filter_Metin": "Metin",
                    "filter_Metin Yok": "Metin Yok", "filter_Boyut": "Boyut", "filter_Regex": "Regex",
                    "filter_Boş Dosya": "Boş Dosya", "filter_Oluşturma Tarihi": "Oluşturma Tarihi",
                    "filter_Değişiklik Tarihi": "Değişiklik Tarihi", "filter_Şifreli": "Şifreli", "filter_Gizli": "Gizli",
                    # App Settings & Placeholders
                    "app_settings": "Uygulama Ayarları",
                    "theme_label": "Görünüm Teması:",
                    "lang_label": "Dil (Language):",
                    "apply_settings": "Ayarları Uygula",
                    "placeholder_select_filter": "Soldan bir filtre seçiniz.",
                    "label_active_filters": "Aktif Filtreler",
                    "placeholder_select_action": "Soldan bir aksiyon seçiniz.",
                    "placeholder_no_actions": "Aksiyon Yok",
                    "placeholder_select_folder": "Lütfen bir klasör seçin",
                    "no_folder_selected": "Klasör seçilmedi",
                    "btn_run_actions": "Aksiyonu Başlat",
                    "action_settings_header": "Aksiyon Ayarları",
                    "active_actions_header": "Aktif Aksiyonlar",
                    "theme_items": ["Açık (Light)", "Koyu (Dark)", "Sistem"]
                })
            else:
                t.update({
                    "action_seq_rename": "Sequential Rename", "action_prefix_suffix": "Prefix/Suffix",
                    "action_find_replace": "Find/Replace", "action_change_ext": "Change Extension",
                    "action_copy": "Copy", "action_tag": "Tag", "action_flatten": "Flatten Folder",
                    "action_secure_del": "Secure Delete", "action_merge": "Merge Text",
                    "action_csv": "CSV Report", "action_excel": "Excel Report",
                    # Filters
                    "filter_panel_header": "Filters",
                    "filter_Uzantı": "Extension", "filter_Dosya Adı": "Filename", "filter_Metin": "Text Content",
                    "filter_Metin Yok": "No Text", "filter_Boyut": "Size", "filter_Regex": "Regex",
                    "filter_Boş Dosya": "Empty File", "filter_Oluşturma Tarihi": "Created Date",
                    "filter_Değişiklik Tarihi": "Modified Date", "filter_Şifreli": "Encrypted", "filter_Gizli": "Hidden",
                    # App Settings & Placeholders
                    "app_settings": "Application Settings",
                    "theme_label": "Appearance Theme:",
                    "lang_label": "Language:",
                    "apply_settings": "Apply Settings",
                    "placeholder_select_filter": "Select a filter from the left.",
                    "label_active_filters": "Active Filters",
                    "placeholder_select_action": "Select an action from the left.",
                    "placeholder_no_actions": "No Actions",
                    "placeholder_select_folder": "Please select a folder",
                    "no_folder_selected": "No folder selected",
                    "btn_run_actions": "Start Actions",
                    "action_settings_header": "Action Settings",
                    "active_actions_header": "Active Actions",
                    "theme_items": ["Light", "Dark", "System"]
                })
            
            # Source Panel
            self._source.tabs.setTabText(0, t["source_tab_files"])
            self._source.tabs.setTabText(1, t["source_tab_settings"])
            source_lbl = self._source.findChild(QLabel, "SectionHeader")
            if source_lbl: source_lbl.setText(t["source_header"])
            self._source.btn_browse.setText(t["browse"])
            # App Settings Update
            if hasattr(self._source.settings_tab, 'update_texts'):
                 self._source.settings_tab.update_texts(t)
            # SourcePanel Update (Placeholder, PathLabel)
            if hasattr(self._source, 'update_texts'):
                 self._source.update_texts(t)
            print("DEBUG: Source Panel updated")
            
            # Filters Panel (List & Settings)
            if hasattr(self._filters, 'update_texts'):
                self._filters.update_texts(t)
            
            if hasattr(self._filters.settings_panel, 'update_texts'):
                self._filters.settings_panel.update_texts(t)
            
            self._filters.settings_panel.header_lbl.setText(t["filter_header"])
            self._filters.settings_panel.btn_add.setText(t["filter_add"])
            self._filters.settings_panel.btn_reset.setText(t["filter_reset"])
            self._filters.settings_panel.btn_cancel.setText(t["filter_cancel"])
            print("DEBUG: Filters Panel updated")
            
            # Action Settings Buttons
            if hasattr(self._actions, 'settings_panel'):
                if hasattr(self._actions.settings_panel, 'update_texts'):
                     self._actions.settings_panel.update_texts(t)
                
                self._actions.settings_panel.btn_apply.setText(t["apply_settings"])
                self._actions.settings_panel.btn_reset.setText(t["filter_reset"])
                self._actions.settings_panel.btn_cancel.setText(t["filter_cancel"])
            
            # Aksiyon Butonlarını Güncelle
            if hasattr(self._actions, 'update_texts'):
                self._actions.update_texts(t)
            
            # Active Actions Panel Update
            if hasattr(self._actions.active_panel, 'update_texts'):
                 self._actions.active_panel.update_texts(t)

            # Preview Panel Update
            if hasattr(self._preview, 'update_texts'):
                 self._preview.update_texts(t)
            
            # Actions Panel Header (Actions / Aksiyonlar)
            # findChildren bazen alt widgetların derinliklerine inemeyebilir veya SectionHeader ismi benzersiz olmayabilir
            # Doğrudan ActionsPanel üzerindeki header'ı bulmaya çalışalım (Sol taraftaki)
            
            # 1. Ana Başlık (Actions)
            main_headers = self._actions.findChildren(QLabel, "SectionHeader")
            for h in main_headers:
                # Ebeveyni ActiveActionsPanel olmamalı
                if h.parent() != self._actions.active_panel and "ActiveActionsPanel" not in str(h.parent()):
                     txt = h.text()
                     if txt in ["Aksiyonlar", "Actions"]:
                        h.setText(t["actions_header"])

            # 2. Aktif Panel Başlığı (Active Actions)
            # ActivePanel içinden doğrudan arayalım
            active_header = self._actions.active_panel.findChild(QLabel, "SectionHeader")
            if active_header:
                active_header.setText(t["active_actions"])
            
            # Run Button (btn_run -> btn_run_all)
            count = self._actions.active_panel.get_task_count()
            # Değişken adı btn_run_all
            btn = self._actions.active_panel.btn_run_all
            
            if count > 0:
                text = f"{count} Aksiyonu Başlat" if self._current_lang == "tr" else f"Start {count} Actions"
                btn.setText(text)
            else:
                text = "Aksiyon Yok" if self._current_lang == "tr" else "No Actions"
                btn.setText(text)
            print("DEBUG: Run Button updated")
            
            # Preview Panel
            preview_lbl = self._preview.findChild(QLabel, "SectionHeader")
            if preview_lbl: preview_lbl.setText(t["preview_header"])
            # self._preview.btn_export.setText(t["export_excel"]) # Removed
            self._preview._tree_view_cb.setText(t["folder_structure"])
            print("DEBUG: Preview Panel updated")
            
        except Exception as e:
            print(f"ERROR in language update: {e}")
            import traceback
            traceback.print_exc()


    def _on_theme_changed(self, theme):
        app = QApplication.instance()
        
        if theme == "light":
             # 1. Icons Reset (Dark Color)
             self._source._icons.set_color("#444444")
             self._source._delegate.set_color("#444444")
             
             # 2. Styles
             app.setStyle("Fusion")
             app.setStyleSheet(STYLE_SHEET + """
                QMainWindow { background-color: #F9F8F2; }
                QLabel { color: #333; }
             """)
             
        elif theme == "dark":
             # 1. Icons White (Pure White)
             self._source.set_icon_color("#FFFFFF")
             self._preview.set_icon_color("#FFFFFF")
             
             # Active Tasks Icons
             self._actions.active_panel.set_icon_color("#FFFFFF")
             
             # 2. Styles
             app.setStyle("Fusion")
             app.setStyleSheet("""
                /* Global Reset */
                QMainWindow, QWidget { background-color: #1E1E1E; color: #E0E0E0; }
                
                /* Islands (Panels) */
                QFrame#SourcePanel, QScrollArea#FiltersPanel, QFrame#ActionsPanel, QFrame#PreviewPanel {
                    background-color: #252526;
                    border: 1px solid #333333;
                }
                QTabWidget::pane {
                    border: none;
                    background-color: #252526;
                    border-top: 1px solid #333;
                }
                QTabBar::tab {
                    background: #2D2D2D;
                    color: #888;
                    border: 1px solid #333;
                    border-bottom: none;
                }
                QTabBar::tab:selected {
                    background: #252526;
                    color: #FFF;
                    border-bottom: 1px solid #252526;
                    font-weight: bold;
                }
                
                /* Specific Widget Backgrounds */
                QWidget#FilesTab, QWidget#SettingsTab { background-color: #252526; }
                
                /* List & Tree */
                QTreeView, QListView {
                    background-color: #252526;
                    color: #E0E0E0;
                    border: none;
                    outline: none;
                }
                QTreeView::item, QListView::item {
                    border: none;
                    padding: 4px;
                }
                QTreeView::item:hover, QListView::item:hover {
                    background-color: #2A2D2E;
                }
                QTreeView::item:selected, QListView::item:selected {
                    background-color: #094771;
                    color: white;
                }
                
                /* Tree Lines (White) */
                QTreeView::branch { background: transparent; }
                QTreeView::branch:has-siblings:!adjoins-item { border-image: url(icons/vline-white.svg) 0; }
                QTreeView::branch:has-siblings:adjoins-item { border-image: url(icons/branch-more-white.svg) 0; }
                QTreeView::branch:!has-children:!has-siblings:adjoins-item { border-image: url(icons/branch-end-white.svg) 0; }
                
                /* Inputs */
                QLineEdit, QComboBox, QSpinBox, QDateEdit, QTextEdit {
                    background-color: #3C3C3C;
                    color: #F0F0F0;
                    border: 1px solid #555;
                    border-radius: 4px;
                }
                
                /* Labels & Checks */
                QLabel, QCheckBox { color: #E0E0E0; }
                
                /* Filter Chips */
                QFrame#FilterChip {
                    background-color: #333;
                    border: 1px solid #555;
                    border-radius: 14px;
                }
                QFrame#FilterChip QLabel { color: white; }
                
                /* Task Items (Action Panel) */
                QFrame#TaskItem {
                    background-color: #2D2D2D;
                    border: 1px solid #444;
                }
                QFrame#TaskItem QPushButton {
                    color: #FFFFFF; /* White Icons */
                    border: none;
                    background: transparent;
                }
                QFrame#TaskItem QPushButton:hover {
                    background-color: #444;
                    border-radius: 4px;
                }
                
                /* Main Buttons */
                QPushButton {
                    background-color: #3B82F6;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 6px;
                }
                QPushButton:hover { background-color: #2563EB; }
                QPushButton:disabled {
                    background-color: #E0E0E0;
                    color: #000000; /* Black text for disabled state */
                }
                
                /* Progress Bar */
                QProgressBar {
                    color: white;
                    text-align: center;
                    border: 1px solid #444;
                    background-color: #2D2D2D;
                }
                QProgressBar::chunk { background-color: #3B82F6; }
                
                /* Header */
                QLabel#SectionHeader { color: #FFFFFF; font-weight: bold; font-size: 13px; }
                
                /* Preview Count & CheckBox */
                QLabel#PreviewCountLabel { color: #E0E0E0; font-size: 11px; }
                QCheckBox { color: #E0E0E0; }
                
                /* Filter Chip Label must be white */
                QFrame#FilterChip QLabel { color: #FFFFFF; font-weight: bold; }
                
                /* No Action Label (White) */
                QLabel#NoActionLabel { color: #E0E0E0; font-weight: bold; }
             """)
             
        elif theme == "system":
             self._source.set_icon_color("#444444")
             self._preview.set_icon_color("#444444")
             self._actions.active_panel.set_icon_color("#444444")
             app.setStyle("Windows")
             app.setStyleSheet("")
             
        # Refresh Views to apply new icons
        self._source._refresh()
        
        # Refresh Task Items Icons (Manual update for active tasks)
        # We iterate over existing TaskItems and update their icons
        count = self._actions.active_panel.task_lay.count()
        icon_color = "#FFFFFF" if theme == "dark" else "#444444"
        
        # Helper to colorize
        def colorize_icon(path, color):
            if not Path(path).exists(): return QIcon()
            pix = QPixmap(path)
            if pix.isNull(): return QIcon()
            colored = QPixmap(pix.size())
            colored.fill(Qt.GlobalColor.transparent)
            painter = QPainter(colored)
            painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
            painter.drawPixmap(0, 0, pix)
            painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
            painter.fillRect(colored.rect(), QColor(color))
            painter.end()
            return QIcon(colored)
            
        edit_icon = colorize_icon("icons/edit-solid.svg", icon_color)
        del_icon = colorize_icon("icons/xmark-solid.svg", icon_color)
        refresh_icon = colorize_icon("icons/arrows-rotate-solid.svg", icon_color)
        browse_icon = colorize_icon("icons/folder-open-solid.svg", icon_color)
        
        # Update Source Panel Buttons
        self._source.btn_refresh.setIcon(refresh_icon)
        self._source.btn_browse.setIcon(browse_icon)

        # Update Active Tasks
        for i in range(count):
            item = self._actions.active_panel.task_lay.itemAt(i)
            if item and item.widget():
                w = item.widget()
                if isinstance(w, TaskItem):
                    w.btn_edit.setIcon(edit_icon)
                    w.btn_del.setIcon(del_icon)

        self._preview.exec_action.connect(self._on_exec)
    
    def _on_dir_selected(self, path: str):
        """Kaynak klasör seçildiğinde çağrılır"""
        self._preview.set_root_path(path)
    
    def _on_filter_added(self, filter_type: str, filter_id: str, filter_data: dict):
        """Filtre eklendiğinde çağrılır"""
        self._preview.add_filter(filter_id, filter_data)
    
    def _on_filter_removed(self, filter_id: str):
        """Filtre kaldırıldığında çağrılır"""
        self._preview.remove_filter(filter_id)
    
    def _on_del(self, p):
        # GÜVENLİK ÖNLEMİ: Yanlışlıkla silmeyi önlemek için devre dışı
        QMessageBox.warning(self, self._t("msg_title_security_warning"), 
            self._t("msg_security_delete_disabled"))
        return

        import shutil
        path = Path(p)
        if not path.exists():
            return
        if path.is_dir():
            msg = self._t("msg_delete_folder_confirm", p)
        else:
            msg = self._t("msg_delete_file_confirm", p)
        reply = QMessageBox.question(
            self, self._t("msg_title_delete_confirm"), msg,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            try:
                if path.is_dir():
                    shutil.rmtree(path)
                else:
                    path.unlink()
                
                # Başarılı silme sonrası yenile
                QTimer.singleShot(200, self._source._refresh)
            except PermissionError:
                QMessageBox.warning(self, self._t("msg_title_error"), self._t("msg_file_in_use", p))
            except Exception as e:
                QMessageBox.warning(self, self._t("msg_title_error"), self._t("msg_delete_failed", e))
    
    def _on_action(self, key):
        # Kullanıcı manuel olarak aksiyon menüsüne tıkladı
        # Düzenleme modunu iptal et
        self._editing_task_index = None
    
    def _on_action_requested(self, action_key, data):
        """ActionSettingsPanel'den 'Uygula' tıklandığında çağrılır"""
        try:
            # Maks 3 Aksiyon Kontrolü (Yeni ekleme yapılacaksa)
            if self._editing_task_index is None and self._actions.active_panel.get_task_count() >= 3:
                QMessageBox.warning(self, self._t("msg_title_warning"), self._t("msg_max_actions"))
                return

            # Aktif seçili dosyaların sayısını al (PreviewPanel'den)
            files = self._preview._filtered_files
            count = len(files)
            
            if count == 0:
                QMessageBox.warning(self, self._t("msg_title_warning"), self._t("msg_no_files_to_process"))
                return
                
            display_name = "Bilinmeyen"
            for d, k in ActionsPanel.ACTIONS:
                if k == action_key:
                    display_name = d
                    break
            
            # Görev metnini oluştur
            task_text = f"{display_name} -> {count} Dosya"
            
            if self._editing_task_index is not None:
                 # Güncelle
                 self._actions.active_panel.update_task(self._editing_task_index, action_key, data, task_text)
                 self._editing_task_index = None
            else:
                 # Yeni Ekle
                 self._actions.active_panel.add_task(action_key, data, task_text, count)
        except Exception as e:
            print(f"_on_action_requested error: {e}")
            import traceback
            traceback.print_exc()
        
    def _on_run_active_actions(self):
        """Aktif görevleri sırayla çalıştır (GÜVENLİ VERSİYON)"""
        task_count = self._actions.active_panel.get_task_count()
        if task_count == 0: return
        
        # 1. Görevleri Topla
        tasks = []
        layout = self._actions.active_panel.task_lay
        for i in range(layout.count()):
             w = layout.itemAt(i).widget()
             if isinstance(w, TaskItem):
                 tasks.append((w.action_key, w.action_data))
        
        # 2. Dosyaları Al
        files = self._preview._filtered_files
        if not files:
            QMessageBox.warning(self, self._t("msg_title_warning"), self._t("msg_no_files"))
            return
            
        # 3. Önceki Worker'ı Temizle (KESİN TEMİZLİK)
        if hasattr(self, '_action_worker') and self._action_worker is not None:
            try:
                # Sinyalleri kopar
                try: self._action_worker.finished.disconnect()
                except: pass
                try: self._action_worker.progress.disconnect()
                except: pass
                
                if self._action_worker.isRunning():
                    self._action_worker.quit()
                    self._action_worker.wait() # Bekle
                
                self._action_worker.deleteLater()
            except Exception as e:
                print(f"Worker cleanup error: {e}")
        
        self._action_worker = None # Referansı boşalt
            
        # 4. Worker'ı Başlat
        from workers import ActionRunnerThread # Import'u garantiye al
        self._action_worker = ActionRunnerThread(files, tasks)
        self._action_worker.progress.connect(self._actions.active_panel.set_progress)
        self._action_worker.finished.connect(self._on_action_finished)
        self._action_worker.start()
        
        # UI Disable
        self._actions.active_panel.btn_run_all.setEnabled(False)
        self._actions.active_panel.btn_run_all.setText(self._t("msg_processing"))

    def _on_action_finished(self, errors):
        # 1. Thread Temizliği
        if hasattr(self, '_action_worker') and self._action_worker:
            # Sinyalleri kopar
            try: self._action_worker.finished.disconnect()
            except: pass
            
            self._action_worker.deleteLater()
            self._action_worker = None # HEMEN NONE YAP

        # 2. Kullanıcıya Bilgi Ver
        if errors:
            msg = "\n".join(errors[:10])
            if len(errors) > 10: msg += self._t("msg_and_more_errors", len(errors)-10)
            QMessageBox.warning(self, self._t("msg_title_completed_with_errors"), self._t("msg_some_operations_failed", msg))
        else:
            # Başarılı mesajını kaldırmak isterseniz burayı yorum satırı yapın, 
            # bazen art arda işlem yaparken mesaj kutusu odak kaybına neden olabilir.
            QMessageBox.information(self, self._t("msg_title_success"), self._t("msg_all_operations_success"))
            
        # 3. GÜVENLİ YENİLEME
        # Kaynak paneli yenile
        self._source._refresh()
        
        # Önizleme panelini yenile (Artık daha güvenli olan fonksiyonu çağırıyor)
        QTimer.singleShot(500, self._preview.reload_directory)
        
        # Butonu resetle (ActiveActionsPanel içindeki fonksiyonu tetikle)
        self._actions.active_panel.reset_progress()

    def _on_task_edit(self, index):
        """Görev düzenleme isteği"""
        # TaskItem'ı ve verisini bul
        task_item = None
        layout = self._actions.active_panel.task_lay
        for i in range(layout.count()):
             w = layout.itemAt(i).widget()
             if isinstance(w, TaskItem) and w.index == index:
                 task_item = w
                 break
        
        if not task_item: return
        
        # 1. Edit Modunu Başlat
        self._editing_task_index = index
        
        # 2. İlgili aksiyon formunu aç
        display_name = "Aksiyon"
        for d, k in ActionsPanel.ACTIONS:
            if k == task_item.action_key:
                display_name = d
                break
        
        # Sol menüdeki butonu seçili yap (Bu formu açar ve sıfırlar)
        button_found = False
        for btn in self._actions._btn_group.buttons():
            if btn.text() == display_name:
                btn.setChecked(True)
                button_found = True
                break
        
        # Eğer buton bulamazsak manuel aç (Nadir durum)
        if not button_found:
             self._actions.settings_panel.show_form(task_item.action_key, display_name)

        # 3. Veriyi yükle (Form açıldıktan ve sıfırlandıktan SONRA)
        self._actions.settings_panel.load_from_data(task_item.action_key, task_item.action_data)

    def _simulate_progress(self, total):
        self._sim_total = total
        self._sim_current = 0
        self._sim_timer = QTimer()
        self._sim_timer.timeout.connect(self._do_sim)
        self._sim_timer.start(50) # Hızlı simülasyon

    def _do_sim(self):
        self._sim_current += max(1, self._sim_total // 20)
        if self._sim_current >= self._sim_total:
            self._sim_current = self._sim_total
            self._sim_timer.stop()
        self._actions.active_panel.set_progress(self._sim_current, self._sim_total)

    def _on_exec(self, key, settings):
        # Preview panel içindeki Run butonları için
        self._on_action_requested(key, settings)

def excepthook(exc_type, exc_value, exc_tb):
    """Global exception handler"""
    import traceback
    traceback.print_exception(exc_type, exc_value, exc_tb)
    # Keep app running to see the error
    
def main():
    # Install global exception hook
    sys.excepthook = excepthook
    
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    pal = app.palette()
    pal.setColor(QPalette.ColorRole.Highlight, QColor("#D7D6D2"))
    pal.setColor(QPalette.ColorRole.HighlightedText, QColor("#444444"))
    pal.setColor(QPalette.ColorRole.Base, QColor("#F9F8F2"))
    app.setPalette(pal)
    app.setStyleSheet(STYLE_SHEET)
    
    try:
        win = MainWindow()
        win.show()
        sys.exit(app.exec())
    except Exception as e:
        import traceback
        print(f"CRITICAL ERROR: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()