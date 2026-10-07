# AI Destekli Araştırma & Doküman İstihbaratı Platformu

Kullanıcıların **PDF, Excel, CSV, TXT ve Markdown** dosyalarını yükleyip **semantik arama** yapabildiği ve yalnızca kendi dokümanlarından beslenen, **kaynak gösteren (grounded) soru-cevap** alabildiği güvenli bir platform.

## 🎯 Temel Özellikler

- 📄 **Çoklu Dosya Desteği:** PDF, Excel, CSV, TXT, Markdown
- 🔍 **Semantik Arama:** OpenAI embeddings + pgvector ile anlam bazlı arama
- 🤖 **Kaynak Gösteren QA:** LLM function calling ile belgelerinizden beslenmiş cevaplar
- 🔐 **Yetkilendirme (RBAC):** Kullanıcılar yalnızca yetkili oldukları dokümanlara erişir
- ⚡ **Asenkron İşleme:** Celery ile dosya parsing, chunking, embedding arka planda çalışır

## 🏗️ Teknoloji Yığını

- **Backend:** Python 3.12+ · Django 5.2 LTS
- **Veritabanı:** PostgreSQL 16 + pgvector
- **Cache & Broker:** Redis 7
- **Asenkron İşleme:** Celery 5 + django-celery-beat
- **LLM:** OpenAI (gpt-4o-mini + text-embedding-3-small)
- **Sunucu:** Gunicorn + NGINX
- **Konteynerizasyon:** Docker Compose

## 📅 Yol Haritası

Proje 10 faz halinde geliştirilecektir:

- **Faz 0:** Ortam Kurulumu & Django İskeleti
- **Faz 1:** Docker, PostgreSQL/pgvector, Redis
- **Faz 2:** Kullanıcı, Kayıt/Giriş, RBAC
- **Faz 3:** Doküman Modeli & Yükleme
- **Faz 4:** Celery & Asenkron İşleme
- **Faz 5:** Parsing, Normalizasyon, Chunking
- **Faz 6:** Embeddings & Semantik Arama
- **Faz 7:** LLM QA & Function Calling
- **Faz 8:** Frontend (Django Templates)
- **Faz 9:** Test, Güvenlik, Performans
- **Faz 10:** Production Dağıtım

Detaylı yol haritası için bkz. [`document_intelligence_platform_roadmap.md`](./document_intelligence_platform_roadmap.md)

## 🚀 Hızlı Başlangıç

### Gereksinimler

- Python 3.12+
- Docker & Docker Compose
- Git

### Kurulum (Faz 0 sonrası)

```bash
# Repo'yu klonla
git clone https://github.com/yourusername/document-intelligence-platform.git
cd document-intelligence-platform

# Virtual environment oluştur
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Bağımlılıkları yükle
pip install -r requirements.txt

# Veritabanı migrasyonlarını çalıştır
python manage.py migrate

# Geliştirme sunucusunu başlat
python manage.py runserver
```

## 📝 Lisans

MIT License - Detaylar için [`LICENSE`](./LICENSE) dosyasına bakın.

## 👤 Yazar

Teoma

---

**Not:** Bu proje aktif geliştirme aşamasındadır. Faz 0 kurulumu devam etmektedir.
