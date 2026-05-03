import json
from langchain_core.tools import tool
from github import Github
from src.config import Config
from src.tools.tech_detector import detect_tech_stack as _detect_tech_stack


def _get_repo(repo_url: str):
    client = Github(Config.GITHUB_TOKEN)
    path = repo_url.replace("https://github.com/", "").strip("/")
    owner_repo = "/".join(path.split("/")[:2])
    return client.get_repo(owner_repo)


@tool
def get_repo_metadata(repo_url: str) -> str:
    """GitHub repo hakkında temel meta bilgileri getirir: isim, açıklama, yıldız, fork, dil, lisans, tarihler, konular."""
    try:
        repo = _get_repo(repo_url)
        license_name = repo.license.name if repo.license else None
        data = {
            "name": repo.full_name,
            "description": repo.description,
            "stars": repo.stargazers_count,
            "forks": repo.forks_count,
            "open_issues": repo.open_issues_count,
            "language": repo.language,
            "license": license_name,
            "created_at": str(repo.created_at),
            "updated_at": str(repo.updated_at),
            "topics": repo.get_topics(),
        }
        return json.dumps(data, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)})


@tool
def get_readme(repo_url: str) -> str:
    """Repo'nun README dosyasını getirir (maksimum 8000 karakter)."""
    try:
        repo = _get_repo(repo_url)
        readme = repo.get_readme()
        content = readme.decoded_content.decode("utf-8")
        if len(content) > 8000:
            content = content[:8000] + "\n[... README kırpıldı ...]"
        return content
    except Exception as e:
        return f"README alınamadı: {str(e)}"


@tool
def get_file_tree(repo_url: str) -> str:
    """Repo'nun root dizinindeki dosya ve klasörleri listeler."""
    try:
        repo = _get_repo(repo_url)
        contents = repo.get_contents("")
        lines = []
        for item in contents:
            if item.type == "dir":
                lines.append(f"📁 {item.name}/")
            else:
                lines.append(f"📄 {item.name}")
        return "\n".join(lines)
    except Exception as e:
        return f"Dosya ağacı alınamadı: {str(e)}"


@tool
def read_file(repo_url: str, file_path: str) -> str:
    """Repo içindeki belirli bir dosyanın içeriğini okur (maksimum 5000 karakter)."""
    try:
        repo = _get_repo(repo_url)
        file_content = repo.get_contents(file_path)
        content = file_content.decoded_content.decode("utf-8")
        if len(content) > 5000:
            content = content[:5000] + "\n[... dosya kırpıldı ...]"
        return content
    except Exception as e:
        return f"Dosya okunamadı: {str(e)}"


@tool
def detect_tech_stack(repo_url: str) -> str:
    """Repo'nun kullandığı teknoloji stack'ini deterministik olarak tespit eder."""
    result = _detect_tech_stack(repo_url)
    return json.dumps(result, default=str, ensure_ascii=False)


@tool
def get_recent_commits(repo_url: str, limit: int = 5) -> str:
    """Repo'nun son commit'lerini getirir."""
    try:
        repo = _get_repo(repo_url)
        commits = list(repo.get_commits()[:limit])
        result = []
        for commit in commits:
            result.append({
                "sha": commit.sha[:7],
                "message": commit.commit.message.splitlines()[0],
                "author": commit.commit.author.name,
                "date": str(commit.commit.author.date),
            })
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)})


ALL_TOOLS = [
    get_repo_metadata,
    get_readme,
    get_file_tree,
    read_file,
    detect_tech_stack,
    get_recent_commits,
]
