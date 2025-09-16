from src.core.loader import parse_mods_txt
from src.core.graph_builder import ModsGraph
import tempfile


def test_auto_linking():
    sample = """
Глобальные:
Mek

Аддоны:
Mek Tools
"""
    with tempfile.NamedTemporaryFile('w+', encoding='utf-8', delete=False) as f:
        f.write(sample); f.flush()
        cats = parse_mods_txt(f.name)
    mg = ModsGraph(cats)
    G = mg.to_networkx()
    assert ('Mek Tools', 'Mek') in G.edges
