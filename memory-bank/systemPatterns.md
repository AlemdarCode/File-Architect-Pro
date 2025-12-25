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
*   `FilterSettingsPanel`: Filtre ayarları için sağ taraftaki form yığını (StackedWidget). Sabit genişlik (280px).
*   `FilterChip`: Aktif filtreler için etiket widget'ı. Kırmızı yuvarlak X butonu ile silme.
*   `ActionsPanel`: Operasyon butonlarını barındırır.
*   `ActionSettingsPanel`: Aksiyon ayarları için sağ panel (FilterSettingsPanel ile simetrik yapı). Sabit genişlik (300px).
*   `PreviewPanel`: Dosya listesini (`QListView` veya `QTreeView`) gösteren ana panel. `PreviewProxyModel` kullanarak gelişmiş filtreleme yapar.
*   `ModernSpinBox`: Özel tasarımlı sayı girişi widget'ı. QIntValidator ile sadece sayı girişi.
*   `PreviewProxyModel`: `QSortFilterProxyModel` tabanlı akıllı filtreleme katmanı.

## Form Widget Yönetimi
*   `form_widgets` dictionary: Her form türü için widget referanslarını saklar.
*   Widget türleri: `input` (QLineEdit), `case/exact/invert` (QCheckBox), `val` (ModernSpinBox), `op/unit` (QComboBox), `start/end` (QDateEdit).
*   `_on_reset()`: Mevcut formu sıfırlar.
*   `_get_filter_description()`: Gerçek form değerlerini okuyup açıklama oluşturur.

## Tasarım Kuralları
*   **Mavi Vurgu Yok**: Palet ve QSS ile kesinlikle engellenmiştir.
*   **Ortalanmış Hiyerarşi Çizgileri**: Çizgiler dosya/klasör ikonunun merkeziyle hizalanmalıdır.
*   **Kompakt Mod**: Küçük dolgularla (padding) yoğun yerleşim.
*   **Dinamik Butonlar**: Ana butonlar (stretch 2), İptal butonu (stretch 1).
*   **Tam Ekran Desteği**: Panel yapıları sabit genişlikle korunur, sağa stretch eklenir.

## Yeni Mimari Desenler

### Akıllı Filtreleme Katmanı (Proxy Model Pattern)
Geleneksel `QFileSystemModel` kısıtlamalarını aşmak için `PreviewProxyModel` kullanılır. Bu katman:
- Kaynak modelden gelen verileri UI'a ulaşmadan önce filtreler.
- Boyut, Tarih, Regex gibi gelişmiş mantıkları koordine eder.
- `beginResetModel`/`endResetModel` ile atomik UI güncellemeleri sağlar.

### Zincirleme Genişletme Deseni (Chain-Expansion Pattern)
`QFileSystemModel`'in asenkron yükleme doğasını yönetmek için kullanılır:
1. `directoryLoaded(path)` sinyali dinlenir.
2. Yüklenen dizin için `mapFromSource` ile proxy indeksi alınır ve `expand()` edilir.
3. Whitelist aktifse, sadece listedeki klasörler için `fetchMore()` çağrılarak hiyerarşi hedefe doğru açılır.

### Arka Plan Tarama Deseni (Background Scanner Pattern)
Arayüzü dondurmadan disk üzerinde derin tarama yapmak için kullanılır:
- `QThread` (FastScannerThread) üzerinden yürütülür.
- `os.walk` ile düşük seviyeli ve hızlı dosya sistemi erişimi sağlar.
- Sonuçları "Whitelist" olarak arayüze (PreviewPanel) sinyal ile iletir.

### Beyaz Liste (Whitelist) Filtreleme Deseni
Proxy model seviyesinde ağaç budama için kullanılır:
- Tarayıcıdan gelen geçerli klasör yolları bir `set` içinde tutulur.
- `filterAcceptsRow` içinde sadece bu listedeki klasörlerin geçişine izin verilir.
- Bu, TreeView'un gereksiz binlerce klasörü işlemesini ve çizmesini engeller.
