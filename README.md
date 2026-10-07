# AI-Powered Research & Document Intelligence Platform

A secure platform where users can upload **PDF, Excel, CSV, TXT, and Markdown** files, perform **semantic search**, and receive **grounded question-answering** responses sourced exclusively from their own documents.

## 🎯 Key Features

- 📄 **Multi-Format Support:** PDF, Excel, CSV, TXT, Markdown
- 🔍 **Semantic Search:** Meaning-based search powered by OpenAI embeddings + pgvector
- 🤖 **Grounded QA:** LLM-powered answers with function calling, sourced from your documents
- 🔐 **Access Control (RBAC):** Users can only access documents they're authorized to view
- ⚡ **Asynchronous Processing:** File parsing, chunking, and embedding run in the background via Celery

## 🏗️ Technology Stack

- **Backend:** Python 3.12+ · Django 5.2 LTS
- **Database:** PostgreSQL 16 + pgvector
- **Cache & Message Broker:** Redis 7
- **Async Task Processing:** Celery 5 + django-celery-beat
- **LLM:** OpenAI (gpt-4o-mini + text-embedding-3-small)
- **Server:** Gunicorn + NGINX
- **Containerization:** Docker Compose

## 📅 Roadmap

The project is developed in 10 phases:

- **Phase 0:** Environment Setup & Django Scaffolding
- **Phase 1:** Docker, PostgreSQL/pgvector, Redis
- **Phase 2:** User Management, Authentication, RBAC
- **Phase 3:** Document Model & Upload
- **Phase 4:** Celery & Async Processing
- **Phase 5:** Parsing, Normalization, Chunking
- **Phase 6:** Embeddings & Semantic Search
- **Phase 7:** LLM QA & Function Calling
- **Phase 8:** Frontend (Django Templates)
- **Phase 9:** Testing, Security, Performance
- **Phase 10:** Production Deployment

For detailed roadmap, see [`document_intelligence_platform_roadmap.md`](./document_intelligence_platform_roadmap.md)

## 🚀 Quick Start

### Requirements

- Python 3.12+
- Docker & Docker Compose
- Git

### Installation (After Phase 0)

```bash
# Clone the repository
git clone https://github.com/yourusername/document-intelligence-platform.git
cd document-intelligence-platform

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
python manage.py migrate

# Start development server
python manage.py runserver
```

## 📝 License

MIT License - See [`LICENSE`](./LICENSE) file for details.

## 👤 Author

Teoman Ünal

---

**Note:** This project is under active development. Phase 0 setup is in progress.
