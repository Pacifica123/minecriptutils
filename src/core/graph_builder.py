"""graph_builder.py
Построение графа из данных парсера. Экспортирует класс ModsGraph.
Он содержит методы для добавления/удаления узлов и рёбер, изменения стилей.
Гарантирует, что core не зависит от визуализации.
"""
from typing import Dict, List, Optional, Any
import networkx as nx


class ModsGraph:
    def __init__(self, categories: Dict[str, List[str]], default_config: Optional[dict] = None):
        self.categories = categories
        self.config = default_config or {}
        # используем направленный граф; неориентированные связи можно представлять как пару ребер
        self.G = nx.DiGraph()
        self._init_nodes()
        self._auto_link_addons()

    def _init_nodes(self):
        for cat, mods in self.categories.items():
            for m in mods:
                self.add_node(m, category=cat)

    def add_node(self, name: str, category: str, **attrs: Any):
        base = {
            'label': name,
            'category': category,
            'size': self.config.get('sizes', {}).get(category, 20),
            'color': self.config.get('colors', {}).get(category),
            'style': self.config.get('styles', {}).get(category, {}),
        }
        base.update(attrs)
        self.G.add_node(name, **base)

    def remove_node(self, name: str):
        if name in self.G:
            self.G.remove_node(name)

    def add_edge(self, a: str, b: str, directed: bool = True, **attrs: Any):
        if directed:
            self.G.add_edge(a, b, **attrs)
        else:
            # симуляция неориентированного ребра — пара направленных
            self.G.add_edge(a, b, **attrs)
            self.G.add_edge(b, a, **attrs)

    def remove_edge(self, a: str, b: str):
        if self.G.has_edge(a, b):
            self.G.remove_edge(a, b)

    def set_node_attr(self, name: str, **attrs: Any):
        if name in self.G.nodes:
            self.G.nodes[name].update(attrs)

    def set_edge_attr(self, a: str, b: str, **attrs: Any):
        if self.G.has_edge(a, b):
            self.G.edges[a, b].update(attrs)

    def _auto_link_addons(self):
        # Простая логика: для каждого аддона ищем вхождение глобального имени.
        globals_ = self.categories.get('Глобальные', []) + self.categories.get('Global', [])
        addons = self.categories.get('Аддоны', []) + self.categories.get('Addons', [])
        for addon in addons:
            a_low = addon.lower()
            for g in globals_:
                if g.lower() in a_low:
                    # связь: addon -> global (relation addon_of)
                    if not self.G.has_edge(addon, g):
                        self.G.add_edge(addon, g, relation='addon_of')
                    break

    def to_networkx(self) -> nx.DiGraph:
        return self.G
