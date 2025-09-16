"""analyzer.py
Вспомогательные методы: fuzzy matching, фильтры, статистика.
Содержит легкое API для фронтэнда, если тот будет спрашивать аналитические данные.
"""
from typing import List, Tuple
import difflib


def fuzzy_match(query: str, choices: List[str], cutoff: float = 0.6) -> List[Tuple[str, float]]:
    """Возвращает отсортированный список (choice, score) c score от 0..1"""
    matches = difflib.get_close_matches(query, choices, n=10, cutoff=cutoff)
    result = []
    for m in matches:
        score = difflib.SequenceMatcher(None, query.lower(), m.lower()).ratio()
        result.append((m, score))
    result.sort(key=lambda x: x[1], reverse=True)
    return result


def stats_categories(categories: dict) -> dict:
    return {k: len(v) for k, v in categories.items()}
