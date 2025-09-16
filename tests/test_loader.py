from src.core.loader import parse_mods_txt
import tempfile


def test_parse_basic():
    sample = """
Глобальные:
A
B

Аддоны:
A Addon
OtherAddon

Вспомогательные:
Helper
"""
    with tempfile.NamedTemporaryFile('w+', encoding='utf-8', delete=False) as f:
        f.write(sample)
        f.flush()
        res = parse_mods_txt(f.name)
    assert 'Глобальные' in res
    assert res['Глобальные'] == ['A', 'B']
    assert 'Аддоны' in res and 'A Addon' in res['Аддоны']
