from pathlib import Path
from string import Template
from typing import Any

PROMPT_DIR = Path(__file__).parent

_USER_INPUT_OPEN = "<USER_INPUT"
_USER_INPUT_CLOSE = "</USER_INPUT>"


def _sanitize_untrusted(value: Any) -> str:
    if value is None:
        return ""
    text = str(value)
    return text.replace(_USER_INPUT_CLOSE, "[/USER_INPUT]").replace(
        _USER_INPUT_OPEN, "[USER_INPUT"
    )


def wrap_untrusted(label: str, value: Any) -> str:
    safe_label = label.replace('"', "'")
    safe_value = _sanitize_untrusted(value)
    return f'<USER_INPUT type="{safe_label}">\n{safe_value}\n</USER_INPUT>'


def load_prompt(name: str, **vars: Any) -> str:
    template_text = (PROMPT_DIR / name).read_text(encoding="utf-8")
    return Template(template_text).safe_substitute(**vars).strip()
