# File Architect Pro

<p align="center">
  <img src="icons/app.ico" alt="File Architect Pro" width="128">
</p>

<p align="center">
  <strong>Profesyonel Dosya Yönetim ve Organizasyon Aracı</strong>
</p>

<p align="center">
  <a href="#özellikler">Özellikler</a> •
  <a href="#kurulum">Kurulum</a> •
  <a href="#kullanım">Kullanım</a> •
  <a href="#güvenlik">Güvenlik</a> •
  <a href="#derleme">Derleme</a>
</p>

---

## Özellikler

### 📁 Dosya Filtreleme
- **Uzantı Filtresi**: Belirli dosya türlerini seçin (.txt, .pdf, .jpg vb.)
- **Metin Arama**: Dosya içeriğinde RAM-efficient arama
- **Boyut Filtresi**: KB, MB, GB cinsinden boyut sınırlaması
- **Tarih Filtresi**: Oluşturma/değiştirme tarihine göre filtreleme
- **Regex Desteği**: Gelişmiş desen eşleştirme (ReDoS korumalı)

### ⚡ Aksiyon Sistemi
- **Sıralı Yeniden Adlandırma**: Dosyaları otomatik numaralandırma
- **Bul & Değiştir**: Dosya adlarında toplu değişiklik
- **Kopyala**: Çakışma yönetimi ile güvenli kopyalama
- **Güvenli Silme**: NIST 800-88 standardında veri imhası
- **Metin Birleştir**: Birden fazla dosyayı tek dosyada birleştirme
- **CSV/Excel Rapor**: Dosya listesi ve hash raporları

### 🎨 Modern Arayüz
- **Koyu/Açık Tema**: Sistem temasına otomatik uyum
- **Türkçe/İngilizce**: Tam çoklu dil desteği
- **Ağaç Görünümü**: Klasör yapısını koruyarak önizleme
- **Gerçek Zamanlı İlerleme**: İşlem durumu takibi

---

## Kurulum

### Gereksinimler
- Python 3.10+
- PyQt6

### Hızlı Başlangıç

```bash
# Depoyu klonlayın
git clone https://github.com/AhmetAlemdar/File-Architect-Pro.git
cd File-Architect-Pro

# Bağımlılıkları yükleyin
pip install -r requirements.txt

# Uygulamayı başlatın
python main.py
```

---

## Kullanım

1. **Kaynak Klasör Seçimi**: Sol panelden klasör seçin veya "Gözat" butonunu kullanın
2. **Filtre Ekleme**: Filtre butonlarından birini seçin ve değerleri girin
3. **Aksiyon Ekleme**: Aksiyon listesinden işlem seçin ve ayarlayın
4. **Çalıştırma**: "Tüm Aksiyonları Çalıştır" butonuna tıklayın

---

## Güvenlik

Bu uygulama OWASP güvenlik standartlarına uygun olarak geliştirilmiştir:

| Güvenlik Özelliği | Açıklama |
|-------------------|----------|
| **ReDoS Koruması** | Regex timeout mekanizması ile CPU aşırı kullanımı engellenir |
| **Path Traversal** | Dizin gezinme saldırıları engellenir |
| **TOCTOU Koruması** | Race condition güvenlik açıkları kapatıldı |
| **SHA-256 Hash** | MD5 yerine güvenli hash algoritması |
| **Symlink Kontrolü** | Sembolik bağlantılar atlanır |
| **Dosya Limiti** | DoS koruması için 100.000 dosya limiti |

---

## Derleme

### Standalone .exe Oluşturma

```batch
# build.bat dosyasını çalıştırın
build.bat
```

> ⚠️ İlk derleme sırasında MinGW derleyicisi gerekebilir. Script size soracaktır.

### Kurulum Dosyası Oluşturma

1. [Inno Setup](https://jrsoftware.org/isinfo.php) indirin ve kurun
2. `installer.iss` dosyasını Inno Setup'ta açın
3. "Compile" butonuna tıklayın
4. Çıktı: `installer_output/FileArchitectPro_Setup_v1.0.exe`

---

## Lisans

Copyright © 2025 Ahmet Alemdar. Tüm Hakları Saklıdır.

---

## Katkıda Bulunma

1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit edin (`git commit -m 'Add amazing feature'`)
4. Push edin (`git push origin feature/amazing-feature`)
5. Pull Request açın
