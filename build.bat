@echo off
chcp 65001 >nul
echo ============================================================
echo   File Architect Pro - PyInstaller Derleme Scripti
echo   Ahmet Alemdar - 2025
echo ============================================================
echo.

echo [*] Derleme basliyor... (Bu islem 3-10 dakika surebilir)
echo.

python -m PyInstaller --noconfirm --onedir --windowed ^
    --name "FileArchitectPro" ^
    --icon "icons/app.ico" ^
    --add-data "icons;icons" ^
    main.py

echo.
echo [*] Ikonlar kopyalaniyor...
xcopy /E /I /Y "icons" "dist\FileArchitectPro\icons" >nul

echo.
if exist "dist\FileArchitectPro\FileArchitectPro.exe" (
    echo ============================================================
    echo   [OK] Derleme basariyla tamamlandi!
    echo   Cikti: dist\FileArchitectPro\
    echo ============================================================
) else (
    echo [!] Derleme tamamlanamadi.
)

echo.
pause
