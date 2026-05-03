# 🔍 GitHub Repo Analiz Agent'ı

LangChain tool-calling agent ile güçlendirilmiş GitHub repo analiz aracı. Bir repo URL'si verdiğinizde agent, projeyi özetler, teknoloji stack'ini tespit eder ve somut geliştirme önerileri üretir.

## ✨ Özellikler

- **Tool-Calling Agent:** GitHub API araçlarını otomatik olarak sırayla çağırır
- **Deterministik Tech Detection:** Teknoloji tespiti dependency dosyaları parse edilerek yapılır, LLM tahminine bırakılmaz
- **Structured Output:** Pydantic modeli ile yapılandırılmış çıktı
- **İki Aşamalı LLM:** Agent keşif yapar, ikinci LLM çağrısı structured formata dönüştürür
- **Streamlit UI:** Kullanımı kolay web arayüzü
- **Çoklu Provider:** Anthropic Claude veya OpenAI GPT desteği

## 🚀 Kurulum

### 1. Sanal ortam oluşturun

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 2. Bağımlılıkları yükleyin

```bash
pip install -r requirements.txt
```

### 3. Environment variables ayarlayın

```bash
cp .env.example .env
```

`.env` dosyasını düzenleyin:

```env
ANTHROPIC_API_KEY=sk-ant-xxxxx   # veya OPENAI_API_KEY
GITHUB_TOKEN=ghp_xxxxx
LLM_PROVIDER=anthropic            # veya openai
```

## 🔑 GitHub Token Oluşturma

1. [https://github.com/settings/tokens](https://github.com/settings/tokens) adresine gidin
2. **"Generate new token (classic)"** seçin
3. Sadece **`public_repo`** iznini işaretleyin
4. Token'ı kopyalayıp `.env` dosyasına yapıştırın

> Token olmadan GitHub API rate limit'e takılırsınız (saatte 60 istek).

## ▶️ Çalıştırma

```bash
streamlit run app.py
```

Tarayıcınızda `http://localhost:8501` açılacak.

## 📖 Örnek Kullanım

1. URL alanına `https://github.com/tiangolo/fastapi` girin
2. **Analiz Et** butonuna tıklayın
3. Agent verbose log'da tool çağrılarını görebilirsiniz:
   - `get_repo_metadata` → temel bilgiler
   - `get_readme` → proje açıklaması
   - `detect_tech_stack` → teknolojiler
   - `get_file_tree` → dosya yapısı
   - `get_recent_commits` → son aktivite
4. Sonuçlar: özet, tech stack, güçlü yanlar, öneriler, genel değerlendirme

## 🧪 Testleri Çalıştırma

```bash
pytest tests/test_basic.py -v
```

## ❓ Sıkça Karşılaşılan Sorunlar

**`GITHUB_TOKEN eksik` hatası:**
`.env` dosyasını oluşturdunuz mu? `cp .env.example .env` komutunu çalıştırın.

**`RateLimitExceededException` hatası:**
GitHub token olmadan veya geçersiz token ile çok fazla istek atıldı. Token'ınızı kontrol edin.

**`ValidationError` hatası (structured output):**
LLM bazen schema'ya uymayan çıktı üretebilir. Tekrar deneyin veya farklı bir model/provider deneyin.

**Streamlit `ModuleNotFoundError`:**
`pip install -r requirements.txt` komutunu sanal ortamda çalıştırın.

**`Private repo` erişim hatası:**
Bu araç yalnızca public repo'ları analiz eder. Private repo için token'ınıza `repo` izni ekleyin.