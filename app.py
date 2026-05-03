import streamlit as st
from src.agent import analyze_repo

st.set_page_config(
    page_title="Repo Analiz",
    page_icon="✦",
    layout="wide",
)

# Injected CSS for Dusty Rose / Plum Aesthetic
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

:root {
    /* Özel Gül Kurusu / Mürdüm Paleti */
    --color-1: #472f3b; /* En koyu arka plan */
    --color-2: #664555; /* Yüzeyler ve Kartlar */
    --color-3: #96677c; /* Kenarlıklar, pasif öğeler */
    --color-4: #d995b2; /* Birincil eylemler, butonlar, aktif seçimler */
    --color-5: #ffd6f3; /* Parlamalar, vurgular, metin başlıkları */
    
    /* Metin renkleri */
    --text-main: #ffffff; /* Okunabilirlik için saf beyaz */
    --text-muted: var(--color-4); /* Soluk metinler için 4. renk */
    
    /* Yapısal eşleştirmeler */
    --bg:        var(--color-1);
    --white:     var(--color-2);
    --text:      var(--text-main);
    --muted:     var(--text-muted);
    --border:    var(--color-3);
    
    /* Tipografi & Düzen */
    --font:      'Nunito', sans-serif;
    --mono:      'JetBrains Mono', monospace;
    --radius:    14px;
    --radius-sm: 8px;
}

html, body, [data-testid="stApp"] {
    background: var(--bg) !important;
    font-family: var(--font) !important;
    color: var(--text) !important;
}

#MainMenu, footer, header, [data-testid="stToolbar"] { display: none !important; }

.block-container {
    padding: 2.5rem 3rem 4rem !important;
    max-width: 1100px !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--white) !important;
    border-right: 1.5px solid var(--border) !important;
}
[data-testid="stSidebar"] > div { padding: 1.5rem !important; }

.sidebar-chip {
    display: inline-block;
    font-size: 0.65rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    background: rgba(150, 103, 124, 0.4); /* color-3 %40 */
    color: var(--color-5);
    border: 1px solid var(--color-4);
    border-radius: 50px;
    padding: 0.2rem 0.6rem;
    margin-bottom: 0.75rem;
    box-shadow: 0 0 10px rgba(217, 149, 178, 0.2);
}
[data-testid="stSidebar"] h3 {
    font-family: var(--font) !important;
    font-size: 0.8rem !important;
    font-weight: 800 !important;
    color: var(--color-5) !important;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin: 1.25rem 0 0.5rem !important;
}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] li {
    font-size: 0.875rem !important;
    color: var(--color-5) !important; /* Sidebar yazıları pudra tonu */
    opacity: 0.8;
    line-height: 1.6 !important;
}

/* ── Hero ── */
.hero {
    background: linear-gradient(145deg, var(--color-1) 0%, var(--color-2) 100%);
    border: 1.5px solid var(--border);
    border-radius: 20px;
    padding: 2.25rem 2.5rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
    box-shadow: inset 0 0 40px rgba(71, 47, 59, 0.8);
}
.hero::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 220px; height: 220px;
    background: radial-gradient(circle, rgba(255, 214, 243, 0.15) 0%, transparent 70%); /* color-5 glow */
    border-radius: 50%;
}
.hero::after {
    content: '';
    position: absolute;
    bottom: -40px; left: 60px;
    width: 140px; height: 140px;
    background: radial-gradient(circle, rgba(217, 149, 178, 0.2) 0%, transparent 70%); /* color-4 glow */
    border-radius: 50%;
}
.hero-content { position: relative; z-index: 1; }
.hero-eyebrow {
    font-size: 0.7rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--color-1);
    background: var(--color-5);
    display: inline-block;
    padding: 0.25rem 0.75rem;
    border-radius: 50px;
    margin-bottom: 0.85rem;
    box-shadow: 0 0 15px rgba(255, 214, 243, 0.4);
}
.hero-title {
    font-size: 2rem !important;
    font-weight: 800 !important;
    color: #ffffff !important;
    line-height: 1.25 !important;
    margin: 0 0 0.5rem !important;
}
.hero-sub {
    font-size: 1rem;
    color: var(--color-4);
}

/* ── Text input ── */
[data-testid="stTextInput"] label {
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    color: var(--color-5) !important;
}
[data-testid="stTextInput"] input {
    background: rgba(71, 47, 59, 0.6) !important; /* color-1 */
    border: 1.5px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    font-family: var(--mono) !important;
    font-size: 0.875rem !important;
    color: #ffffff !important;
    padding: 0.65rem 1rem !important;
    transition: all 0.3s ease !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: var(--color-5) !important;
    box-shadow: 0 0 12px rgba(255, 214, 243, 0.25) !important;
}

/* ── Radio pills ── */
[data-testid="stRadio"] > label {
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    color: var(--color-5) !important;
}
[data-testid="stRadio"] > div[role="radiogroup"] { 
    display: flex; gap: 0.75rem; flex-wrap: wrap; 
}
[data-testid="stRadio"] > div[role="radiogroup"] > label {
    background: var(--color-1) !important;
    border: 1.5px solid var(--color-3) !important;
    border-radius: 50px !important;
    padding: 0.45rem 1.2rem !important;
    transition: all 0.2s !important;
    cursor: pointer;
    align-items: center;
}
[data-testid="stRadio"] > div[role="radiogroup"] > label div[data-testid="stMarkdownContainer"] p {
    font-size: 0.875rem !important;
    font-weight: 600 !important;
    color: var(--color-4) !important;
    margin: 0 !important;
}
[data-testid="stRadio"] > div[role="radiogroup"] > label:hover {
    border-color: var(--color-4) !important;
}
[data-testid="stRadio"] > div[role="radiogroup"] > label:hover div[data-testid="stMarkdownContainer"] p {
    color: var(--color-5) !important;
}
[data-testid="stRadio"] > div[role="radiogroup"] > label > div:first-child {
    display: none !important; 
}
/* Seçili Durum */
[data-testid="stRadio"] > div[role="radiogroup"] > label:has(input:checked) {
    border-color: var(--color-5) !important;
    background: var(--color-4) !important;
    box-shadow: 0 0 15px rgba(217, 149, 178, 0.5) !important;
}
[data-testid="stRadio"] > div[role="radiogroup"] > label:has(input:checked) div[data-testid="stMarkdownContainer"] p {
    color: var(--color-1) !important;
    font-weight: 800 !important;
}

/* ── Button ── */
button[kind="primary"] {
    background: var(--color-4) !important;
    color: var(--color-1) !important;
    font-family: var(--font) !important;
    font-weight: 800 !important;
    font-size: 0.9rem !important;
    border: 1px solid var(--color-5) !important;
    border-radius: var(--radius-sm) !important;
    padding: 0.7rem !important;
    letter-spacing: 0.02em;
    transition: all 0.2s ease !important;
}
button[kind="primary"]:hover {
    background: var(--color-5) !important;
    color: var(--color-1) !important;
    transform: translateY(-2px);
    box-shadow: 0 0 20px rgba(255, 214, 243, 0.5) !important;
}
button[kind="primary"]:disabled {
    background: var(--color-2) !important;
    border-color: var(--color-3) !important;
    color: var(--color-3) !important;
    box-shadow: none !important;
}

/* ── Expanders ── */
[data-testid="stExpander"] {
    background: var(--white) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: var(--radius) !important;
    margin-bottom: 1rem !important;
    overflow: hidden;
}
[data-testid="stExpander"] summary {
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    color: var(--color-5) !important;
    padding: 1rem 1.25rem !important;
    background: var(--color-2) !important;
}
[data-testid="stExpander"] summary:hover {
    color: #ffffff !important;
}
[data-testid="stExpander"] > div > div { padding: 0 1.25rem 1.25rem !important; }

/* ── Result header ── */
.result-header {
    display: flex;
    align-items: center;
    gap: 1rem;
    background: var(--white);
    border: 1.5px solid var(--border);
    border-radius: 20px;
    padding: 1.5rem 2rem;
    margin-bottom: 1.5rem;
}
.repo-name {
    font-family: var(--mono);
    font-size: 1.1rem;
    font-weight: 600;
    color: #ffffff;
}
.repo-badge {
    font-size: 0.7rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    padding: 0.2rem 0.65rem;
    border-radius: 50px;
    border: 1px solid currentColor;
}
.badge-c5 { background: rgba(255, 214, 243, 0.1); color: var(--color-5); }
.badge-c4 { background: rgba(217, 149, 178, 0.1); color: var(--color-4); }

/* ── Suggestion cards (Tamamen kendi paletine uyarlandı) ── */
.sug-card {
    background: var(--white);
    border-top: 1.5px solid var(--border);
    border-bottom: 1.5px solid var(--border);
    border-right: 1.5px solid var(--border);
    padding: 1rem 1.25rem;
    margin-bottom: 0.75rem;
    border-radius: 0 var(--radius) var(--radius) 0;
}
/* Öncelik renkleri de senin paletinden (Kırmızı/Sarı vb YOK) */
.sug-high   { border-left: 4px solid var(--color-5); }
.sug-medium { border-left: 4px solid var(--color-4); }
.sug-low    { border-left: 4px solid var(--color-3); }

.pill {
    display: inline-block;
    font-size: 0.68rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    padding: 0.15rem 0.55rem;
    border-radius: 50px;
    margin-right: 0.3rem;
    border: 1px solid transparent;
}
.pill-high   { background: rgba(255, 214, 243, 0.15); color: var(--color-5); border-color: rgba(255, 214, 243, 0.3); }
.pill-medium { background: rgba(217, 149, 178, 0.15); color: var(--color-4); border-color: rgba(217, 149, 178, 0.3); }
.pill-low    { background: rgba(150, 103, 124, 0.15); color: var(--color-3); border-color: rgba(150, 103, 124, 0.3); }
.pill-cat    { background: var(--color-2); color: var(--text-main); border-color: var(--color-3); }

/* ── Metric ── */
[data-testid="stMetric"] {
    background: var(--color-1) !important;
    border: 1px solid var(--color-4) !important;
    border-radius: var(--radius) !important;
    padding: 1rem 1.25rem !important;
    box-shadow: 0 0 15px rgba(217, 149, 178, 0.1);
}
[data-testid="stMetricLabel"] { color: var(--color-5) !important; font-size: 0.75rem !important; font-weight: 800 !important; text-transform: uppercase; letter-spacing: 0.06em; }
[data-testid="stMetricValue"] { color: #ffffff !important; font-weight: 800 !important; font-size: 1.4rem !important; text-shadow: 0 0 10px rgba(255, 214, 243, 0.3); }

/* ── Section label ── */
.section-label {
    font-size: 0.72rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--color-5);
    margin: 1.5rem 0 0.75rem;
    border-bottom: 1px solid var(--color-3);
    padding-bottom: 0.4rem;
}

/* ── Phase step cards ── */
.phase-top {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 0.75rem;
}
.phase-title {
    font-weight: 800;
    font-size: 0.95rem;
    color: #ffffff;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.phase-dot {
    width: 10px; height: 10px;
    border-radius: 50%;
    flex-shrink: 0;
    box-shadow: 0 0 8px currentColor;
}
.phase-time {
    font-family: var(--mono);
    font-size: 0.72rem;
    font-weight: 700;
    background: var(--color-1);
    color: var(--color-5);
    border-radius: 50px;
    padding: 0.2rem 0.65rem;
    border: 1px solid var(--color-3);
}

/* Containers with border */
[data-testid="stVerticalBlock"][style*="border"] {
    background: var(--white) !important;
    border-color: var(--color-3) !important;
    border-radius: var(--radius) !important;
    padding: 1.25rem 1.5rem !important;
    transition: border-color 0.3s;
}
[data-testid="stVerticalBlock"][style*="border"]:hover {
    border-color: var(--color-4) !important;
}

/* ── Global text colors (Düzeltilmiş Hali) ── */
p, li, label {
    color: var(--text) !important;
    font-family: var(--font) !important;
}
strong, b { color: #ffffff !important; font-weight: 700 !important; }
[data-testid="stMarkdownContainer"] p { font-size: 0.9rem !important; line-height: 1.7 !important; margin-bottom: 0.35rem !important; }
[data-testid="stMarkdownContainer"] li { font-size: 0.9rem !important; line-height: 1.75 !important; }

/* ── Alert & Uyarı Kutuları (Renk paletine sıkı sıkıya bağlı) ── */
[data-testid="stAlert"], [data-testid="stInfo"] {
    background-color: rgba(217, 149, 178, 0.15) !important; /* color-4 */
    border: 1px solid rgba(217, 149, 178, 0.4) !important;
    border-radius: var(--radius-sm) !important;
    padding: 1rem !important;
}
[data-testid="stAlert"] p, [data-testid="stInfo"] p {
    color: #ffffff !important;
    font-size: 0.9rem !important;
}
[data-testid="stAlert"] span { color: var(--color-5) !important; }

/* ── Clean spacing ── */
[data-testid="stVerticalBlock"] > div:empty { display: none !important; }
.element-container:has(> div:empty) { margin: 0 !important; padding: 0 !important; }
[data-testid="stMarkdownContainer"]:empty { display: none !important; }

/* ── Misc ── */
hr { border-color: var(--color-3) !important; margin: 1.5rem 0 !important; }
h1, h2, h3 { font-family: var(--font) !important; color: var(--color-5) !important; }
h2 { font-size: 1.3rem !important; font-weight: 800 !important; }
h3 { font-size: 1rem !important; font-weight: 700 !important; }
h4, h5 { font-family: var(--font) !important; color: #ffffff !important; font-weight: 700 !important; }
ul { margin: 0.25rem 0 0.75rem 1rem !important; padding: 0 !important; }
[data-testid="column"] { padding: 0 0.4rem !important; }

/* Dark mode scrollbars (Senin renklerine özel) */
::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-track { background: var(--color-1); }
::-webkit-scrollbar-thumb { background: var(--color-3); border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: var(--color-4); }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-chip">✦ Rehber</div>', unsafe_allow_html=True)
    st.markdown("### Nasıl Kullanılır")
    st.markdown("""
    1. `.env` dosyasında API key'lerini tanımla
    2. GitHub repo URL'sini yapıştır
    3. Analiz modunu seç
    4. Başlat butonuna tıkla
    """)
    st.markdown("### Modlar")
    st.markdown("""
    **Kod İncelemesi**  
    Güçlü yönler, iyileştirme önerileri ve mimari analiz.

    **Klonlama Yol Haritası**  
    Projeyi sıfırdan oluşturmak için adım adım rehber.
    """)
    st.markdown("### Gereksinimler")
    st.markdown("""
    `GITHUB_TOKEN` · zorunlu  
    `GROQ_API_KEY` veya `ANTHROPIC_API_KEY`
    """)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-content">
    <div class="hero-eyebrow">✦ GitHub Repo Analizi</div>
    <div class="hero-title">Kodunu keşfet,<br>yol haritanı çiz.</div>
    <div class="hero-sub">Repo URL'sini gir, AI senin için derinlemesine analiz yapsın.</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Input ─────────────────────────────────────────────────────────────────────
# st.container kullanarak öğeleri sarıyoruz (HTML div hatasını giderir)
with st.container(border=True):
    repo_url = st.text_input(
        "GitHub Repo URL",
        placeholder="https://github.com/kullanici/repo",
    )

    mode_option = st.radio(
        "Analiz Modu",
        options=["Kod İncelemesi", " Klonlama Yol Haritası"],
        horizontal=True,
    )

    analyze_button = st.button(
        "✦  Analizi Başlat",
        disabled=not repo_url.strip(),
        type="primary",
        use_container_width=True,
    )

mode = "code_review" if "Kod" in mode_option else "system_design"

# ── Analiz ────────────────────────────────────────────────────────────────────
if analyze_button and repo_url.strip():
    with st.spinner("Analiz yapılıyor..."):
        try:
            result = analyze_repo(repo_url.strip(), mode=mode)
        except Exception as e:
            st.error(f"Hata oluştu: {str(e)}")
            st.stop()

    # ── MOD 1: Kod İncelemesi ─────────────────────────────────────────────────
    if mode == "code_review":
        st.markdown(
            f'<div class="result-header">'
            f'<span style="font-size:1.6rem"></span>'
            f'<div>'
            f'<div class="repo-name">{result["repo_name"]}</div>'
            f'<span class="repo-badge badge-c5">Kod İncelemesi</span>'
            f'</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
        st.markdown(result["summary"])
        st.markdown("---")

        with st.expander("  Tech Stack", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Diller**")
                for lang in result["tech_stack"]["languages"]:
                    st.markdown(f"- {lang}")
                st.markdown("**Frameworkler**")
                for fw in result["tech_stack"]["frameworks"]:
                    st.markdown(f"- {fw}")
            with col2:
                if result["tech_stack"]["databases"]:
                    st.markdown("**Veritabanları**")
                    for db in result["tech_stack"]["databases"]:
                        st.markdown(f"- {db}")
                if result["tech_stack"]["tools"]:
                    st.markdown("**Araçlar**")
                    for t in result["tech_stack"]["tools"]:
                        st.markdown(f"- {t}")
                if result["tech_stack"]["cloud_services"]:
                    st.markdown("**Cloud**")
                    for cs in result["tech_stack"]["cloud_services"]:
                        st.markdown(f"- {cs}")

        with st.expander(" Güçlü Yanlar", expanded=True):
            for strength in result["strengths"]:
                st.markdown(f"- {strength}")

        st.markdown('<div class="section-label"> Öneriler</div>', unsafe_allow_html=True)

        pri_pill  = {"high": "pill-high",  "medium": "pill-medium",  "low": "pill-low"}
        pri_label = {"high": "Yüksek",      "medium": "Orta",         "low": "Düşük"}
        pri_card  = {"high": "sug-high",    "medium": "sug-medium",   "low": "sug-low"}

        for s in result["suggestions"]:
            pri = s["priority"]
            st.markdown(
                f'<div class="sug-card {pri_card.get(pri, "")}">'
                f'<div style="margin-bottom:0.4rem">'
                f'<strong>{s["title"]}</strong>&nbsp;'
                f'<span class="pill pill-cat">{s["category"]}</span>'
                f'<span class="pill {pri_pill.get(pri, "")}">{pri_label.get(pri, pri)}</span>'
                f'</div>'
                f'<div style="font-size:0.875rem;color:var(--text-main);line-height:1.6;opacity:0.85">{s["description"]}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

        st.markdown("---")
        st.info(f"**Genel Değerlendirme:** {result['overall_assessment']}")

    # ── MOD 2: Klonlama Yol Haritası ──────────────────────────────────────────
    else:
        col_h, col_m = st.columns([4, 1])
        with col_h:
            st.markdown(
                f'<div class="result-header" style="margin-bottom:0">'
                f'<span style="font-size:1.6rem"></span>'
                f'<div>'
                f'<div class="repo-name">{result["repo_name"]}</div>'
                f'<span class="repo-badge badge-c4">Klonlama Rehberi</span>'
                f'</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
        with col_m:
            st.metric("Toplam Süre", result["estimated_total_duration"])

        st.markdown(result["summary"])
        st.markdown("---")

        with st.expander("  Temel Özellikler", expanded=True):
            for feat in result["core_features"]:
                st.markdown(f"- {feat}")

        with st.expander("  Önerilen Tech Stack", expanded=True):
            stack = result["recommended_tech_stack"]
            cols = st.columns(min(len(stack), 3))
            cat_emoji = {
                "Frontend": "", "Backend": "",
                "Database": "", "DevOps": "", "Testing": "",
            }
            for i, (cat, techs) in enumerate(stack.items()):
                with cols[i % len(cols)]:
                    st.markdown(f"**{cat_emoji.get(cat,'')} {cat}**")
                    for tech in techs:
                        st.markdown(f"- {tech}")

        st.markdown('<div class="section-label"> Adım Adım Yol Haritası</div>', unsafe_allow_html=True)

        # Yeni paletinden renkler: 5 numara, 4 numara ve 3 numara sıralı dönecek
        dot_colors = ["#ffd6f3", "#d995b2", "#96677c", "#ffd6f3", "#d995b2", "#96677c"]
        
        for i, step in enumerate(result["step_by_step_roadmap"]):
            dot = dot_colors[i % len(dot_colors)]
            with st.container(border=True):
                st.markdown(
                    f'<div class="phase-top">'
                    f'<div class="phase-title">'
                    f'<span class="phase-dot" style="color:{dot}; background:currentColor;"></span>'
                    f'{step["phase"]}'
                    f'</div>'
                    f'<span class="phase-time">⏱ {step["duration"]}</span>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
                c1, c2 = st.columns([2, 1])
                with c1:
                    st.markdown("**Görevler**")
                    for task in step["tasks"]:
                        st.markdown(f"  - {task}")
                with c2:
                    st.markdown(
                        f'<div style="background:var(--color-1);border:1px solid var(--color-3);border-radius:10px;padding:0.75rem 1rem;">'
                        f'<div style="font-size:0.7rem;font-weight:800;text-transform:uppercase;'
                        f'letter-spacing:0.06em;color:var(--color-4);margin-bottom:0.35rem">✓ Çıktı</div>'
                        f'<div style="font-size:0.875rem;color:var(--text-main)">{step["deliverable"]}</div>'
                        f'</div>',
                        unsafe_allow_html=True,
                    )

        st.markdown("---")

        with st.expander("  Potansiyel Zorluklar", expanded=True):
            for ch in result["potential_challenges"]:
                st.warning(ch)