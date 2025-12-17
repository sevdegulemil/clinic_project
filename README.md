### Kurulum ve Çalıştırma
 Gereksinimler
Docker
Docker Compose
Python veya virtualenv kurmanıza gerek yoktur. Tüm servisler Docker içinde çalışır.
 Projeyi Klonlayın
git clone https://github.com/kullaniciadi/solix-dent.git
cd solix-dent
 Docker Servislerini Başlatın
docker compose up --build
Bu komut aşağıdaki servisleri ayağa kaldırır:
Django Backend
PostgreSQL
Redis
Veritabanı Migrasyonları
Yeni bir terminal açın:
docker compose exec backend python manage.py migrate
Superuser Oluşturma (Opsiyonel)
docker compose exec backend python manage.py createsuperuser
Uygulamaya Erişim




Proje Yapısı
solix_dent_clinic/
├── login/          # Giriş, çıkış ve ana sayfa
├── user/           # Hasta profili ve hasta sayfaları
├── doctor/         # Doktor paneli, slot ve bekleme listesi
├── assets/         # Statik görseller (logo, ikonlar)
├── templates/      # HTML template dosyaları
├── docker-compose.yml
└── manage.py
Temel Özellikler
Doktor Paneli
Günlük randevuları görüntüleme
Slot iptali
Bekleme listesini yönetme
Doluluk oranı takibi
 Hasta Paneli
Tarih, branş ve doktora göre randevu arama
Aynı gün tek randevu kısıtı
Dolu slotlar için bekleme listesine katılma
Bekleme Listesi Mantığı
Slot boşalınca ilk sıradaki hasta bilgilendirilir
30 dakika içinde onaylanmazsa sıradaki hastaya geçilir
Sıra biterse slot tekrar herkese açılır
 Güvenlik ve Notlar
Django session bazlı authentication kullanılır
login_required ile yetkilendirme sağlanır
Aynı gün aynı doktora birden fazla randevu engellenir
Redis şu an altyapı olarak eklenmiştir (ileride concurrency için genişletilebilir)
Geliştirme Notu
Bu proje bir case / öğrenme projesidir. Kod yapısı özellikle aşırı soyutlanmamış, okunabilir ve geliştirilebilir tutulmuştur.
Gelecek Geliştirmeler
Redis ile slot locking (SETNX)
Gerçek zamanlı bildirimler
DRF API ayrımı
Rol bazlı dashboard yönlendirme
