# Product Context

## Project Name
File-Architect-Pro

## Description
An advanced file management and architecture tool built with Python and PyQt6. Allows users to visualize directory structures, filter files by various criteria, and perform batch operations.

## Core Features
1. **Source Directory Browser**:
    * Tree view of the file system.
    * Custom drawn hierarchy lines (centered).
    * Folder expansion logic (deep automatic expansion).
2. **Filter Panel**:
    * Collapsible filters (Extension, Name, Regex, Size, etc.).
    * Center column layout.
3. **Action Panel**:
    * Symmetric structure with filter panel.
    * Operation buttons on the left, dynamic settings panel (`ActionSettingsPanel`) on the right.
    * **Active Actions List**: Selected operations (Max 3) are listed here, can be edited or deleted.
    * **Worker Thread Architecture**: File operations run in the background without freezing the main interface.
4. **File Preview Panel**:
    * Detail view (Name, Type, Size, Modified Date).
    * Text preview for supported files.
    * Operation configuration interfaces (pattern input, etc.).

## Design Philosophy
* **Professional Interface**: Custom styling, "Fusion" style base, removal of default system blue highlights.
* **Aesthetic**: Minimalist, clean lines, custom color palette (#E7E6E2, #F0EFEB, #F9F8F2).
* **Responsive**: Panels resize proportionally, grid structure adapts to screen size.
* **User Friendly**: Users are continuously informed with progress indicators and confirmation messages during operations.
