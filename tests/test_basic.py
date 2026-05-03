import pytest
import os
from src.utils.parsers import parse_requirements_txt, detect_framework_signatures


def test_parse_requirements_txt_basic():
    content = """
# Bu bir yorum
requests>=2.28.0
flask==2.3.0

# Boş satır üstünde
django>=4.0,<5.0
"""
    result = parse_requirements_txt(content)
    assert "requests" in result
    assert "flask" in result
    assert "django" in result
    assert len([r for r in result if r.startswith("#")]) == 0


def test_parse_requirements_txt_empty():
    assert parse_requirements_txt("") == []
    assert parse_requirements_txt("# sadece yorum") == []


def test_detect_framework_signatures_dockerfile():
    files = ["Dockerfile", "README.md", "src/main.py"]
    result = detect_framework_signatures(files)
    assert "Docker" in result


def test_detect_framework_signatures_multiple():
    files = ["next.config.js", "Dockerfile", "docker-compose.yml", ".github/workflows/ci.yml"]
    result = detect_framework_signatures(files)
    assert "Next.js" in result
    assert "Docker" in result
    assert "Docker Compose" in result
    assert "GitHub Actions" in result


def test_detect_framework_signatures_empty():
    assert detect_framework_signatures([]) == []
    assert detect_framework_signatures(["random.txt"]) == []


def test_config_validate_missing_env():
    from src.config import Config
    original_token = Config.GITHUB_TOKEN
    original_key = Config.ANTHROPIC_API_KEY

    Config.GITHUB_TOKEN = ""
    Config.ANTHROPIC_API_KEY = ""

    with pytest.raises(ValueError, match="GITHUB_TOKEN"):
        Config.validate()

    Config.GITHUB_TOKEN = original_token
    Config.ANTHROPIC_API_KEY = original_key


def test_config_validate_missing_api_key():
    from src.config import Config
    original_token = Config.GITHUB_TOKEN
    original_key = Config.ANTHROPIC_API_KEY
    original_provider = Config.LLM_PROVIDER

    Config.GITHUB_TOKEN = "fake_token"
    Config.ANTHROPIC_API_KEY = ""
    Config.LLM_PROVIDER = "anthropic"

    with pytest.raises(ValueError, match="ANTHROPIC_API_KEY"):
        Config.validate()

    Config.GITHUB_TOKEN = original_token
    Config.ANTHROPIC_API_KEY = original_key
    Config.LLM_PROVIDER = original_provider