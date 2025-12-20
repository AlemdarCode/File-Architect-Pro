
# =============================================================================
# FILTER SETTINGS UI (RIGHT SIDE)
# =============================================================================

class FilterSettingsPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.forms = {}
        self._build()

    def _build(self):
        lay = QVBoxLayout(self)
        lay.setContentsMargins(16, 4, 4, 4)
        lay.setSpacing(12)
        
        # Header
        self.header_lbl = QLabel("Filtre Ayarları")
        self.header_lbl.setStyleSheet("font-weight: bold; font-size: 13px; color: #333;")
        lay.addWidget(self.header_lbl)
        
        # Stack
        self.stack = QStackedWidget()
        lay.addWidget(self.stack)
        
        # Create Forms and add to stack
        self._init_forms()
        
        # Buttons
        btn_lay = QHBoxLayout()
        btn_lay.setSpacing(6)
        
        self.btn_add = QPushButton("Filtre Ekle")
        self.btn_reset = QPushButton("Sıfırla")
        self.btn_cancel = QPushButton("İptal")
        
        # Style buttons
        # self.btn_add.setStyleSheet("background-color: #e0e0e0; font-weight: bold;")
        
        btn_lay.addWidget(self.btn_add)
        btn_lay.addWidget(self.btn_reset)
        btn_lay.addWidget(self.btn_cancel)
        
        lay.addLayout(btn_lay)
        
        # Active Filters Section
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("color: #ccc;")
        lay.addWidget(sep)
        
        lbl_active = QLabel("Aktif Filtreler")
        lbl_active.setStyleSheet("font-weight: bold; font-size: 12px;")
        lay.addWidget(lbl_active)
        
        # Scroll Area for chips
        self.chips_container = QWidget()
        self.chips_lay = QVBoxLayout(self.chips_container)
        self.chips_lay.setContentsMargins(0,0,0,0)
        self.chips_lay.setSpacing(4)
        self.chips_lay.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.chips_container)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background: transparent;")
        
        lay.addWidget(scroll)
        
    def _init_forms(self):
        # 1. Uzantı
        f_ext = QWidget()
        l_ext = QFormLayout(f_ext)
        l_ext.addRow("Uzantılar (örn: jpg, png):", QLineEdit())
        self._add_stack("Uzantı", f_ext)
        
        # 2. Dosya Adı
        f_name = QWidget()
        l_name = QVBoxLayout(f_name)
        l_name.setSpacing(8)
        l_name.addWidget(QLabel("Arama Metni:"))
        l_name.addWidget(QLineEdit())
        l_name.addWidget(QCheckBox("Büyük/Küçük Harf Duyarlı"))
        l_name.addWidget(QCheckBox("Tam Eşleşme"))
        l_name.addWidget(QCheckBox("Tersini Al (İçermeyen)"))
        l_name.addStretch()
        self._add_stack("Dosya Adı", f_name)
        
        # 3. Metin (İçerik)
        f_content = QWidget()
        l_content = QVBoxLayout(f_content)
        l_content.addWidget(QLabel("Dosya İçeriği (Metin):"))
        l_content.addWidget(QLineEdit())
        l_content.addWidget(QCheckBox("Büyük/Küçük Harf Duyarlı"))
        l_content.addStretch()
        self._add_stack("Metin", f_content)
        
        # 4. Regex
        f_regex = QWidget()
        l_regex = QVBoxLayout(f_regex)
        l_regex.addWidget(QLabel("Regular Expression:"))
        l_regex.addWidget(QLineEdit())
        l_regex.addStretch()
        self._add_stack("Regex", f_regex)
        
        # 5. Metin Yok
        f_nocontent = QWidget()
        l_nocontent = QVBoxLayout(f_nocontent)
        l_nocontent.addWidget(QLabel("İçermeyen Metin:"))
        l_nocontent.addWidget(QLineEdit())
        l_nocontent.addStretch()
        self._add_stack("Metin Yok", f_nocontent)
        
        # 6. Boyut
        f_size = QWidget()
        l_size = QFormLayout(f_size)
        
        cb_op = QComboBox()
        cb_op.addItems(["> Büyüktür", "< Küçüktür", "= Eşittir"])
        l_size.addRow("Operatör:", cb_op)
        
        sb_val = QDoubleSpinBox()
        sb_val.setRange(0, 999999999)
        l_size.addRow("Değer:", sb_val)
        
        cb_unit = QComboBox()
        cb_unit.addItems(["MB", "KB", "GB", "Byte"])
        l_size.addRow("Birim:", cb_unit)
        self._add_stack("Boyut", f_size)
        
        # 7. Boş Dosya
        f_empty = QWidget()
        l_empty = QVBoxLayout(f_empty)
        l_empty.addWidget(QLabel("Boş dosyaları (0 byte) göster."))
        l_empty.addStretch()
        self._add_stack("Boş Dosya", f_empty)
        
        # 8. Tarih (Genel)
        f_date = QWidget()
        l_date = QFormLayout(f_date)
        l_date.addRow("Başlangıç:", QDateEdit())
        l_date.addRow("Bitiş:", QDateEdit())
        self._add_stack("Oluşturma Tarihi", f_date)
        
        f_date2 = QWidget()
        l_date2 = QFormLayout(f_date2)
        l_date2.addRow("Başlangıç:", QDateEdit())
        l_date2.addRow("Bitiş:", QDateEdit())
        self._add_stack("Değişiklik Tarihi", f_date2)

        # 9. Şifreli / Gizli
        f_bool = QWidget()
        l_bool = QVBoxLayout(f_bool)
        l_bool.addWidget(QLabel("Bu özellik için ayar yok."))
        l_bool.addStretch()
        self._add_stack("Şifreli", f_bool)
        
        f_hidden = QWidget()
        l_hidden = QVBoxLayout(f_hidden)
        l_hidden.addWidget(QLabel("Gizli dosyaları göster."))
        l_hidden.addStretch()
        self._add_stack("Gizli", f_hidden)
        
        # Default placeholder
        f_def = QWidget()
        l_def = QVBoxLayout(f_def)
        l_def.addWidget(QLabel("Soldan bir filtre seçiniz."))
        l_def.addStretch()
        self.stack.addWidget(f_def)

    def _add_stack(self, name, widget):
        idx = self.stack.addWidget(widget)
        self.forms[name] = idx

    def show_form(self, name):
        self.header_lbl.setText(f"{name} Ayarları")
        if name in self.forms:
            self.stack.setCurrentIndex(self.forms[name])
        else:
            self.stack.setCurrentIndex(self.stack.count()-1)
