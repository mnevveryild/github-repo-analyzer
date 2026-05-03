import json
import re
from typing import Dict, List, Any

try:
    import tomli
except ImportError:
    tomli = None


def parse_package_json(content: str) -> Dict[str, List[str]]:
    try:
        data = json.loads(content)
        return {
            "dependencies": list(data.get("dependencies", {}).keys()),
            "devDependencies": list(data.get("devDependencies", {}).keys()),
            "scripts": list(data.get("scripts", {}).keys()),
        }
    except Exception:
        return {"dependencies": [], "devDependencies": [], "scripts": []}


def parse_requirements_txt(content: str) -> List[str]:
    result = []
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        pkg = re.split(r"[<>=!~]", line)[0].strip()
        if pkg:
            result.append(pkg)
    return result


def parse_pyproject_toml(content: str) -> List[str]:
    if tomli is None:
        return []
    try:
        data = tomli.loads(content)
        deps = []
        # Poetry format
        poetry_deps = data.get("tool", {}).get("poetry", {}).get("dependencies", {})
        for k in poetry_deps:
            if k.lower() != "python":
                deps.append(k)
        # PEP 621 format
        pep621_deps = data.get("project", {}).get("dependencies", [])
        for dep in pep621_deps:
            pkg = re.split(r"[<>=!~\s\[]", dep)[0].strip()
            if pkg and pkg.lower() != "python":
                deps.append(pkg)
        return list(dict.fromkeys(deps))
    except Exception:
        return []


FRAMEWORK_SIGNATURES: Dict[str, str] = {
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


def detect_framework_signatures(file_paths: List[str]) -> List[str]:
    detected = []
    for fp in file_paths:
        for sig, framework in FRAMEWORK_SIGNATURES.items():
            if sig in fp and framework not in detected:
                detected.append(framework)
    return detected
