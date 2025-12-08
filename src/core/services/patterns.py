from typing import TypedDict

from src.constants import Language


class Patterns(TypedDict):
    language: Language
    patterns: list[str]


# Injections
injections_en: Patterns = {
    "language": Language.EN,
    "patterns": [
        r"ignore\s+(previous|all|above)",
        r"disregard\s+(previous|all|above)",
        r"forget\s+(previous|all|above)",
        r"new\s+instructions?",
        r"system\s*:",
        r"<\s*system\s*>",
        r"\[\s*system\s*\]",
        r"you\s+are\s+now",
        r"act\s+as\s+if",
        r"pretend\s+(you|to\s+be)",
        r"roleplay\s+as",
        r"translate\s+everything\s+to",
        r"respond\s+in\s+(chinese|chinese|arabic|korean)"
    ]
}

injections_ru: Patterns = {
    "language": Language.RU,
    "patterns": [
        r"отвечай\s+на\s+(китайском|арабском|корейском)",
        r"переведи\s+всё\s+на",
        r"ты\s+теперь",
        r"новые\s+инструкции",
        r"игнорируй\s+(предыдущ|всё|выше)",
        r"забудь\s+(предыдущ|всё|выше)",
        ]
    }

# Remote Code Execution
rce_en: Patterns = {
    "language": Language.RU,
    "patterns": [
            r"exec\s*\(",
            r"eval\s*\(",
            r"os\s*\.\s*system",
            r"subprocess",
            r"import\s+os",
            r"__import__",
            r"cat\s+/etc/",
            r"cat\s+~/.ssh",
            r"rm\s+-rf",
            r"/bin/(ba)?sh",
            r"curl\s+.+\s*\|",
            r"wget\s+.+\s*\|",
            r"execute\s+command",
            r"run\s+command",
            r"shell\s+command",
        ]
}

rce_ru: Patterns = {
    "language": Language.RU,
    "patterns": [
            r"выполни\s+команду",
            r"запусти\s+скрипт",
        ]
}

recon_en: Patterns = {
    "language": Language.EN,
    "patterns": [
        r"what\s+(model|ai|llm)\s+are\s+you",
        r"your\s+api\s+key",
        r"show\s+(me\s+)?your\s+(config|settings|prompt)",
        r"what\s+is\s+your\s+system\s+prompt",
        r"dump\s+(your\s+)?(memory|context|instructions)",
        r"print\s+(your\s+)?(instructions|prompt)",
    ]
}

recon_ru: Patterns = {
    "language": Language.RU,
    "patterns": [
        r"какая\s+ты\s+модель",
        r"какой\s+у\s+тебя\s+api",
        r"твой\s+api\s+ключ",
        r"покажи\s+(свой\s+)?(конфиг|настройки|промпт)",
        r"какой\s+твой\s+системный\s+промпт",
    ]
}

spam_en: Patterns = {
    "language": Language.EN,
    "patterns": [
        r"(.)\1{10,}",  # Same character 10+ times
        r"(test\s*){5,}",  # "test" repeated 5+ times
        r"^[a-z]{50,}$",  # 50+ lowercase letters without spaces
        r"^[A-Z]{50,}$",  # 50+ uppercase letters without spaces
    ]
}

spam_ru: Patterns = {
    "language": Language.RU,
    "patterns": [
        r"(тест\s*){5,}",  # "test" repeated 5+ times
        r"^[а-я]{50,}$",  # 50+ lowercase letters without spaces
        r"^[А-Я]{50,}$",  # 50+ uppercase letters without spaces
    ]
}

token_exhaustion_en: Patterns = {
    "language": Language.EN,
    "patterns": [
        r"write\s+(a\s+)?(story|essay|text)\s+(of\s+)?\d{3,}\s+(words|characters)",  # noqa: E501
        r"generate\s+\d{3,}\s+(words|characters|lines)",
        r"repeat\s+.+\s+\d{3,}\s+times",
        ]
}

token_exhaustion_ru: Patterns = {
    "language": Language.EN,
    "patterns": [
        r"напиши\s+(рассказ|историю|текст|эссе)\s+на\s+\d{3,}\s+(слов|символов)",  # noqa: E501
        r"сгенерируй\s+\d{3,}\s+(слов|символов|строк)",
        r"повтори\s+.+\s+\d{3,}\s+раз",
        ]
}

all_patterns = [
    injections_en, injections_ru,
    rce_en, rce_ru,
    recon_en, recon_ru,
    spam_en, spam_ru,
    token_exhaustion_en, token_exhaustion_ru
]
