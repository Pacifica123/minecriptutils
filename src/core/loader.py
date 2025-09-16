"""loader.py
Парсер входного txt. Возвращает словарь категорий -> список модов.
Поддерживает заголовки с двоеточием. Если аддон явно содержит имя глобального мода —
то он не связывается здесь, это делается в graph_builder (чтобы separation of concerns).
"""
from typing import Dict, List
import re

CATEGORY_RE = re.compile(r"^([\w \u0400-\u04FF'\-\.]+):$", flags=re.UNICODE)


def parse_mods_txt(path: str) -> Dict[str, List[str]]:
    categories: Dict[str, List[str]] = {}
    current = None
    with open(path, encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line:
                continue
            m = CATEGORY_RE.match(line)
            if m:
                current = m.group(1).strip()
                categories.setdefault(current, [])
                continue
            if current is None:
                # если файл начинается без категории — положим в 'Глобальные'
                current = "Глобальные"
                categories.setdefault(current, [])
            categories.setdefault(current, []).append(line)
    return categories


if __name__ == '__main__':
    import argparse, json
    p = argparse.ArgumentParser()
    p.add_argument('input')
    p.add_argument('--show', action='store_true')
    args = p.parse_args()
    res = parse_mods_txt(args.input)
    if args.show:
        print(json.dumps(res, ensure_ascii=False, indent=2))
