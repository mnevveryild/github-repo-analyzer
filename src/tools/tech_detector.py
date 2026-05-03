from typing import Dict, Any
from github import Github
from src.config import Config
from src.utils.parsers import (
    parse_package_json,
    parse_requirements_txt,
    parse_pyproject_toml,
    detect_framework_signatures,
)


def detect_tech_stack(repo_url: str) -> Dict[str, Any]:
    try:
        client = Github(Config.GITHUB_TOKEN)
        path = repo_url.replace("https://github.com/", "").strip("/")
        owner_repo = "/".join(path.split("/")[:2])
        repo = client.get_repo(owner_repo)

        languages = dict(repo.get_languages())

        dependencies: Dict[str, Any] = {}
        dep_files = {
            "package.json": parse_package_json,
            "requirements.txt": parse_requirements_txt,
            "pyproject.toml": parse_pyproject_toml,
            "Cargo.toml": None,
            "go.mod": None,
            "pom.xml": None,
            "Gemfile": None,
        }

        for filename, parser in dep_files.items():
            try:
                file_content = repo.get_contents(filename)
                content = file_content.decoded_content.decode("utf-8")
                if parser:
                    dependencies[filename] = parser(content)
                else:
                    dependencies[filename] = content[:500]
            except Exception:
                pass

        root_contents = repo.get_contents("")
        file_paths = [f.path for f in root_contents]
        # Also check .github/workflows
        try:
            gh_contents = repo.get_contents(".github/workflows")
            if gh_contents:
                file_paths.append(".github/workflows")
        except Exception:
            pass

        frameworks = detect_framework_signatures(file_paths)

        return {
            "languages": languages,
            "dependencies": dependencies,
            "frameworks": frameworks,
            "file_signatures": file_paths,
        }
    except Exception as e:
        return {"error": str(e)}
