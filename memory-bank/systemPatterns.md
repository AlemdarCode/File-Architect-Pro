# Sistem Desenleri

## Mimari
*   **Tekil Betik (Monolithic Script)**: Şu anda `main.py` tüm uygulama mantığını içerir (`MainWindow`, `SourcePanel`, `FiltersPanel`, `ActionsPanel`, `PreviewPanel` sınıfları buradadır).
*   **Olay Güdümlü (Event Driven)**: Bileşenler arası iletişim için PyQt6 Signal/Slot mekanizmasına yoğun bağımlılık (örn. Kaynak panelindeki seçim değişikliği Önizleme panelini tetikler).

## Arayüz Desenleri
*   **Özel Boyama (Custom Painting)**: Öğeler ve çizgiler genellikle Delegate'ler veya `paintEvent` geçersiz kılmalarıyla özel olarak çizilir (`GradientLine`, `TreeDelegate`).
*   **Stil Sayfası (QSS)**: Global `STYLE_SHEET` sabiti temel görünümü tanımlar.
*   **Düzenler (Layouts)**: İç içe `QVBoxLayout` ve `QHBoxLayout`, ana ızgara için `QGridLayout` ile birleştirilmiştir.

## Ana Sınıflar
*   `MainWindow`: Yerleşimi düzenler ve panelleri oluşturur.
*   `SourcePanel`: `QFileSystemModel` ile `QTreeView`. Dizin navigasyonunu yönetir.
*   `FiltersPanel`: Filtreleme butonlarını barındırır.
*   `FilterSettingsPanel`: Filtre ayarları için sağ taraftaki form yığını (StackedWidget). Dinamik genişlik.
*   `ActionsPanel`: Operasyon butonlarını barındırır.
*   `ActionSettingsPanel`: Aksiyon ayarları için sağ panel (FilterSettingsPanel ile simetrik yapı).
*   `PreviewPanel`: Dosya bilgisi veya işlem yapılandırma formlarını gösteren `QStackedWidget`.

## Tasarım Kuralları
*   **Mavi Vurgu Yok**: Palet ve QSS ile kesinlikle engellenmiştir.
*   **Ortalanmış Hiyerarşi Çizgileri**: Çizgiler dosya/klasör ikonunun merkeziyle hizalanmalıdır.
*   **Kompakt Mod**: Küçük dolgularla (padding) yoğun yerleşim.
