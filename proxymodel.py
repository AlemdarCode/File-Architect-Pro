from PyQt6.QtCore import QSortFilterProxyModel, QFileInfo, QDate, Qt

class PreviewProxyModel(QSortFilterProxyModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.active_filters = {} # {filter_id: filter_data}
        self.root_path = None
        self.whitelist_dirs = None # Set of paths (None = Devre dışı)
        self.setRecursiveFilteringEnabled(True) # Alt klasörleri de filtrele

    def set_filters(self, filters):
        self.active_filters = filters.copy()
        # Filtreler değişince whitelist'i sıfırla
        self.whitelist_dirs = None
        self.invalidateFilter() # Reset yerine invalidate kullan (State korunur)

    def set_whitelist(self, dirs):
        """Sadece bu klasörleri göster (Performans Modu)"""
        self.beginResetModel()
        self.whitelist_dirs = dirs
        self.endResetModel()

    def filterAcceptsRow(self, source_row, source_parent):
        # Eğer filtre yoksa, hiçbir şey gösterme (Performans ve istek üzerine)
        if not self.active_filters:
            return False

        # Dosya indeksini al
        source_model = self.sourceModel()
        index = source_model.index(source_row, 0, source_parent)
        
        # Klasörleri kontrol et
        if source_model.isDir(index):
            if self.whitelist_dirs is not None:
                # Whitelist aktifse, sadece listedeki klasörleri göster
                path = source_model.filePath(index)
                # Normalizasyon (separator farklarını önlemek için)
                path = path.replace('/', '\\')
                if path not in self.whitelist_dirs:
                    return False
            return True

        # Dosya bilgilerini al
        file_name = source_model.fileName(index)
        file_path = source_model.filePath(index)
        if not file_path: return False
        file_info = QFileInfo(file_path)
        
        # Filtreleri Ayrıştır
        extension_filters = []
        other_filters = []
        
        for f_data in self.active_filters.values():
            if f_data.get("type") == "Uzantı":
                extension_filters.append(f_data)
            else:
                other_filters.append(f_data)
        
        # 1. Uzantı Kontrolü (OR Mantığı)
        if extension_filters:
            ext_match = False
            current_ext = file_info.suffix().lower()
            if current_ext.startswith('.'):
                current_ext = current_ext[1:]
                
            for f_data in extension_filters:
                allowed = f_data.get("extensions", [])
                if current_ext in allowed:
                    ext_match = True
                    break
            
            if not ext_match:
                return False

        # 2. Diğer Filtreler (AND Mantığı)
        for f_data in other_filters:
            ft = f_data.get("type")
            
            if ft == "Dosya Adı":
                text = f_data.get("text", "")
                if not text: continue
                match_text = file_name
                search_text = text
                if not f_data.get("case_sensitive"):
                    match_text = match_text.lower()
                    search_text = search_text.lower()
                
                if f_data.get("exact_match"):
                    match = match_text == search_text
                else:
                    match = search_text in match_text
                
                if f_data.get("invert"):
                    if match: return False
                else:
                    if not match: return False

            elif ft == "Boyut":
                size = file_info.size()
                op = f_data.get("op", ">")
                target = f_data.get("value", 0)
                unit = f_data.get("unit", "KB")
                
                if unit == "KB": target *= 1024
                elif unit == "MB": target *= 1024**2
                elif unit == "GB": target *= 1024**3
                
                if op == ">" and not (size > target): return False
                if op == "<" and not (size < target): return False
                if op == "=" and not (size == target): return False

            elif ft == "Oluşturma Tarihi":
                dt = file_info.birthTime().date()
                start = QDate.fromString(f_data.get("start"), "yyyy-MM-dd")
                end = QDate.fromString(f_data.get("end"), "yyyy-MM-dd")
                if not (start <= dt <= end): return False

            elif ft == "Değişiklik Tarihi":
                dt = file_info.lastModified().date()
                start = QDate.fromString(f_data.get("start"), "yyyy-MM-dd")
                end = QDate.fromString(f_data.get("end"), "yyyy-MM-dd")
                if not (start <= dt <= end): return False

            elif ft == "Boş Dosya":
                if file_info.size() > 0: return False

            elif ft == "Gizli":
                if not file_info.isHidden(): return False
            
        return True
