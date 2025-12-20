# Uygulama Planı - Gelişmiş Filtre Sistemi

## Hedef
Kullanıcıların birden fazla filtreyi yapılandırmasına, eklemesine ve yönetmesine olanak tanıyan, `FiltersPanel`'in sağ bölümünde kapsamlı bir Filtre Ayarları Arayüzü oluşturmak.

## Kullanıcı İncelemesi Gereklidir
> [!IMPORTANT]
> **Yerleşim Stratejisi**: `FiltersPanel`'in sağ tarafı, seçilen filtre butonuna göre farklı formlar gösteren bir `QStackedWidget` yapısına dönüştürülecektir.
> **Otomatik Seçim Kaldırma Mantığı**: Butonların "Otomatik Seçimi Kaldırma" (1 sn gecikme) özelliği görsel geri bildirim olarak korunacak, ancak *asıl filtre* eklendikten sonra "Aktif Filtreler" listesinde görünür ve kalıcı olacaktır.

## Önerilen Değişiklikler

### 1. FiltersPanel Mimarisi Güncellemesi
*   **Düzen (Layout)**: Sağdaki `Stretch` (boşluk), özel bir kapsayıcıya (`QWidget`) dönüştürülecek.
*   **Bileşenler**:
    *   `FilterFormStack` (QStackedWidget): Her filtre tipi için (Uzantı, Boyut vb.) özel formları tutar.
    *   `ActiveFiltersView` (FlowLayout/HBoxLayout): Eklenen filtreleri kaldırılabilir etiketler (örn. `[ Uzantı: .py (x) ]`) olarak gösterir.

### 2. Filtre Formları (Detaylı İşlevsellik)

#### A. Ortak Kontroller (Tüm Formlar İçin)
*   **Alt Butonlar**:
    *   `Ekle`: Girdiyi doğrular, filtre objesi oluşturur, aktif listeye ekler, seçimi temizler.
    *   `Sıfırla`: Mevcut form girdilerini temizler.
    *   `İptal`: Formu gizler (veya butonu hemen pasif hale getirir).

#### B. Özel Formlar
1.  **Uzantı**
    *   *Girdi*: `QLineEdit` (virgülle ayrılmış, örn. "jpg, png").
    *   *Doğrulama*: Noktaları kaldır, boşlukları temizle.
2.  **Dosya Adı**
    *   *Girdi*: `QLineEdit` (Arama metni).
    *   *Seçenekler*: `Büyük/Küçük Harf Duyarlı` (CheckBox), `Tam Eşleşme` (CheckBox).
3.  **Metin** & **Metin Yok**
    *   *Girdi*: `QLineEdit` (Arama metni).
    *   *Not*: "Metin Yok", "İçerik ŞUNU İÇERMEZ" anlamına gelir.
4.  **Regex**
    *   *Girdi*: `QLineEdit` (Desen).
    *   *Doğrulama*: `re.compile(desen)` geçerli mi kontrol et. Geçersizse hata göster.
5.  **Boyut**
    *   *Girdiler*:
        *   Operatör: `>`, `<`, `=`
        *   Değer: `DoubleSpinBox` (0-9999).
        *   Birim: `B`, `KB`, `MB`, `GB`.
6.  **Tarih (Oluşturma/Değiştirme)**
    *   *Girdiler*:
        *   Başlangıç Tarihi (`QDateEdit`).
        *   Bitiş Tarihi (`QDateEdit`).
        *   Başlangıç/Bitiş için onay kutuları (açık aralıklar için, örn. "2023 sonrası").
7.  **Mantıksal/Basit Filtreler (Boş Dosya, Şifreli, Gizli)**
    *   *Girdi*: Basit bir etiket "Bu filtreyi eklemek istiyor musunuz?" veya direkt Ekleme.
    *   *Mantık*: Aç/Kapa (Toggle) işlevi görür.

### 3. Aktif Filtre Mantığı
*   **Etiket (Chip) Widget**: Özel widget `FilterChip(metin, filtre_verisi)`.
    *   Görsel: Arka plan rengi, Metin, Kapat (X) ikonu.
    *   Sinyal: `removed()` -> filtreyi kaldırır ve listeyi yeniler.
*   **Filtre Yöneticisi**:
    *   Aktif `Filtre` objeleri listesi.
    *   Tüm dosyaları döngüye sok -> Her dosyayı TÜM aktif filtrelere karşı kontrol et (VE mantığı).
    *   **Mantık**: Bir dosyanın görünmesi için TÜM aktif koşulları sağlaması gerekir.

### 4. Entegrasyon
*   `FiltersPanel`, `filters_changed(aktif_filtreler_listesi)` sinyali yayar.
*   `MainWindow` sinyali alır -> `SourcePanel` proxy modelini veya manuel filtrelemeyi çağırır.
*   **İyileştirme**: `QFileSystemModel` filtrelemesi sınırlı olduğu için (sadece isim), ağaç görünümüne (`tree view`) bağlı bir `QSortFilterProxyModel` alt sınıfı (`CustomFilterProxy`) gereklidir.
    *   `filterAcceptsRow`: Mantığı uygular (İsim, Boyut, Tarih, İçerik kontrolleri).

## Doğrulama Planı

### 5. Filtre Özellikleri ve Stilleri (Kullanıcı Düzenlemesi İçin)

Her bir filtre butonu ve ilişkili formun teknik ve görsel detayları aşağıdadır. Lütfen bu bölümü düzenleyerek tercihlerinizi belirtin.

#### Genel Stil (Tüm Formlar)
*   **Başlık Fontu**: 13px, Kalın, Renk: #333333
*   **Etiket (Label) Fontu**: 11px, Renk: #555555
*   **Input Yüksekliği**: 24px
*   **Butonlar (Ekle/Sıfırla/İptal)**:
    *   Yükseklik: 26px
    *   Ekle Butonu Rengi: #E0E0E0 (Hover: #D0D0D0)
    *   Kenarlık: 1px solid #CCCCCC (Radius: 3px)

---

#### 1. Uzantı Filtresi
*   **Amaç**: Dosyaları uzantılarına göre filtreler.
*   **Girdiler**:
    *   `QLineEdit` (Placeholder: "jpg, png, txt")
*   **Mantik**:
    *   Nokta ile veya noktasız giriş kabul edilir (örn. `.jpg` veya `jpg`).
    *   Birden fazla uzantı virgül ile ayrılır.
*   **Stil**: Standart Text Input.

#### 2. Dosya Adı Filtresi
*   **Amaç**: Dosya isminde belirli bir metni arar.
*   **Girdiler**:
    *   `QLineEdit` (Arama Metni)
    *   `QCheckBox`: "Büyük/Küçük Harf Duyarlı"
    *   `QCheckBox`: "Tam Eşleşme" (abc -> abc.txt (Hayır), abc (Evet))
    *   `QCheckBox`: "Tersini Al" (İçermeyenleri göster)
*   **Stil**: Checkbox'lar dikey hizalı, aralarındaki boşluk 4px.

#### 3. Metin (İçerik) Filtresi
*   **Amaç**: Dosya *içeriğinde* metin arar.
*   **Girdiler**:
    *   `QLineEdit` (Aranacak Metin)
    *   `QCheckBox`: "Büyük/Küçük Harf Duyarlı"
*   **Uyarı**: Büyük dosyalarda performans düşürebilir (uyarı ikonu eklenebilir).

#### 4. Regex Filtresi
*   **Amaç**: Gelişmiş desen eşleştirme.
*   **Girdiler**:
    *   `QLineEdit` (Regex Deseni, örn: `^image_\d+\.png$`)
*   **Validation**: Geçersiz regex girilirse "Ekle" butonu pasif olur veya input kırmızı çerçeve olur.

#### 5. Metin Yok (İçerik)
*   **Amaç**: İçeriğinde belirli metni *barındırmayan* dosyaları bulur.
*   **Girdiler**:
    *   `QLineEdit` (Olmayan Metin)

#### 6. Boyut Filtresi
*   **Amaç**: Dosya boyutuna göre süzme.
*   **Girdiler**:
    *   `QComboBox` (Operatör): [Büyüktür (>), Küçüktür (<), Eşittir (=)]
    *   `QDoubleSpinBox` (Değer): 0 - 999999
    *   `QComboBox` (Birim): [Byte, KB, MB, GB]
*   **Layout**: `FormLayout` (Etiket: Kontrol).

#### 7. Boş Dosya
*   **Amaç**: 0 byte boyutundaki dosyaları bulur.
*   **Girdiler**: Yok (Sadece onay/bilgi etiketi).
*   **Mantik**: Otomatik olarak "Size = 0 Byte" filtresi oluşturur.

#### 8. Oluşturma / Değişiklik Tarihi
*   **Amaç**: Tarih aralığına göre filtreleme.
*   **Girdiler**:
    *   `QDateEdit` (Başlangıç) - Opsiyonel (CheckBox ile aktifleşir)
    *   `QDateEdit` (Bitiş) - Opsiyonel
    *   Format: `dd.MM.yyyy`
*   **Stil**: Takvim popup özellikli.

#### 9. Şifreli / Gizli / Salt Okunur
*   **Amaç**: Dosya özniteliklerine göre filtreleme.
*   **Girdiler**: Yok (Onay etiketi).
*   **Mantik**: Windows özniteliklerini (Hidden, ReadOnly) kontrol eder.

