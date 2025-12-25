# Technical Context

## Stack
* **Language**: Python 3.x
* **GUI Framework**: PyQt6
* **Operating System**: Windows (specifically optimized for Windows look and feel integration, but styled OS-independently).

## Constraints
* **Single File**: Preference to keep logic in `main.py` for sharing/easy running (even though user has folders like `views/`, driver is `main.py`).
* **Memory Bank**: Documentation must be kept in `memory-bank/` folder.

## Dependencies
* `PyQt6` (GUI foundation)
* `proxymodel.py` (Local Proxy Model component)
* `workers.py` (Background scanner and worker threads)
* Standard Python libraries (`pathlib`, `sys`, `datetime`, `re`, `uuid`, `os`).

## Security
* OWASP compliant security improvements
* SHA-256 for file hashing
* ReDoS protection with timeout
* Path traversal protection
* TOCTOU/EAFP pattern fix
