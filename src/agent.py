from langgraph.prebuilt import create_react_agent
from src.config import Config
from src.schemas import RepoAnalysis
from src.prompts import SYSTEM_PROMPT
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
    else: # biz bunu kullanacağız ama diğerlerini de destekleyelim ki isteyen değiştirebilsin
        from langchain_groq import ChatGroq
        return ChatGroq(
            model=Config.GROQ_MODEL,
            temperature=0.2,
            api_key=Config.GROQ_API_KEY,
        )


def analyze_repo(repo_url: str) -> dict:
    Config.validate()

    llm = get_llm()
    agent = create_react_agent(llm, ALL_TOOLS, prompt=SYSTEM_PROMPT)

    result = agent.invoke({
        "messages": [("human", f"Şu GitHub reposunu analiz et: {repo_url}")]
    })

    raw_output = result["messages"][-1].content

    structured_llm = llm.with_structured_output(RepoAnalysis)
    structured_result: RepoAnalysis = structured_llm.invoke(
        f"Aşağıdaki repo analiz çıktısını yapılandırılmış formata dönüştür:\n\n{raw_output}"
    )
    return structured_result.model_dump()
