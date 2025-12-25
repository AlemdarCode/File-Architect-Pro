# System Patterns

## Architecture
* **Monolithic Script**: Currently `main.py` contains all application logic (`MainWindow`, `SourcePanel`, `FiltersPanel`, `ActionsPanel`, `PreviewPanel` classes are here).
* **Event Driven**: Heavy reliance on PyQt6 Signal/Slot mechanism for inter-component communication (e.g., selection change in Source panel triggers Preview panel).

## Interface Patterns
* **Custom Painting**: Items and lines are typically custom drawn with Delegates or `paintEvent` overrides (`GradientLine`, `TreeDelegate`).
* **Style Sheet (QSS)**: Global `STYLE_SHEET` constant defines the base appearance.
* **Layouts**: Nested `QVBoxLayout` and `QHBoxLayout`, combined with `QGridLayout` for main grid.

## Main Classes
* `MainWindow`: Organizes layout and creates panels.
* `SourcePanel`: `QTreeView` with `QFileSystemModel`. Manages directory navigation.
* `FiltersPanel`: Hosts filtering buttons.
* `FilterSettingsPanel`: Form stack for filter settings on the right side (StackedWidget). Fixed width (280px).
* `FilterChip`: Tag widget for active filters. Delete with red circle X button.
* `ActionsPanel`: Hosts operation buttons.
* `ActionSettingsPanel`: Right panel for action settings (symmetric structure with FilterSettingsPanel). Fixed width (300px).
* `PreviewPanel`: Main panel showing file list (`QListView` or `QTreeView`). Does advanced filtering using `PreviewProxyModel`.
* `ModernSpinBox`: Custom designed number input widget. Number-only input with QIntValidator.
* `PreviewProxyModel`: Smart filtering layer based on `QSortFilterProxyModel`.

## Form Widget Management
* `form_widgets` dictionary: Stores widget references for each form type.
* Widget types: `input` (QLineEdit), `case/exact/invert` (QCheckBox), `val` (ModernSpinBox), `op/unit` (QComboBox), `start/end` (QDateEdit).
* `_on_reset()`: Resets the current form.
* `_get_filter_description()`: Reads actual form values and creates description.

## Design Rules
* **No Blue Highlight**: Strictly prevented with Palette and QSS.
* **Centered Hierarchy Lines**: Lines must align with the center of file/folder icon.
* **Compact Mode**: Dense layout with small padding.
* **Dynamic Buttons**: Main buttons (stretch 2), Cancel button (stretch 1).
* **Full Screen Support**: Panel structures preserved with fixed width, stretch added to right.

## New Architectural Patterns

### Smart Filtering Layer (Proxy Model Pattern)
`PreviewProxyModel` is used to overcome traditional `QFileSystemModel` limitations. This layer:
- Filters data from source model before reaching UI.
- Coordinates advanced logic like Size, Date, Regex.
- Provides atomic UI updates with `beginResetModel`/`endResetModel`.

### Chain-Expansion Pattern
Used to manage the asynchronous loading nature of `QFileSystemModel`:
1. `directoryLoaded(path)` signal is listened to.
2. Proxy index is obtained with `mapFromSource` for loaded directory and `expand()` is called.
3. If whitelist is active, only folders in the list have `fetchMore()` called to open hierarchy towards target.

### Background Scanner Pattern
Used for deep disk scanning without freezing the interface:
- Executed via `QThread` (FastScannerThread).
- Provides low-level and fast file system access with `os.walk`.
- Sends results to interface (PreviewPanel) as "Whitelist" via signal.

### Whitelist Filtering Pattern
Used for tree pruning at proxy model level:
- Valid folder paths from scanner are kept in a `set`.
- In `filterAcceptsRow`, only folders in this list are allowed to pass.
- This prevents TreeView from processing and drawing unnecessary thousands of folders.
