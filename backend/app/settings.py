import os
from typing import Optional


def get_project_root() -> str:
    # Workspace root is two levels up from this file (backend/app -> workspace)
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def get_templates_dir() -> str:
    root = get_project_root()
    return os.path.join(root, "templates")


def get_examples_output_dir_default() -> str:
    root = get_project_root()
    return os.path.join(root, "examples", "output")


def get_output_dir() -> str:
    output_dir = os.getenv("OUTPUT_DIR") or get_examples_output_dir_default()
    os.makedirs(output_dir, exist_ok=True)
    return output_dir


def is_mock_llm_enabled() -> bool:
    return (os.getenv("MOCK_LLM", "false").lower() == "true")


def get_openai_api_key() -> Optional[str]:
    return os.getenv("OPENAI_API_KEY")


