from langgraph.prebuilt import create_react_agent
from src.config import Config
from src.schemas import RepoAnalysis, SystemDesignAnalysis
from src.prompts import CODE_REVIEW_PROMPT, SYSTEM_DESIGN_PROMPT
from src.tools.github_tools import ALL_TOOLS


def get_llm():
    if Config.LLM_PROVIDER == "anthropic":
        from langchain_anthropic import ChatAnthropic
        return ChatAnthropic(
            model=Config.ANTHROPIC_MODEL,
            temperature=0.2,
            max_tokens=4096,
            api_key=Config.ANTHROPIC_API_KEY,
        )
    elif Config.LLM_PROVIDER == "openai":
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            model=Config.OPENAI_MODEL,
            temperature=0.2,
            api_key=Config.OPENAI_API_KEY,
        )
    else:
        from langchain_groq import ChatGroq
        return ChatGroq(
            model=Config.GROQ_MODEL,
            temperature=0.2,
            api_key=Config.GROQ_API_KEY,
        )


def analyze_repo(repo_url: str, mode: str = "code_review") -> dict:
    """
    Repo analizi yapar.

    mode="code_review"   → Kod incelemesi, güçlü yanlar, öneriler (RepoAnalysis)
    mode="system_design" → Klonlama yol haritası, tech stack, roadmap (SystemDesignAnalysis)
    """
    Config.validate()

    llm = get_llm()

    # Moda göre prompt ve çıktı şeması seç
    if mode == "system_design":
        prompt = SYSTEM_DESIGN_PROMPT
        output_schema = SystemDesignAnalysis
    else:
        # Varsayılan: code_review — eski davranış aynen korunur
        prompt = CODE_REVIEW_PROMPT
        output_schema = RepoAnalysis

    # Aşama 1: ReAct agent — tool'ları çağırarak serbest analiz yap
    agent = create_react_agent(llm, ALL_TOOLS, prompt=prompt)
    result = agent.invoke({
        "messages": [("human", f"Şu GitHub reposunu analiz et: {repo_url}")]
    })
    raw_output = result["messages"][-1].content

    # Aşama 2: Ham metni seçilen şemaya göre yapılandır
    structured_llm = llm.with_structured_output(output_schema)
    structured_result = structured_llm.invoke(
        f"Aşağıdaki repo analiz çıktısını yapılandırılmış formata dönüştür:\n\n{raw_output}"
    )
    return structured_result.model_dump()