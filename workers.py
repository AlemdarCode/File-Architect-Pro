
from PyQt6.QtCore import QThread, pyqtSignal
from pathlib import Path
import os
import shutil
import re
import datetime
import csv
import secrets
import hashlib
import threading
import queue

# ============================================================
# GÜVENLİK FONKSİYONLARI (OWASP Uyumlu)
# ============================================================

def search_file_generator(file_path, search_term, case_sensitive=False):
    """
    Dosyayı satır satır okur, RAM'i şişirmez.
    Generator pattern ile memory-efficient arama.
    """
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            search = search_term if case_sensitive else search_term.lower()
            for line_num, line in enumerate(f, 1):
                check_line = line if case_sensitive else line.lower()
                if search in check_line:
                    yield line_num, line.strip()
    except Exception:
        pass  # Okunamayan dosyaları sessizce atla


def file_contains_text(file_path, search_term, case_sensitive=False):
    """
    Dosyada metin var mı kontrolü (ilk eşleşmede durur).
    RAM-efficient: Tüm dosyayı yüklemez.
    """
    for _ in search_file_generator(file_path, search_term, case_sensitive):
        return True
    return False


def safe_regex_search(pattern_str, text, timeout=2.0):
    """
    Regex aramasını belirli süre içinde bitirmezse durdurur.
    ReDoS koruması - Windows/Linux/Mac uyumlu.
    
    Returns: tuple (status, result)
        - ('success', matches_list)
        - ('timeout', error_message)
        - ('error', error_message)
    """
    result_queue = queue.Queue()

    def worker():
        try:
            compiled = re.compile(pattern_str)
            matches = list(compiled.finditer(text))
            result_queue.put(('success', matches))
        except re.error as e:
            result_queue.put(('error', str(e)))
        except Exception as e:
            result_queue.put(('error', str(e)))

    t = threading.Thread(target=worker)
    t.daemon = True
    t.start()
    t.join(timeout)

    if t.is_alive():
        return ('timeout', 'Regex çok karmaşık veya metin çok büyük')
    
    if not result_queue.empty():
        return result_queue.get()
    return ('error', 'Bilinmeyen hata')


def is_safe_path(base_path, target_path):
    """
    Hedef yolun güvenli olduğunu doğrula (Directory Traversal koruması).
    ../../../ gibi saldırıları engeller.
    """
    real_base = os.path.realpath(base_path)
    real_target = os.path.realpath(target_path)
    return real_target.startswith(real_base + os.sep) or real_target == real_base


# Windows rezerve dosya isimleri
WINDOWS_RESERVED = {'CON', 'PRN', 'AUX', 'NUL', 
                   'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9',
                   'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9'}

def is_valid_filename(name):
    """Windows'ta geçersiz dosya isimlerini kontrol eder."""
    if not name:
        return False
    base = name.split('.')[0].upper()
    return base not in WINDOWS_RESERVED


# Dosya tarama limiti (DoS koruması)
MAX_SCAN_FILES = 100000

class FastScannerThread(QThread):
    """
    Belirtilen dizini ve alt dizinlerini süper hızlı tarar (os.scandir kullanır).
    Filtreye uyan dosyaların yollarını ve bu dosyaların bulunduğu tüm üst klasör yollarını (whitelist) çıkarır.
    """
    scan_finished = pyqtSignal(set, set) # (whitelist_dirs, matched_files)
    
    def __init__(self, root_path, filters):
        super().__init__()
        self.root_path = root_path
        self.filters = filters
        self.is_running = True
        
    def run(self):
        whitelist_dirs = set()
        matched_files = set()
        
        # Filtreleri hazırla
        ext_filters = []
        other_filters = []
        
        for f in self.filters.values():
            if f.get("type") == "Uzantı":
                ext_filters.append(f)
            else:
                other_filters.append(f)
        
        # Uzantı setini hazırla (Hız için)
        allowed_extensions = set()
        for f in ext_filters:
            for ext in f.get("extensions", []):
                allowed_extensions.add('.' + ext if not ext.startswith('.') else ext)
                allowed_extensions.add(ext.lstrip('.')) # both .txt and txt
        
        file_count = 0  # Dosya sayısı sayacı
        
        try:
            for root, dirs, files in os.walk(self.root_path):
                if not self.is_running: break
                
                # Dosya limiti kontrolü (DoS koruması)
                if file_count >= MAX_SCAN_FILES:
                    print(f"Uyarı: Dosya limiti aşıldı ({MAX_SCAN_FILES})")
                    break
                
                # Dosyaları kontrol et
                dir_has_match = False
                
                for file in files:
                    if not self.is_running: break
                    
                    # Dosya limiti kontrolü
                    if file_count >= MAX_SCAN_FILES:
                        break
                    
                    full_path = Path(root) / file
                    
                    # Symlink kontrolü (güvenlik)
                    if full_path.is_symlink():
                        continue  # Symlink'leri atla
                    
                    # 1. Uzantı Kontrolü (Hızlı)
                    if allowed_extensions:
                        _, ext = os.path.splitext(file)
                        if ext.lower().lstrip('.') not in allowed_extensions:
                            continue # Uzantı uymuyorsa diğer filtrelere bakma (Optimizasyon)
                    
                    # 2. Diğer Filtreler (Yavaş olabilir, burada basitleştirilmiş kontrol yapılabilir)
                    # Şimdilik sadece uzantı ve isim kontrolü yapalım thread içinde.
                    # Detaylı kontrolü UI thread'de Proxy yapacak zaten. 
                    # Amaç "hangi klasörleri açmalıyız"ı bulmak.
                    
                    # Basit kabul: Eğer uzantı filtresi varsa ve uyuyorsa, veya filtre yoksa
                    match = True
                    # (Burada tam filtre kontrolü yapmak zor olabilir, QFileInfo vs thread güvenliği ve performans)
                    # Strateji: Uzantı uyuyorsa whitelist'e ekle. 
                    # Yanlış pozitifler olabilir (örn: boyut uymayan txt), ama sorun değil, UI onları gizler.
                    # Önemli olan yanlış negatif olmaması (olan bir şeyi açmamazlık yapmayalım).
                    
                    if match:
                        matched_files.add(str(full_path))
                        dir_has_match = True
                        file_count += 1
                
                if dir_has_match:
                    # Bu klasörü ve tüm üst klasörlerini whitelist'e ekle
                    current = Path(root)
                    while current != Path(self.root_path).parent:
                        whitelist_dirs.add(str(current))
                        current = current.parent
                        
        except Exception as e:
            print(f"Scan error: {e}")
            
        self.scan_finished.emit(whitelist_dirs, matched_files)

    def stop(self):
        self.is_running = False

class ActionRunnerThread(QThread):
    """
    Seçili dosyaları verilen işlem listesine göre işler.
    """
    progress = pyqtSignal(int, int, str) # current, total, status_message
    finished = pyqtSignal(list) # errors list
    
    def __init__(self, files, tasks):
        super().__init__()
        self.files = files
        self.tasks = tasks
        self.is_running = True
        
    def run(self):
        total_steps = len(self.files) * len(self.tasks)
        if total_steps == 0:
            self.finished.emit([])
            return
            
        current_step = 0
        errors = []
        
        # Dosya listesini kopyala çünkü işlem sırasında değişebilir
        processing_files = self.files.copy()
        
        # Global Counters for tasks
        task_info = []
        for key, data in self.tasks:
            info = {"key": key, "data": data}
            if key == "seq_rename":
                info["counter"] = data.get("start", 1)
            elif key == "csv" or key == "excel":
                info["report_data"] = []
            elif key == "merge":
                info["merged_content"] = []
            task_info.append(info)
            
        processed_count = 0
        total_files = len(processing_files)
        
        for idx, file_path in enumerate(processing_files):
            if not self.is_running: break
            
            current_file = Path(file_path)
            
            if not current_file.exists():
                errors.append(f"Bulunamadı: {current_file}")
                continue
                
            original_file = current_file # Referans
            
            # Pipeline: Dosyayı görevlerden geçir
            for t_idx, t_info in enumerate(task_info):
                key = t_info["key"]
                data = t_info["data"]
                
                try:
                    if key == "seq_rename":
                        pattern = data.get("pattern", "File_{n}")
                        start = data.get("start", 1)
                        step = data.get("step", 1)
                        pad = data.get("pad", 3)
                        
                        counter = t_info["counter"]
                        num_str = str(counter).zfill(pad)
                        new_name = pattern.replace("{n}", num_str)
                        # Uzantıyı koru
                        if "." not in new_name and current_file.suffix:
                             new_name += current_file.suffix
                             
                        new_path = current_file.with_name(new_name)
                        
                        # Çakışma kontrolü
                        if new_path.exists() and new_path != current_file:
                             # Basit çakışma çözümü: _1 ekle
                             stem = new_path.stem
                             new_path = new_path.with_name(f"{stem}_1{new_path.suffix}")
                        
                        current_file.rename(new_path)
                        current_file = new_path # Pipeline için güncelle
                        t_info["counter"] += step
                        
                    elif key == "prefix_suffix":
                        prefix = data.get("prefix", "")
                        suffix = data.get("suffix", "")
                        
                        stem = current_file.stem
                        ext = current_file.suffix
                        new_name = f"{prefix}{stem}{suffix}{ext}"
                        new_path = current_file.with_name(new_name)
                        current_file.rename(new_path)
                        current_file = new_path
                        
                    elif key == "find_replace":
                        find = data.get("find", "")
                        replace = data.get("replace", "")
                        case = data.get("case", False)
                        
                        name = current_file.name
                        if not case:
                            # Case insensitive replace is tricky properly, simpler approach:
                            if find.lower() in name.lower():
                                # Re-construct using regex for case-insensitive
                                pattern = re.compile(re.escape(find), re.IGNORECASE)
                                new_name = pattern.sub(replace, name)
                                new_path = current_file.with_name(new_name)
                                current_file.rename(new_path)
                                current_file = new_path
                        else:
                            if find in name:
                                new_name = name.replace(find, replace)
                                new_path = current_file.with_name(new_name)
                                current_file.rename(new_path)
                                current_file = new_path

                    elif key == "change_ext":
                        new_ext = data.get("new_ext", "").strip()
                        if not new_ext.startswith("."):
                            new_ext = "." + new_ext
                        new_path = current_file.with_suffix(new_ext)
                        current_file.rename(new_path)
                        current_file = new_path

                    elif key == "copy":
                        target = Path(data.get("target"))
                        conflict = data.get("conflict", "Atla") # Üzerine Yaz, Atla, Kopya Oluştur
                        
                        if not target.exists():
                            target.mkdir(parents=True, exist_ok=True)
                            
                        dest_path = target / current_file.name
                        
                        if dest_path.exists():
                            if conflict == "Üzerine Yaz":
                                shutil.copy2(current_file, dest_path)
                            elif conflict == "Kopya Oluştur":
                                stem = dest_path.stem
                                dest_path = target / f"{stem}_copy{dest_path.suffix}"
                                shutil.copy2(current_file, dest_path)
                            # else: Atla -> do nothing
                        else:
                            shutil.copy2(current_file, dest_path)
                        
                    elif key == "flatten":
                         parent = current_file.parent.parent
                         if parent.exists():
                             dest = parent / current_file.name
                             current_file.rename(dest)
                             current_file = dest

                    elif key == "secure_del":
                        method = data.get("method")
                        passes = 1
                        zeros = False
                        
                        # "NIST 800-88 Clear (1-Pass)" -> passes=1, zeros=True
                        # "NIST 800-88 Purge (3-Pass Random)" -> passes=3, zeros=False
                        # "Zero Fill (1-Pass)" -> passes=1, zeros=True
                        
                        if "Clear" in method or "Zero" in method:
                            passes = 1
                            zeros = True
                        elif "Purge" in method or "3-Pass" in method:
                            passes = 3
                            zeros = False # Random
                        
                        size = current_file.stat().st_size
                        with open(current_file, "r+b") as f:
                            for i in range(passes):
                                f.seek(0)
                                if zeros and i == passes-1:
                                    # Last pass zeros or ONLY pass zeros (NIST Clear)
                                    chunk_size = 64 * 1024
                                    remaining = size
                                    while remaining > 0:
                                        write_sz = min(chunk_size, remaining)
                                        f.write(b'\x00' * write_sz)
                                        remaining -= write_sz
                                else:
                                    # Random
                                    chunk_size = 64 * 1024
                                    remaining = size
                                    while remaining > 0:
                                        write_sz = min(chunk_size, remaining)
                                        f.write(os.urandom(write_sz))
                                        remaining -= write_sz
                                f.flush()
                                os.fsync(f.fileno())
                                
                        # Rename to random trash before deleting to hide metadata
                        try:
                            new_name = secrets.token_hex(12) + ".tmp"  # Kriptografik güvenli
                            new_path = current_file.with_name(new_name)
                            current_file.rename(new_path)
                            current_file = new_path
                        except: pass
                        
                        current_file.unlink()
                        break 
                    
                    elif key == "merge":
                        try:
                            content = current_file.read_text(encoding='utf-8', errors='ignore')
                            t_info["merged_content"].append(content)
                        except: pass
                    
                    elif key in ["csv", "excel"]:
                         cols = data.get("columns", [])
                         row = {}
                         stat = current_file.stat()
                         
                         if "Dosya Adı" in cols: row["Dosya Adı"] = current_file.name
                         if "Yol" in cols: row["Yol"] = str(current_file)
                         if "Boyut" in cols: row["Boyut"] = str(stat.st_size)
                         if "Tarih" in cols: row["Tarih"] = datetime.datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
                         
                         if "Hash" in cols:
                             # MD5 Hash Calculation
                             h = hashlib.sha256()  # MD5 yerine SHA-256 (OWASP uyumlu)
                             with open(current_file, "rb") as f:
                                 while chunk := f.read(8192):
                                     h.update(chunk)
                             row["Hash"] = h.hexdigest()
                             
                         t_info["report_data"].append(row)
                         
                except Exception as e:
                    errors.append(f"{current_file.name} - {key}: {str(e)}")
            
            processed_count += 1
            self.progress.emit(processed_count, total_files, f"İşleniyor: {current_file.name}")
        
        # Post-Processing Tasks
        for t_info in task_info:
            key = t_info["key"]
            data = t_info["data"]
            try:
                if key == "merge":
                    out_name = data.get("output", "merged.txt")
                    sep_opt = data.get("sep")
                    sep_map = {"Satır Sonu (\\n)": "\n", "Virgül": ",", "Boşluk": " "}
                    real_sep = sep_map.get(sep_opt, "\n")
                    
                    if self.files and len(t_info["merged_content"]) > 0:
                         first_file = Path(self.files[0])
                         out_path = first_file.parent / out_name
                         out_path.write_text(real_sep.join(t_info["merged_content"]), encoding='utf-8')
                
                elif key == "csv" or key == "excel":
                    out_path_str = data.get("output_path")
                    if not out_path_str:
                        out_path = Path.home() / "Desktop" / "FileArchitect_Report.csv"
                    else:
                        out_path = Path(out_path_str)
                    
                    # Ensure parent dir exists
                    out_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    cols = data.get("columns", ["Dosya Adı"])
                    encoding = data.get("encoding", "utf-8")
                    sep_map = {"Virgül (,)": ",", "Noktalı Virgül (;)": ";"}
                    delimiter = sep_map.get(data.get("sep"), ",")
                    
                    # Excel uyumluluğu için BOM ekle
                    if encoding == "UTF-8" and "Excel" in key:
                        encoding = "utf-8-sig"
                        
                    with open(out_path, 'w', newline='', encoding=encoding) as csvfile:
                         writer = csv.DictWriter(csvfile, fieldnames=cols, delimiter=delimiter)
                         writer.writeheader()
                         writer.writerows(t_info["report_data"])
                         
            except Exception as e:
                errors.append(f"Post-process {key}: {str(e)}")
                
        self.finished.emit(errors)

    def stop(self):
        self.is_running = False
