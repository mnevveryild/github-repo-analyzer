import streamlit as st
from src.agent import analyze_repo

st.set_page_config(
    page_title="GitHub Repo Analiz Agent'ı",
    page_icon="🔍",
    layout="wide",
)

st.title("🔍 GitHub Repo Analiz Agent'ı")
st.markdown("Bir GitHub repo URL'si girin, agent projeyi analiz etsin.")

with st.sidebar:
    st.header("📖 Kullanım")
    st.markdown("""
    1. `.env` dosyasını oluşturun ve API key'lerinizi ekleyin
    2. Bir GitHub repo URL'si girin (örn. `https://github.com/tiangolo/fastapi`)
    3. **Analiz Et** butonuna tıklayın
    4. Agent tool'ları sırayla çağırarak analizi tamamlar

    **Gereksinimler:**
    - `GITHUB_TOKEN` (zorunlu)
    - `ANTHROPIC_API_KEY` veya `OPENAI_API_KEY`
    """)

repo_url = st.text_input(
    "GitHub Repo URL",
    placeholder="https://github.com/kullanici/repo",
)

analyze_button = st.button("Analiz Et", disabled=not repo_url.strip(), type="primary")

if analyze_button and repo_url.strip():
    with st.spinner("🤖 Agent analiz yapıyor, lütfen bekleyin..."):
        try:
            result = analyze_repo(repo_url.strip())

            st.header(f"📦 {result['repo_name']}")
            st.markdown(result["summary"])

            with st.expander("🛠️ Tech Stack", expanded=True):
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("Diller")
                    for lang in result["tech_stack"]["languages"]:
                        st.markdown(f"- {lang}")
                    st.subheader("Frameworkler")
                    for fw in result["tech_stack"]["frameworks"]:
                        st.markdown(f"- {fw}")
                with col2:
                    if result["tech_stack"]["databases"]:
                        st.subheader("Veritabanları")
                        for db in result["tech_stack"]["databases"]:
                            st.markdown(f"- {db}")
                    if result["tech_stack"]["tools"]:
                        st.subheader("Araçlar")
                        for tool in result["tech_stack"]["tools"]:
                            st.markdown(f"- {tool}")
                    if result["tech_stack"]["cloud_services"]:
                        st.subheader("Cloud Servisleri")
                        for cs in result["tech_stack"]["cloud_services"]:
                            st.markdown(f"- {cs}")

            with st.expander("💪 Güçlü Yanlar", expanded=True):
                for strength in result["strengths"]:
                    st.markdown(f"- {strength}")

            st.subheader("💡 Öneriler")
            priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}
            for suggestion in result["suggestions"]:
                with st.container(border=True):
                    emoji = priority_emoji.get(suggestion["priority"], "⚪")
                    st.markdown(
                        f"{emoji} **{suggestion['title']}** "
                        f"`{suggestion['category']}` · `{suggestion['priority']}`"
                    )
                    st.markdown(suggestion["description"])

            st.info(f"**Genel Değerlendirme:** {result['overall_assessment']}")

        except Exception as e:
            st.error(f"❌ Hata: {str(e)}")
