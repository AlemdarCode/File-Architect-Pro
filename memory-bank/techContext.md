# Teknik Bağlam

## Yığın (Stack)
*   **Dil**: Python 3.x
*   **GUI Çerçevesi**: PyQt6
*   **İşletim Sistemi**: Windows (özellikle Windows görünüm ve hissi entegrasyonu için optimize edilmiş, ancak OS'den bağımsız stillendirilmiş).

## Kısıtlamalar
*   **Tek Dosya**: Paylaşım/kolay çalıştırma için mantığın `main.py` içinde tutulması tercihi (kullanıcının `views/` gibi klasörleri olsa da sürücü `main.py`'dir).
*   **Hafıza Bankası**: Dokümantasyon `memory-bank/` klasöründe tutulmalıdır.

## Bağımlılıklar
*   `PyQt6` (GUI temeli)
*   `proxymodel.py` (Yerel Proxy Model bileşeni)
*   `workers.py` (Arka plan tarayıcı ve iş parçacıkları)
*   Standart Python kütüphaneleri (`pathlib`, `sys`, `datetime`, `re`, `uuid`, `os`).
