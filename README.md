# GitHub Repo Analyzer

GitHub Repo Analyzer, public GitHub depolarini yapay zeka destekli olarak inceleyen bir analiz aracidir. Bir repo URL'si verildiginde proje amacini ozetler, teknoloji stack'ini cikarir, guclu yanlari listeler ve gelistirme onerileri uretir. Ayrica `system_design` modu ile benzer bir projeyi sifirdan gelistirmek icin yol haritasi hazirlayabilir.

Proje iki farkli arayuzle calisabilir:

- **Streamlit UI:** Hizli ve tek komutla calisan Python arayuzu.
- **Angular + FastAPI UI:** Ayrik frontend/backend mimarisiyle modern web arayuzu.

## Ozellikler

- GitHub API uzerinden repo metadata, README, dosya agaci ve commit bilgisi toplama
- LangChain/LangGraph tabanli tool-calling agent
- LLM provider secimi: Groq, Anthropic veya OpenAI
- Dependency dosyalarindan deterministik teknoloji tespiti
- Pydantic modelleriyle yapilandirilmis analiz ciktisi
- Kod inceleme ve sistem tasarimi olmak uzere iki analiz modu
- Streamlit, FastAPI ve Angular arayuz secenekleri

## Teknolojiler

**Backend**

- Python
- FastAPI
- Streamlit
- LangChain / LangGraph
- PyGithub
- Pydantic

**Frontend**

- Angular 17
- TypeScript
- SCSS
- RxJS

## Proje Yapisi

```text
.
├── app.py                         # Streamlit arayuzu
├── api.py                         # FastAPI servisi
├── requirements.txt               # Python bagimliliklari
├── src/
│   ├── agent.py                   # LLM agent ve analiz akisi
│   ├── config.py                  # Ortam degiskenleri ve provider ayarlari
│   ├── prompts.py                 # Analiz promptlari
│   ├── schemas.py                 # Pydantic cikti modelleri
│   ├── tools/                     # GitHub araclari ve teknoloji tespiti
│   └── utils/                     # Parser yardimcilari
├── frontend/
│   ├── src/app/                   # Angular uygulamasi
│   ├── proxy.conf.json            # Angular -> FastAPI proxy ayari
│   └── package.json               # Frontend bagimliliklari
└── tests/                         # Temel testler
```

## Gereksinimler

- Python 3.10+
- Node.js 18+
- GitHub Personal Access Token
- En az bir LLM API anahtari:
  - Groq
  - Anthropic
  - OpenAI

## Kurulum

### 1. Depoyu hazirlayin

```bash
git clone <repo-url>
cd github-repo-analyzer
```

### 2. Python sanal ortami olusturun

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

macOS/Linux:

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Python bagimliliklarini yukleyin

```bash
pip install -r requirements.txt
```

### 4. Ortam degiskenlerini ayarlayin

```bash
cp .env.example .env
```

`.env` dosyasini kendi anahtarlarinizla doldurun:

```env
GITHUB_TOKEN=ghp_xxxxx
LLM_PROVIDER=groq
GROQ_API_KEY=gsk_xxxxx

# Alternatif provider kullanacaksaniz:
ANTHROPIC_API_KEY=sk-ant-xxxxx
OPENAI_API_KEY=sk-xxxxx
```

`LLM_PROVIDER` degeri `groq`, `anthropic` veya `openai` olabilir.

## GitHub Token

GitHub API rate limit sorunlarini azaltmak icin token zorunludur.

1. GitHub token sayfasina gidin: https://github.com/settings/tokens
2. **Generate new token (classic)** secenegini kullanin.
3. Public repolar icin `public_repo` izni yeterlidir.
4. Token'i `.env` dosyasindaki `GITHUB_TOKEN` alanina ekleyin.

## Calistirma

### Secenek 1: Streamlit arayuzu

```bash
streamlit run app.py
```

Uygulama varsayilan olarak su adreste acilir:

```text
http://localhost:8501
```

### Secenek 2: FastAPI + Angular arayuzu

Bir terminalde backend'i baslatin:

```bash
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

Baska bir terminalde frontend'i baslatin:

```bash
cd frontend
npm install
npm start
```

Angular arayuzu:

```text
http://localhost:4200
```

API saglik kontrolu:

```text
http://localhost:8000/api/health
```

## API Kullanimi

Analiz endpoint'i:

```http
POST /api/analyze
Content-Type: application/json
```

Kod inceleme modu:

```json
{
  "repo_url": "https://github.com/tiangolo/fastapi",
  "mode": "code_review"
}
```

Sistem tasarimi modu:

```json
{
  "repo_url": "https://github.com/tiangolo/fastapi",
  "mode": "system_design"
}
```

## Analiz Modlari

### `code_review`

Repo hakkinda genel kod inceleme ciktisi uretir:

- Proje ozeti
- Ana amac
- Teknoloji stack'i
- Guclu yanlar
- Guvenlik, test, dokumantasyon, mimari ve gelistirici deneyimi onerileri
- Genel degerlendirme

### `system_design`

Benzer bir projeyi gelistirmek icin sistem tasarimi odakli cikti uretir:

- Temel ozellikler
- Onerilen teknoloji stack'i
- Asamali gelistirme yol haritasi
- Potansiyel zorluklar
- Tahmini toplam sure

## Testler

```bash
pytest tests/test_basic.py -v
```

## Frontend Build

```bash
cd frontend
npm run build
```

Build ciktisi `frontend/dist/` altinda olusturulur.

## Sik Karsilasilan Sorunlar

**`GITHUB_TOKEN eksik` hatasi**

`.env` dosyasinin olusturuldugundan ve `GITHUB_TOKEN` degerinin dolu oldugundan emin olun.

**LLM API anahtari eksik hatasi**

`LLM_PROVIDER` hangi provider'i gosteriyorsa ilgili API anahtarini `.env` dosyasina ekleyin.

**GitHub rate limit hatasi**

Token'in gecerli oldugunu kontrol edin. Public repo analizi icin `public_repo` izni yeterlidir.

**Angular API'ye ulasamiyor**

FastAPI servisinin `http://localhost:8000` adresinde calistigindan emin olun. Frontend proxy ayari `frontend/proxy.conf.json` dosyasinda `/api` isteklerini bu adrese yonlendirir.

**Private repo analiz edilemiyor**

Varsayilan kurulum public repolar icindir. Private repo analizi icin GitHub token'iniza ilgili repo izinlerini eklemeniz gerekir.

## Lisans

Bu depo icin henuz lisans dosyasi eklenmemis.
