# File-Architect-Pro - Memory Bank

## Project Overview
**Application Name:** File-Architect-Pro  
**Version:** v1.0.0  
**Framework:** PyQt6  
**Language:** Python  
**Purpose:** A professional file management and batch processing application with filtering, actions, and preview capabilities.

---

## Architecture

### Main Components (Classes)

| Class | Location | Purpose |
|-------|----------|---------|
| `MainWindow` | ~Line 3650 | Main application window, orchestrates all panels |
| `SourcePanel` | ~Line 800 | File tree view with browse, refresh, and hidden file management |
| `FiltersPanel` | ~Line 1779 | Filter list buttons + FilterSettingsPanel |
| `FilterSettingsPanel` | ~Line 1149 | Dynamic filter forms (Extension, Filename, Size, Date, etc.) |
| `ActionsPanel` | ~Line 2650 | Action list buttons + ActionSettingsPanel + ActiveActionsPanel |
| `ActionSettingsPanel` | ~Line 1862 | Dynamic action forms (Rename, Copy, Tag, etc.) |
| `ActiveActionsPanel` | ~Line 2366 | Task queue with run button and progress |
| `PreviewPanel` | ~Line 2700 | File list/tree preview with filtering results |
| `AppSettingsWidget` | ~Line 680 | Theme and language settings tab |

### Key Signals
- `language_changed(str)` - Emitted by AppSettingsWidget when language changes
- `theme_changed(str)` - Emitted when theme changes (light/dark/system)
- `filter_added/removed` - Filter chip management
- `action_requested` - Action execution request
- `run_requested` - Start all queued actions

---

## Translation System (i18n)

### Implementation
- **Method:** `MainWindow._update_ui_text()` (Line ~3700)
- **Trigger:** Connected to `AppSettingsWidget.language_changed` signal
- **Languages:** Turkish (tr), English (en)

### Translation Dictionary Keys
```python
# Base translations (tr/en dictionaries at ~Line 3730)
"source_tab_files", "source_tab_settings", "source_header", "browse",
"filter_header", "filter_add", "filter_reset", "filter_cancel",
"actions_header", "preview_header", "folder_structure", "files_count",
"run_button"

# Dynamic translations (added via t.update() at ~Line 3765)
# Actions
"action_seq_rename", "action_prefix_suffix", "action_find_replace",
"action_change_ext", "action_copy", "action_tag", "action_flatten",
"action_secure_del", "action_merge", "action_csv", "action_excel"

# Filters
"filter_panel_header", "filter_Uzantı", "filter_Dosya Adı", "filter_Metin",
"filter_Metin Yok", "filter_Boyut", "filter_Regex", "filter_Boş Dosya",
"filter_Oluşturma Tarihi", "filter_Değişiklik Tarihi", "filter_Şifreli", "filter_Gizli"

# App Settings & Placeholders
"app_settings", "theme_label", "lang_label", "apply_settings",
"placeholder_select_filter", "label_active_filters",
"placeholder_select_action", "placeholder_no_actions",
"placeholder_select_folder", "no_folder_selected",
"btn_run_actions", "action_settings_header", "active_actions_header",
"theme_items" (list)
```

### Panel update_texts Methods
Each panel has an `update_texts(t)` method that receives the translation dictionary:
- `AppSettingsWidget.update_texts(t)` - Header, labels, button, ComboBox items
- `SourcePanel.update_texts(t)` - Placeholder, path label
- `FiltersPanel.update_texts(t)` - Header, filter buttons
- `FilterSettingsPanel.update_texts(t)` - Placeholder, active filters label
- `ActionSettingsPanel.update_texts(t)` - Placeholder, header
- `ActiveActionsPanel.update_texts(t)` - Header, no-action label, run button
- `PreviewPanel.update_texts(t)` - List placeholder

---

## Styling

### Theme System
- Light theme: `LIGHT_STYLE` (Line ~45)
- Dark theme: `DARK_STYLE` (Line ~400)
- System detection via `darkdetect` module

### Key Style Classes
- `#SourcePanel`, `#FiltersPanel`, `#ActionsPanel`, `#PreviewPanel`
- `#SectionHeader` - Bold section titles
- `#ListBtn` - Filter/Action toggle buttons
- `#BrowseBtn` - Icon buttons
- `#TaskItem` - Active action items
- `#FilterChip` - Applied filter tags

---

## File Operations

### Source Panel Features
- QFileSystemModel with proxy for hidden files
- Virtual deletion (hide from view, not disk)
- Root drive protection (prevents C:\, D:\ deletion)
- File watcher enabled for auto-refresh

### Filter Types
1. Uzantı (Extension) - File extension filter
2. Dosya Adı (Filename) - Name pattern matching
3. Metin (Text Content) - Content search
4. Metin Yok (No Text) - Exclude content
5. Boyut (Size) - Size comparison (>, <, =)
6. Regex - Regular expression
7. Boş Dosya (Empty File) - Zero-byte files
8. Oluşturma Tarihi (Created Date) - Date range
9. Değişiklik Tarihi (Modified Date) - Date range
10. Şifreli (Encrypted) - Encrypted files
11. Gizli (Hidden) - Hidden files

### Action Types
1. seq_rename - Sequential renaming with pattern
2. prefix_suffix - Add prefix/suffix
3. find_replace - Find and replace in names
4. change_ext - Change file extension
5. copy - Copy to target folder
6. tag - Add metadata tags
7. flatten - Flatten folder structure
8. secure_del - Secure deletion (overwrite)
9. merge - Merge text files
10. csv/excel - Generate reports

---

## Known Issues & Notes

1. **Message Boxes:** QMessageBox dialogs still use hardcoded Turkish strings (not translated)
2. **Dynamic Button Text:** Run button shows "{count} Aksiyonu Başlat" with proper translation
3. **ComboBox Items:** Theme selector items are dynamically updated on language change
4. **Filter Key Property:** Each filter button has `filter_key` property for translation lookup
5. **Action Key Property:** Each action button has `action_key` property for translation lookup

---

## Recent Changes (December 2024)

### Language Switching Implementation
- Full Turkish/English translation support
- Dynamic UI text updates without restart
- ComboBox item translation
- Placeholder text translation
- Panel header translation
- Button text translation

### Bug Fixes
- Fixed `btn_apply` NameError in AppSettingsWidget
- Fixed IndentationError in ActiveActionsPanel.get_task_count
- Fixed AttributeError for missing panel references
- Fixed FilterSettingsPanel.settings_panel access path

---

## File Structure
```
File-Architect-Pro/
├── main.py              # Main application (4300+ lines)
├── icons/               # SVG icons for buttons
│   ├── folder-open-solid.svg
│   ├── arrows-rotate-solid.svg
│   ├── edit-solid.svg
│   ├── xmark-solid.svg
│   └── ...
├── .agent/
│   ├── memory-bank/     # This file
│   └── workflows/       # Automation workflows
└── README.md
```

---

## Development Notes

### Adding New Translations
1. Add key to both `tr` and `en` dictionaries in `_update_ui_text()`
2. Add `update_texts(t)` method to relevant panel class
3. Call panel's `update_texts(t)` from `MainWindow._update_ui_text()`
4. Make target labels/buttons accessible via `self.`

### Testing Language Switch
1. Run `Py main.py`
2. Go to "Settings" tab
3. Change "Dil (Language)" dropdown
4. Click "Ayarları Uygula" / "Apply Settings"
5. All UI elements should update immediately
