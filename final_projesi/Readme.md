
# 📌 Proje Başlığı

> Stok Takip Sistemi

## 🧾 Proje Tanıtımı

    Bu projeyi, bir firmanın ürünlerinin stok durumunu takip altına almak amacıyla geliştirdim. Projeyi yaparken uzun vadeli düşündüm; ileride bu sistemi daha da geliştirip kendi GitHub hesabıma yüklemeyi ve satışa sunmayı planlıyorum. Gerçek dünyada da bu projenin karşılığı büyük çünkü çoğu firma ve iş yeri için oldukça uygun bir çözüm sunuyor.

## 🚀 Proje Özellikleri

Aşağıya projenizin sunduğu temel işlevleri maddeler halinde yazınız:
Örneğin:  
- 🔐 Kullanıcı kayıt ve giriş işlemleri
- 📚 Yeni veri ürün ekleyebilme , güncelleme ve silme
- 📝 Verileri düzenleyebilme ve silebilme
- 🔎 Arama / filtreleme özellikleri
- 📦 Veritabanı bağlantısı ile kalıcı veri saklama

## ⚙️ Kurulum ve Çalıştırma
    Evet, proje başkaları tarafından da sorunsuz çalıştırılabilir. Kurulum ve çalıştırma adımları net ve eksiksiz şekilde belirlendi. 
    Kurulum talimatları, projeyi ilk defa kuracak bir kişinin bile hata almadan sistemi ayağa kaldırabilmesi için ayrıntılı ve adım adım açıklandı.
    ‘ pip install -r requirements.txt ‘, tüm paketleri yükleyebilir.
    Projemiz Render üzerinden yayınlamaktadır.

### ✅ Gereksinimler
    Python=3.13.1
    Flask==3.0.0
    Flask-Login==0.6.3
    Flask-SQLAlchemy==3.1.1
    Werkzeug==3.0.1
    fpdf==1.7.2
    pandas==2.1.0
    numpy==1.26.2
    XlsxWriter==3.1.0
> Not: Bu kütüphaneleri `requirements.txt` dosyasından otomatik olarak yükleyebilirsiniz.

### 🚀 Uygulamayı Başlatma
    Uygulama tarayıcınızda http://127.0.0.1:5000/ adresinde çalışacaktır. local olarak böyle , 
    https://stok-takip-sistemi.onrender.com adresi sayesinde tüm tarayıcılardan erişme açık

## 📂 Proje Dosya Yapısı
    STOK_TAKIP_SISTEMI/
    ├── app.py
    ├── alldbjson.py
    ├── db2json.py
    ├── db3json.py
    ├── requirements.txt
    ├── kullanici_urunler.json
    ├── products.json
    ├── users.json
    ├── static/
    │   ├── fonts/
    │   │   ├── arial.cw127.pkl
    │   │   ├── arial.pkl
    │   │   ├── ARIAL.TTF
    │   │   ├── ARIALBD.TTF
    │   │   ├── ARIALBI.TTF
    │   │   ├── ARIALI.TTF
    │   │   └── ARIBLK.TTF
    │   ├── image/
    │   │   ├── logo.png
    │   │   ├── warehouse1.png
    │   │   └── warehouse2.png
    │   ├── base.css
    │   ├── critical_stok.css
    │   ├── dashboard.css
    │   ├── products.css
    │   ├── products_add.css
    │   ├── products_update.css
    │   └── register.css
    ├── templates/
    │   ├── about.html
    │   ├── base.html
    │   ├── contant.html
    │   ├── critical_stok.html
    │   ├── dashboard.html
    │   ├── dashboardbase.html
    │   ├── home.html
    │   ├── login.html
    │   ├── products.html
    │   ├── products_add.html
    │   ├── products_update.html
    │   ├── register.html
    │   ├── reports.html
    │   ├── users.html
    │   └── users_update.html
    └── README.md
















