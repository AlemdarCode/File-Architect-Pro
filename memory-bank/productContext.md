# Ürün Bağlamı

## Proje Adı
File-Architect-Pro

## Tanım
Python ve PyQt6 ile oluşturulmuş gelişmiş bir dosya yönetimi ve mimari aracı. Kullanıcıların dizin yapılarını görselleştirmesine, dosyaları çeşitli kriterlere göre filtrelemesine ve toplu işlemler gerçekleştirmesine olanak tanır.

## Temel Özellikler
1.  **Kaynak Dizin Tarayıcısı**:
    *   Dosya sisteminin ağaç görünümü.
    *   Özel çizilmiş hiyerarşi çizgileri (ortalanmış).
    *   Klasör genişletme mantığı (derinlemesine otomatik genişletme).
2.  **Filtre Paneli**:
    *   Açılıp kapanabilir filtreler (Uzantı, İsim, Regex, Boyut vb.).
    *   Merkezi sütun yerleşimi.
3.  **İşlem (Aksiyon) Paneli**:
    *   Filtre paneli ile simetrik yapı.
    *   Sol tarafta operasyon butonları, sağda dinamik ayar paneli (`ActionSettingsPanel`).
    *   Aktif aksiyonlar listesi ("chipler").
4.  **Dosya Önizleme Paneli**:
    *   Detay görünümü (İsim, Tip, Boyut, Değiştirilme Tarihi).
    *   Desteklenen dosyalar için metin önizleme.
    *   İşlem yapılandırma arayüzleri (desen girişi vb.).

## Tasarım Felsefesi
*   **Profesyonel Arayüz**: Özel stil, "Fusion" stili temeli, varsayılan sistem mavi vurgularının kaldırılması.
*   **Estetik**: Minimalist, temiz çizgiler, özel renk paleti (#E7E6E2, #F0EFEB, #F9F8F2).
*   **Duyarlı (Responsive)**: Paneller orantılı olarak yeniden boyutlanır.
