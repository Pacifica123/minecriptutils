"""main.py
Собирает pipeline: парсер -> graph_builder -> visualizer
Пример:
python -m src.main data/mods_list_example.txt output/mods_graph.html --bg-color '#101010' --templates src/visualizer/templates
"""
import argparse
import os
from src.core.loader import parse_mods_txt
from src.core.graph_builder import ModsGraph
from src.visualizer.visualizer import Visualizer
from src.core.analyzer import stats_categories
from src.visualizer import __name__ as vis_mod


def main():
    p = argparse.ArgumentParser()
    p.add_argument('input')
    p.add_argument('output')
    p.add_argument('--templates', help='Путь к папке с template файлами (custom.js/custom.css)', default=None)
    p.add_argument('--bg-color', help='Background color like #101010', default=None)
    p.add_argument('--bg-image', help='Background image url or path', default=None)
    args = p.parse_args()

    cats = parse_mods_txt(args.input)
    print('Категории:', stats_categories(cats))

    default_config = {
        'colors': {
            'Глобальные': '#1f77b4',
            'Аддоны': '#2ca02c',
            'Вспомогательные': '#7f7f7f'
        },
        'sizes': {
            'Глобальные': 40,
            'Аддоны': 16,
            'Вспомогательные': 24
        },
        'styles': {},
        'fallback_color': '#aaaaaa'
    }

    mg = ModsGraph(cats, default_config)
    G = mg.to_networkx()

    viz = Visualizer(G, config=default_config)
    bg = None
    if args.bg_color:
        bg = {'type': 'color', 'value': args.bg_color}
    elif args.bg_image:
        bg = {'type': 'image', 'value': args.bg_image}

    os.makedirs(os.path.dirname(args.output) or '.', exist_ok=True)
    viz.render(args.output, template_dir=args.templates, bg=bg)
    print('Генерация завершена:', args.output)


if __name__ == '__main__':
    main()
