"""
Action Controller for File-Architect-Pro.
Handles file manipulation actions (rename, copy, merge, etc.).
"""

import re
from pathlib import Path
from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass


class ActionError(Exception):
    """Custom exception for action operations."""
    pass


@dataclass
class ActionResult:
    """Result of an action execution."""
    success: bool
    processed_count: int
    failed_count: int
    messages: List[str]
    
    @classmethod
    def success_result(cls, processed: int, messages: List[str] = None) -> 'ActionResult':
        return cls(True, processed, 0, messages or [])
    
    @classmethod
    def failure_result(cls, message: str) -> 'ActionResult':
        return cls(False, 0, 0, [message])


class ActionController:
    """
    Controller for file manipulation actions.
    Each action takes selected files and settings, returns ActionResult.
    """
    
    def __init__(self) -> None:
        self._action_handlers: Dict[str, Callable] = {
            "sequential_rename": self._execute_sequential_rename,
            "add_prefix_suffix": self._execute_prefix_suffix,
            "find_replace_text": self._execute_find_replace,
            "change_extension": self._execute_change_extension,
            "copy": self._execute_copy,
            "tag": self._execute_tag,
            "single_folder": self._execute_single_folder,
            "secure_delete": self._execute_secure_delete,
            "merge_text": self._execute_merge_text,
            "csv_report": self._execute_csv_report,
            "excel_report": self._execute_excel_report,
        }
    
    def execute_action(self, action_type: str, files: List[Path], settings: Dict[str, Any]) -> ActionResult:
        """
        Execute an action on the given files.
        
        Args:
            action_type: Type of action to execute
            files: List of files to process
            settings: Action-specific settings
            
        Returns:
            ActionResult with execution details
        """
        if action_type not in self._action_handlers:
            return ActionResult.failure_result(f"Unknown action type: {action_type}")
        
        if not files:
            return ActionResult.failure_result("No files selected")
        
        try:
            handler = self._action_handlers[action_type]
            return handler(files, settings)
        except Exception as e:
            return ActionResult.failure_result(f"Action failed: {str(e)}")
    
    def get_action_preview(self, action_type: str, files: List[Path], settings: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        Get preview of action results without executing.
        
        Returns:
            List of dicts with 'original' and 'result' keys
        """
        preview = []
        
        if action_type == "sequential_rename":
            pattern = settings.get("pattern", "File_{n}")
            start = settings.get("start_number", 1)
            step = settings.get("step", 1)
            preserve_ext = settings.get("preserve_extension", True)
            
            for i, file in enumerate(files):
                num = start + (i * step)
                new_name = pattern.replace("{n}", str(num))
                new_name = re.sub(r'\{n:(\d+)d\}', lambda m: str(num).zfill(int(m.group(1))), new_name)
                
                if preserve_ext and file.suffix:
                    new_name += file.suffix
                    
                preview.append({
                    "original": file.name,
                    "result": new_name
                })
        
        elif action_type == "add_prefix_suffix":
            prefix = settings.get("prefix", "")
            suffix = settings.get("suffix", "")
            before_ext = settings.get("before_extension", True)
            
            for file in files:
                if before_ext and file.suffix:
                    new_name = f"{prefix}{file.stem}{suffix}{file.suffix}"
                else:
                    new_name = f"{prefix}{file.name}{suffix}"
                    
                preview.append({
                    "original": file.name,
                    "result": new_name
                })
        
        elif action_type == "change_extension":
            from_ext = settings.get("from_extension", "")
            to_ext = settings.get("to_extension", "")
            
            for file in files:
                if file.suffix.lower() == from_ext.lower():
                    new_name = f"{file.stem}{to_ext}"
                    preview.append({
                        "original": file.name,
                        "result": new_name
                    })
        
        # TODO: Add preview generation for other action types
        
        return preview
    
    # === Action Implementations ===
    
    def _execute_sequential_rename(self, files: List[Path], settings: Dict[str, Any]) -> ActionResult:
        """Execute sequential rename action."""
        pattern = settings.get("pattern", "File_{n}")
        start = settings.get("start_number", 1)
        step = settings.get("step", 1)
        preserve_ext = settings.get("preserve_extension", True)
        
        processed = 0
        failed = 0
        messages = []
        
        for i, file in enumerate(files):
            try:
                num = start + (i * step)
                new_name = pattern.replace("{n}", str(num))
                new_name = re.sub(r'\{n:(\d+)d\}', lambda m: str(num).zfill(int(m.group(1))), new_name)
                
                if preserve_ext and file.suffix:
                    new_name += file.suffix
                
                new_path = file.parent / new_name
                
                if new_path.exists():
                    messages.append(f"Skipped {file.name}: target exists")
                    failed += 1
                    continue
                
                file.rename(new_path)
                processed += 1
                
            except Exception as e:
                messages.append(f"Failed {file.name}: {str(e)}")
                failed += 1
        
        return ActionResult(
            success=failed == 0,
            processed_count=processed,
            failed_count=failed,
            messages=messages
        )
    
    def _execute_prefix_suffix(self, files: List[Path], settings: Dict[str, Any]) -> ActionResult:
        """Execute add prefix/suffix action."""
        prefix = settings.get("prefix", "")
        suffix = settings.get("suffix", "")
        before_ext = settings.get("before_extension", True)
        
        if not prefix and not suffix:
            return ActionResult.failure_result("No prefix or suffix specified")
        
        processed = 0
        failed = 0
        messages = []
        
        for file in files:
            try:
                if before_ext and file.suffix:
                    new_name = f"{prefix}{file.stem}{suffix}{file.suffix}"
                else:
                    new_name = f"{prefix}{file.name}{suffix}"
                
                new_path = file.parent / new_name
                
                if new_path.exists():
                    messages.append(f"Skipped {file.name}: target exists")
                    failed += 1
                    continue
                
                file.rename(new_path)
                processed += 1
                
            except Exception as e:
                messages.append(f"Failed {file.name}: {str(e)}")
                failed += 1
        
        return ActionResult(
            success=failed == 0,
            processed_count=processed,
            failed_count=failed,
            messages=messages
        )
    
    def _execute_find_replace(self, files: List[Path], settings: Dict[str, Any]) -> ActionResult:
        """Execute find/replace text action."""
        find_text = settings.get("find", "")
        replace_text = settings.get("replace", "")
        case_sensitive = settings.get("case_sensitive", False)
        use_regex = settings.get("use_regex", False)
        in_content = settings.get("in_content", False)
        
        if not find_text:
            return ActionResult.failure_result("Find text not specified")
        
        processed = 0
        failed = 0
        messages = []
        
        for file in files:
            try:
                if in_content and file.is_file():
                    # Replace in file content
                    # TODO: Implement content replacement with encoding detection
                    pass
                else:
                    # Replace in filename
                    name = file.stem
                    ext = file.suffix
                    
                    if use_regex:
                        flags = 0 if case_sensitive else re.IGNORECASE
                        new_name = re.sub(find_text, replace_text, name, flags=flags)
                    else:
                        if case_sensitive:
                            new_name = name.replace(find_text, replace_text)
                        else:
                            # Case-insensitive replace
                            pattern = re.compile(re.escape(find_text), re.IGNORECASE)
                            new_name = pattern.sub(replace_text, name)
                    
                    if new_name != name:
                        new_path = file.parent / f"{new_name}{ext}"
                        
                        if new_path.exists():
                            messages.append(f"Skipped {file.name}: target exists")
                            failed += 1
                            continue
                        
                        file.rename(new_path)
                        processed += 1
                
            except Exception as e:
                messages.append(f"Failed {file.name}: {str(e)}")
                failed += 1
        
        return ActionResult(
            success=failed == 0,
            processed_count=processed,
            failed_count=failed,
            messages=messages
        )
    
    def _execute_change_extension(self, files: List[Path], settings: Dict[str, Any]) -> ActionResult:
        """Execute change extension action."""
        from_ext = settings.get("from_extension", "").lower()
        to_ext = settings.get("to_extension", "")
        
        if not from_ext or not to_ext:
            return ActionResult.failure_result("Extensions not specified")
        
        # Ensure extensions start with dot
        if not from_ext.startswith('.'):
            from_ext = '.' + from_ext
        if not to_ext.startswith('.'):
            to_ext = '.' + to_ext
        
        processed = 0
        failed = 0
        messages = []
        
        for file in files:
            try:
                if file.suffix.lower() == from_ext:
                    new_path = file.parent / f"{file.stem}{to_ext}"
                    
                    if new_path.exists():
                        messages.append(f"Skipped {file.name}: target exists")
                        failed += 1
                        continue
                    
                    file.rename(new_path)
                    processed += 1
                
            except Exception as e:
                messages.append(f"Failed {file.name}: {str(e)}")
                failed += 1
        
        return ActionResult(
            success=failed == 0,
            processed_count=processed,
            failed_count=failed,
            messages=messages
        )
    
    def _execute_copy(self, files: List[Path], settings: Dict[str, Any]) -> ActionResult:
        """Execute copy action."""
        destination = settings.get("destination", "")
        
        if not destination:
            return ActionResult.failure_result("Destination not specified")
        
        dest_path = Path(destination)
        if not dest_path.exists():
            try:
                dest_path.mkdir(parents=True)
            except Exception as e:
                return ActionResult.failure_result(f"Cannot create destination: {e}")
        
        import shutil
        processed = 0
        failed = 0
        messages = []
        
        for file in files:
            try:
                if file.is_file():
                    shutil.copy2(file, dest_path / file.name)
                else:
                    shutil.copytree(file, dest_path / file.name)
                processed += 1
            except Exception as e:
                messages.append(f"Failed {file.name}: {str(e)}")
                failed += 1
        
        return ActionResult(
            success=failed == 0,
            processed_count=processed,
            failed_count=failed,
            messages=messages
        )
    
    def _execute_tag(self, files: List[Path], settings: Dict[str, Any]) -> ActionResult:
        """Execute tag action."""
        # TODO: Implement file tagging (metadata or sidecar file approach)
        return ActionResult.failure_result("Tag action not yet implemented")
    
    def _execute_single_folder(self, files: List[Path], settings: Dict[str, Any]) -> ActionResult:
        """Execute single folder (flatten) action."""
        destination = settings.get("destination", "")
        
        if not destination:
            return ActionResult.failure_result("Destination not specified")
        
        dest_path = Path(destination)
        if not dest_path.exists():
            try:
                dest_path.mkdir(parents=True)
            except Exception as e:
                return ActionResult.failure_result(f"Cannot create destination: {e}")
        
        import shutil
        processed = 0
        failed = 0
        messages = []
        
        def flatten_dir(dir_path: Path) -> None:
            nonlocal processed, failed
            for item in dir_path.iterdir():
                if item.is_file():
                    try:
                        target = dest_path / item.name
                        # Handle duplicates
                        counter = 1
                        while target.exists():
                            target = dest_path / f"{item.stem}_{counter}{item.suffix}"
                            counter += 1
                        shutil.copy2(item, target)
                        processed += 1
                    except Exception as e:
                        messages.append(f"Failed {item.name}: {str(e)}")
                        failed += 1
                elif item.is_dir():
                    flatten_dir(item)
        
        for file in files:
            if file.is_dir():
                flatten_dir(file)
            else:
                try:
                    target = dest_path / file.name
                    shutil.copy2(file, target)
                    processed += 1
                except Exception as e:
                    messages.append(f"Failed {file.name}: {str(e)}")
                    failed += 1
        
        return ActionResult(
            success=failed == 0,
            processed_count=processed,
            failed_count=failed,
            messages=messages
        )
    
    def _execute_secure_delete(self, files: List[Path], settings: Dict[str, Any]) -> ActionResult:
        """Execute secure delete action."""
        import os
        
        passes = settings.get("passes", 3)
        processed = 0
        failed = 0
        messages = []
        
        for file in files:
            try:
                if file.is_file():
                    size = file.stat().st_size
                    with open(file, 'rb+') as f:
                        for _ in range(passes):
                            f.seek(0)
                            f.write(os.urandom(size))
                            f.flush()
                            os.fsync(f.fileno())
                    file.unlink()
                    processed += 1
                else:
                    messages.append(f"Skipped directory: {file.name}")
                    
            except Exception as e:
                messages.append(f"Failed {file.name}: {str(e)}")
                failed += 1
        
        return ActionResult(
            success=failed == 0,
            processed_count=processed,
            failed_count=failed,
            messages=messages
        )
    
    def _execute_merge_text(self, files: List[Path], settings: Dict[str, Any]) -> ActionResult:
        """Execute merge text files action."""
        output_file = settings.get("output_file", "")
        separator = settings.get("separator", "\n\n")
        encoding = settings.get("encoding", "utf-8")
        
        if not output_file:
            return ActionResult.failure_result("Output file not specified")
        
        output_path = Path(output_file)
        
        try:
            content_parts = []
            for file in files:
                if file.is_file():
                    try:
                        with open(file, 'r', encoding=encoding, errors='ignore') as f:
                            content_parts.append(f.read())
                    except Exception as e:
                        return ActionResult.failure_result(f"Cannot read {file.name}: {e}")
            
            merged_content = separator.join(content_parts)
            
            with open(output_path, 'w', encoding=encoding) as f:
                f.write(merged_content)
            
            return ActionResult.success_result(len(files), [f"Merged to {output_path}"])
            
        except Exception as e:
            return ActionResult.failure_result(f"Merge failed: {e}")
    
    def _execute_csv_report(self, files: List[Path], settings: Dict[str, Any]) -> ActionResult:
        """Execute CSV report generation action."""
        import csv
        
        output_file = settings.get("output_file", "file_report.csv")
        
        try:
            output_path = Path(output_file)
            
            with open(output_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Name', 'Path', 'Size', 'Type', 'Modified'])
                
                for file in files:
                    try:
                        stat = file.stat()
                        import datetime
                        mtime = datetime.datetime.fromtimestamp(stat.st_mtime)
                        writer.writerow([
                            file.name,
                            str(file),
                            stat.st_size,
                            file.suffix or 'Directory',
                            mtime.strftime('%Y-%m-%d %H:%M:%S')
                        ])
                    except Exception:
                        continue
            
            return ActionResult.success_result(len(files), [f"Report saved to {output_path}"])
            
        except Exception as e:
            return ActionResult.failure_result(f"Report generation failed: {e}")
    
    def _execute_excel_report(self, files: List[Path], settings: Dict[str, Any]) -> ActionResult:
        """Execute Excel report generation action."""
        # TODO: Implement Excel report using openpyxl
        # Requires: pip install openpyxl
        return ActionResult.failure_result("Excel report requires openpyxl package. Install with: pip install openpyxl")
