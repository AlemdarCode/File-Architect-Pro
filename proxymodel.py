from PyQt6.QtCore import QSortFilterProxyModel, QFileInfo, QDate, Qt

class PreviewProxyModel(QSortFilterProxyModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.active_filters = {} # {filter_id: filter_data}
        self.root_path = None
        self.whitelist_dirs = None # Set of paths (None = Disabled)
        self.setRecursiveFilteringEnabled(True) # Also filter subdirectories

    def set_filters(self, filters):
        self.active_filters = filters.copy()
        # Reset whitelist when filters change
        self.whitelist_dirs = None
        self.invalidateFilter() # Use invalidate instead of reset (State preserved)

    def set_whitelist(self, dirs):
        """Show only these directories (Performance Mode)"""
        self.beginResetModel()
        self.whitelist_dirs = dirs
        self.endResetModel()

    def filterAcceptsRow(self, source_row, source_parent):
        # If no filter, show nothing (Performance and per request)
        if not self.active_filters:
            return False

        # Get file index
        source_model = self.sourceModel()
        index = source_model.index(source_row, 0, source_parent)
        
        # Check directories
        if source_model.isDir(index):
            if self.whitelist_dirs is not None:
                # If whitelist is active, show only directories in list
                path = source_model.filePath(index)
                # Normalization (to prevent separator differences)
                path = path.replace('/', '\\')
                if path not in self.whitelist_dirs:
                    return False
            return True

        # Get file info
        file_name = source_model.fileName(index)
        file_path = source_model.filePath(index)
        if not file_path: return False
        file_info = QFileInfo(file_path)
        
        # Parse Filters
        extension_filters = []
        other_filters = []
        
        for f_data in self.active_filters.values():
            if f_data.get("type") == "Uzantı":
                extension_filters.append(f_data)
            else:
                other_filters.append(f_data)
        
        # 1. Extension Check (OR Logic)
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

        # 2. Other Filters (AND Logic)
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
