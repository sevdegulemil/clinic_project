# 🦷 Solix Dent - Diş Kliniği Randevu Sistemi

Solix Dent, Django ve Docker kullanılarak geliştirilmiş, doktor ve hasta yönetimini kolaylaştıran, bekleme listesi algoritmalarına sahip modern bir randevu takip sistemidir.

---

## 🚀 Kurulum ve Çalıştırma

### 🛠 Gereksinimler
* **Docker** ve **Docker Compose**
* *Not: Python veya virtualenv kurmanıza gerek yoktur. Tüm servisler izole bir şekilde Docker içinde çalışır.*

### 1. Projeyi Klonlayın
```bash
git clone [https://github.com/kullaniciadi/solix-dent.git](https://github.com/kullaniciadi/solix-dent.git)
cd solix-dent

### 2. Docker Servislerini Başlatın
Bash
cd clinic_project/solix_dent_clinic dizinine gidin

docker compose up --build

Bu komut aşağıdaki servisleri otomatik olarak yapılandırır ve başlatır:

🐍 Django Backend

🐘 PostgreSQL (Veri Depolama)

⚡ Redis (Altyapı/Cache)

3. Veritabanı Yapılandırması
Servisler ayağa kalktıktan sonra yeni bir terminal açarak veritabanı tablolarını oluşturun:
docker compose exec backend python manage.py migrate

4. Yönetici Paneli (Opsiyonel)
docker compose exec backend python manage.py createsuperuser

Tabii ki, projenin tamamını tek bir dosya içeriği olarak aşağıda hazırladım. Bu metnin tamamını kopyalayıp projenin ana dizinindeki README.md dosyasının içine yapıştırabilirsin.Aşağıdaki blok, GitHub'ın en iyi şekilde render edeceği (görselleştireceği) formatta düzenlenmiştir:Markdown# 🦷 Solix Dent - Diş Kliniği Randevu Sistemi

Solix Dent, Django ve Docker kullanılarak geliştirilmiş, doktor ve hasta yönetimini kolaylaştıran, bekleme listesi algoritmalarına sahip modern bir randevu takip sistemidir.

---

## 🚀 Kurulum ve Çalıştırma

### 🛠 Gereksinimler
* **Docker** ve **Docker Compose**
* *Not: Python veya virtualenv kurmanıza gerek yoktur. Tüm servisler izole bir şekilde Docker içinde çalışır.*

### 1. Projeyi Klonlayın
```bash
git clone [https://github.com/kullaniciadi/solix-dent.git](https://github.com/kullaniciadi/solix-dent.git)
cd solix-dent
2. Docker Servislerini BaşlatınBashdocker compose up --build
Bu komut aşağıdaki servisleri otomatik olarak yapılandırır ve başlatır:🐍 Django Backend🐘 PostgreSQL (Veri Depolama)⚡ Redis (Altyapı/Cache)3. Veritabanı YapılandırmasıServisler ayağa kalktıktan sonra yeni bir terminal açarak veritabanı tablolarını oluşturun:Bashdocker compose exec backend python manage.py migrate
4. Yönetici Paneli (Opsiyonel)Sisteme admin olarak giriş yapabilmek için:Bashdocker compose exec backend python manage.py createsuperuser
🌐 Uygulama Sayfaları
Sayfa                    Erişim Linki
🏠 Ana Sayfa             http://localhost:8000
🩹 Hasta Girişi          http://localhost:8000/patient-login/
👨‍⚕️ Doktor Girişi         http://localhost:8000/doctor-login/
⚙️ Admin Panel           http://localhost:8000/admin/

solix_dent_clinic/
├── login/          # Auth işlemleri (Giriş, çıkış ve ana sayfa)
├── user/          Temel Özellikler
🩺 Doktor Paneli
Günlük randevuları anlık görüntüleme.

Slot (randevu saati) iptali ve yönetimi.

Bekleme listesi üzerindeki hastaları takip etme.

Poliklinik doluluk oranı takibi.

👤 Hasta Paneli
Tarih, branş ve doktora göre gelişmiş randevu arama.

Kısıtlama: Aynı gün içinde sadece tek bir randevu alabilme kuralı.

Dolu olan saatler için Bekleme Listesi'ne katılma seçeneği.

⏳ Bekleme Listesi Algoritması
Bir slot boşaldığında, sistem otomatik olarak ilk sıradaki hastayı bilgilendirir.

İlk sıradaki hastanın onaylaması için 30 dakikası vardır.

Onay gelmezse sıra otomatik olarak bir sonraki hastaya geçer.

Liste biterse slot tekrar genel erişime açılır.

🔐 Güvenlik ve Mimari Notlar
Authentication: Django Session bazlı güvenli kimlik doğrulama.

Authorization: Tüm hassas görünümler login_required ile korunmaktadır.

Validasyon: İş mantığı hatalarını önlemek için (aynı gün mükerrer randevu vb.) model ve form seviyesinde kontroller.

Redis: Altyapıda yer almaktadır; ilerleyen aşamalarda concurrency (eşzamanlılık) yönetimi için genişletilecektir.

[!IMPORTANT] Geliştirme Notu: Bu proje bir case/öğrenme çalışmasıdır. Kod yapısı temiz, okunabilir ve geliştirilmeye açık (extensible) tutulmuştur.

🛠 Gelecek Geliştirmeler
[ ] Redis SETNX: Slot kilitleme ile yarış durumlarını (race conditions) önleme.

[ ] Websockets: Gerçek zamanlı bildirim ve sıra takibi.

[ ] REST API: Django Rest Framework entegrasyonu.

[ ] Dashboard: Rol bazlı gelişmiş grafiksel paneller. # Hasta işlemleri (Profil, randevu alma)
├── doctor/         # Doktor işlemleri (Panel, slot ve bekleme listesi)
├── assets/         # Statik dosyalar (Logo, ikonlar)
├── templates/      # Klasik Django HTML template dosyaları
├── docker-compose.yml
└── manage.py

Temel Özellikler
🩺 Doktor Paneli
Günlük randevuları anlık görüntüleme.

Slot (randevu saati) iptali ve yönetimi.

Bekleme listesi üzerindeki hastaları takip etme.

Poliklinik doluluk oranı takibi.

👤 Hasta Paneli
Tarih, branş ve doktora göre gelişmiş randevu arama.

Kısıtlama: Aynı gün içinde sadece tek bir randevu alabilme kuralı.

Dolu olan saatler için Bekleme Listesi'ne katılma seçeneği.

⏳ Bekleme Listesi Algoritması
Bir slot boşaldığında, sistem otomatik olarak ilk sıradaki hastayı bilgilendirir.

İlk sıradaki hastanın onaylaması için 30 dakikası vardır.

Onay gelmezse sıra otomatik olarak bir sonraki hastaya geçer.

Liste biterse slot tekrar genel erişime açılır.

🔐 Güvenlik ve Mimari Notlar
Authentication: Django Session bazlı güvenli kimlik doğrulama.

Authorization: Tüm hassas görünümler login_required ile korunmaktadır.

Validasyon: İş mantığı hatalarını önlemek için (aynı gün mükerrer randevu vb.) model ve form seviyesinde kontroller.

Redis: Altyapıda yer almaktadır; ilerleyen aşamalarda concurrency (eşzamanlılık) yönetimi için genişletilecektir.

[!IMPORTANT] Geliştirme Notu: Bu proje bir case/öğrenme çalışmasıdır. Kod yapısı temiz, okunabilir ve geliştirilmeye açık (extensible) tutulmuştur.

🛠 Gelecek Geliştirmeler
[ ] Redis SETNX: Slot kilitleme ile yarış durumlarını (race conditions) önleme.

[ ] Websockets: Gerçek zamanlı bildirim ve sıra takibi.

[ ] REST API: Django Rest Framework entegrasyonu.

[ ] Dashboard: Rol bazlı gelişmiş grafiksel paneller.
