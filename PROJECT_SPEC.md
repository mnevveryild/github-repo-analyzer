# GitHub Repo Analiz Agent — Proje Spesifikasyonu

Bu dosya, Claude Code'un sıfırdan oluşturması gereken projenin tam tarifidir. Bu spec'i okuyup adım adım uygula.

---

## 🎯 Proje Amacı

Bir GitHub repo URL'si verildiğinde:
1. Projeyi özetleyen
2. Kullanılan teknolojileri çıkaran
3. "Bu projeyi geliştirmek için öneriler" üreten

bir **LangChain tool-calling agent** sistemi. Kullanıcı arayüzü **Streamlit** ile yapılacak.

---

## 🏗️ Mimari

- **Tool-Calling Agent yaklaşımı:** Agent, GitHub'dan veri çekmek için tool'ları kendi mantığıyla çağırır.
- **Deterministik tech detection:** Teknoloji tespiti LLM'e bırakılmıyor; dependency dosyaları parse edilerek kesin sonuç üretiliyor, sonra LLM bu structured veriyi yorumluyor.
- **Structured output:** Çıktı Pydantic modeli ile yapılandırılıyor (`with_structured_output`).
- **İki aşamalı LLM kullanımı:** Önce agent keşif yapıyor, sonra ikinci bir LLM çağrısı raw çıktıyı structured formata dönüştürüyor.

---

## 📁 Dosya Yapısı

Aşağıdaki dosya yapısını birebir oluştur:

```
github-repo-analyzer/
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
├── app.py
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── agent.py
│   ├── schemas.py
│   ├── prompts.py
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── github_tools.py
│   │   └── tech_detector.py
│   └── utils/
│       ├── __init__.py
│       └── parsers.py
└── tests/
    └── test_basic.py
```

---

## 📦 Bağımlılıklar (requirements.txt)

```txt
langchain>=0.3.0
langchain-anthropic>=0.3.0
langchain-openai>=0.2.0
langchain-community>=0.3.0
PyGithub>=2.4.0
pydantic>=2.9.0
python-dotenv>=1.0.1
streamlit>=1.39.0
tomli>=2.0.2
requests>=2.32.0
```

---

## 🔐 Environment Variables (.env.example)

```env
# Anthropic Claude için
ANTHROPIC_API_KEY=sk-ant-xxxxx

# Veya OpenAI için
OPENAI_API_KEY=sk-xxxxx

# GitHub Personal Access Token (zorunlu - rate limit için)
# https://github.com/settings/tokens adresinden oluştur
# Sadece "public_repo" izni yeterli
GITHUB_TOKEN=ghp_xxxxx

# Hangi model kullanılacak: anthropic veya openai
LLM_PROVIDER=anthropic
```

---

## 🚫 .gitignore

```
venv/
__pycache__/
*.pyc
.env
.streamlit/
.vscode/
*.egg-info/
.pytest_cache/
```

---

## 🧩 Modül Detayları

### src/config.py

`Config` sınıfı tanımla:
- `.env`'den şu değişkenleri yükle: `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `GITHUB_TOKEN`, `LLM_PROVIDER`
- `LLM_PROVIDER` default değeri `"anthropic"`
- `ANTHROPIC_MODEL = "claude-sonnet-4-5"` (Claude Sonnet 4.5)
- `OPENAI_MODEL = "gpt-4o-mini"`
- `validate()` classmethod'u: GITHUB_TOKEN yoksa ve seçili provider'ın API key'i yoksa hata fırlat

### src/schemas.py

Pydantic v2 modelleri:

**TechStack:**
- `languages: List[str]` — programlama dilleri
- `frameworks: List[str]` — React, Django gibi
- `databases: List[str]` (default boş liste)
- `tools: List[str]` (default boş liste) — build, test, CI/CD
- `cloud_services: List[str]` (default boş liste)

**Suggestion:**
- `category: Literal["security", "performance", "testing", "documentation", "architecture", "dx", "dependencies"]`
- `title: str` — kısa başlık
- `description: str` — detaylı açıklama
- `priority: Literal["high", "medium", "low"]`

**RepoAnalysis:**
- `repo_name: str`
- `summary: str` — 2-3 cümlelik özet
- `main_purpose: str`
- `tech_stack: TechStack`
- `strengths: List[str]`
- `suggestions: List[Suggestion]`
- `overall_assessment: str`

### src/utils/parsers.py

Şu fonksiyonları yaz:

**`parse_package_json(content: str) -> Dict[str, List[str]]`**
- JSON parse et
- `dependencies`, `devDependencies`, `scripts` anahtarlarını döndür (her biri liste)
- Hata durumunda boş listeler döndür

**`parse_requirements_txt(content: str) -> List[str]`**
- Her satırı işle
- Yorum satırlarını (`#`) ve boş satırları atla
- Versiyon belirteçlerini regex ile temizle: `[<>=!~]`

**`parse_pyproject_toml(content: str) -> List[str]`**
- `tomli` ile parse et
- Hem Poetry formatını (`tool.poetry.dependencies`) hem PEP 621 formatını (`project.dependencies`) destekle
- `python` anahtarını hariç tut

**`detect_framework_signatures(file_paths: List[str]) -> List[str]`**
- Şu signature dict'ini kullan:
  ```python
  {
      "next.config.js": "Next.js",
      "next.config.ts": "Next.js",
      "nuxt.config.js": "Nuxt.js",
      "vue.config.js": "Vue.js",
      "angular.json": "Angular",
      "svelte.config.js": "Svelte",
      "manage.py": "Django",
      "wsgi.py": "Django/Flask",
      "Gemfile": "Ruby on Rails",
      "Cargo.toml": "Rust",
      "go.mod": "Go",
      "pom.xml": "Maven/Java",
      "build.gradle": "Gradle/Java",
      "Dockerfile": "Docker",
      "docker-compose.yml": "Docker Compose",
      ".github/workflows": "GitHub Actions",
  }
  ```
- Eşleşenleri (duplicate olmadan) liste olarak döndür

### src/tools/tech_detector.py

**`detect_tech_stack(repo_url: str) -> Dict[str, Any]`** fonksiyonu:

1. `Github(Config.GITHUB_TOKEN)` ile client oluştur
2. URL'den `owner/repo` formatını çıkar (`https://github.com/` prefix'ini kaldır, `/` ile split et)
3. `repo.get_languages()` ile dilleri al
4. Şu dosyaları sırayla kontrol et: `package.json`, `requirements.txt`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `pom.xml`, `Gemfile`
5. Her birini parse et (uygun parser ile)
6. Root dizindeki tüm dosyaları listele, `detect_framework_signatures` ile framework tespiti yap
7. Şu yapıda dict döndür:
   ```python
   {
       "languages": dict,
       "dependencies": dict,
       "frameworks": list,
       "file_signatures": list,
   }
   ```
8. Hata durumlarında `{"error": str(e)}` döndür

### src/tools/github_tools.py

`@tool` decorator'ı ile şu LangChain tool'larını tanımla:

**`get_repo_metadata(repo_url: str) -> str`**
- PyGithub ile repo'yu al
- Şu bilgileri JSON olarak döndür: `name, description, stars, forks, open_issues, language, license, created_at, updated_at, topics`

**`get_readme(repo_url: str) -> str`**
- README'yi decode et
- 8000 karakterden uzunsa kırp ve `[... README kırpıldı ...]` ekle

**`get_file_tree(repo_url: str) -> str`**
- Root dizindeki dosya/klasörleri listele
- Klasörler için 📁, dosyalar için 📄 emoji kullan

**`read_file(repo_url: str, file_path: str) -> str`**
- Belirli dosyanın içeriğini oku
- 5000 karakterden uzunsa kırp

**`detect_tech_stack(repo_url: str) -> str`**
- `tech_detector.py`'deki fonksiyonu çağır
- Sonucu JSON string olarak döndür (`json.dumps(..., default=str)`)

**`get_recent_commits(repo_url: str, limit: int = 5) -> str`**
- Son `limit` kadar commit'i getir
- Her biri için: sha (kısa), message (ilk satır), author, date

Sonunda `ALL_TOOLS` listesi tanımla, tüm tool'ları içersin.

### src/prompts.py

Türkçe bir `SYSTEM_PROMPT` tanımla. İçeriği:
- Agent'a deneyimli bir yazılım mimarı olduğunu söyle
- Adım sırasını belirt: önce metadata → readme → tech_stack → file_tree → gerekirse read_file → recent_commits
- Çıktıda istenenleri listele: özet, teknolojiler, güçlü yanlar, **somut ve eyleme dönük öneriler**
- Önerilerin spesifik olması gerektiğini vurgula ("X dosyasında Y eksik" gibi)
- Kategori etiketleri ve öncelik seviyeleri kullansın
- Türkçe yanıt versin

### src/agent.py

**`get_llm()` fonksiyonu:**
- `Config.LLM_PROVIDER` "anthropic" ise `ChatAnthropic` döndür (temperature=0.2, max_tokens=4096)
- "openai" ise `ChatOpenAI` döndür (temperature=0.2)

**`create_analyzer_agent()` fonksiyonu:**
- `ChatPromptTemplate.from_messages` ile prompt oluştur (system, human, agent_scratchpad placeholder)
- `create_tool_calling_agent` ile agent oluştur
- `AgentExecutor` ile sar (verbose=True, max_iterations=15)

**`analyze_repo(repo_url: str) -> dict` fonksiyonu:**
1. `Config.validate()` çağır
2. Agent'ı çalıştır, raw çıktıyı al
3. İkinci LLM çağrısı yap: `llm.with_structured_output(RepoAnalysis)` ile structured çıktı üret
4. `model_dump()` ile dict'e çevirip döndür

### app.py — Streamlit UI

- Sayfa başlığı: "🔍 GitHub Repo Analiz Agent'ı"
- Text input: repo URL'si
- "Analiz Et" butonu (URL boşken disabled)
- Buton tıklanınca `st.spinner` içinde `analyze_repo()` çağır
- Sonucu şu şekilde göster:
  - Repo adı (header)
  - Özet (paragraf)
  - Tech Stack (expander içinde 2 kolon: diller/framework | DB/araçlar)
  - Güçlü Yanlar (expander, bullet list)
  - Öneriler (her biri `st.container(border=True)` içinde, priority emoji'leri: 🔴 high, 🟡 medium, 🟢 low)
  - Genel Değerlendirme (`st.info`)
- Hata durumunda `st.error` ile göster
- Sidebar'da kısa kullanım talimatı

### tests/test_basic.py

Basit smoke test'ler:
- `parse_requirements_txt` doğru çalışıyor mu
- `detect_framework_signatures` Dockerfile'ı tespit ediyor mu
- `Config.validate()` eksik env'de hata fırlatıyor mu

---

## 📝 README.md İçeriği

Şunları içersin:
- Proje tanımı
- Özellikler listesi
- Kurulum adımları (venv, pip install, .env)
- GitHub token oluşturma rehberi
- `streamlit run app.py` komutu
- Örnek kullanım
- Sıkça karşılaşılan sorunlar bölümü

---

## ✅ Kabul Kriterleri

Proje tamamlandığında şunlar çalışmalı:

1. `pip install -r requirements.txt` hatasız çalışmalı
2. `.env.example` dosyası `.env` olarak kopyalanıp doldurulduğunda
3. `streamlit run app.py` ile UI açılmalı
4. `https://github.com/tiangolo/fastapi` gibi bir repo girildiğinde:
   - Agent tool'ları sırayla çağırmalı (verbose log'da görünecek)
   - Structured çıktı üretilmeli
   - UI'da tüm bölümler render edilmeli
5. Geçersiz URL veya private repo için hata mesajı düzgün gösterilmeli

---

## 🚧 Dikkat Edilecek Noktalar

- **Import path'leri:** `src.tools.github_tools` gibi tam path kullan, relative import yapma
- **`__init__.py` dosyaları boş olabilir** ama mutlaka oluştur
- **`@tool` decorator'ı** `langchain_core.tools`'tan import edilmeli
- **Streamlit cache:** Aynı repo tekrar analiz edilirse hızlı dönsün diye `@st.cache_data` kullanmayı düşün ama agent çağrısında dikkatli ol (her çağrı pahalı)
- **PyGithub'da** rate limit hata yakalaması koyma, basit `try/except` yeterli
- **Token kırpma sınırları:** README 8000, dosya 5000 karakter — bu sınırlar fix kalsın

---

## 🎬 Yapılış Sırası (Önerilen)

1. Dizin yapısını ve boş dosyaları oluştur
2. `requirements.txt`, `.env.example`, `.gitignore`
3. `config.py` ve `schemas.py`
4. `utils/parsers.py`
5. `tools/tech_detector.py`
6. `tools/github_tools.py`
7. `prompts.py`
8. `agent.py`
9. `app.py`
10. `tests/test_basic.py`
11. `README.md`
12. Son olarak: tüm dosyaları okuyarak import'lar ve syntax'ı doğrula
