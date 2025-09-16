# mods-graph-project (refactor)

Проект разделён на core и visualizer. Core возвращает NetworkX-graph; visualizer
отвечает за HTML/JS/CSS. Это даёт фронтендеру чистую точку входа для стилизации.

## Быстрый запуск

1. Установить зависимости

pip install -r req.txt

2. Генерация

python -m src.main data/mods_list_example.txt output/mods_graph.html --templates src/visualizer/templates --bg-color '#0b0b0b'

3. Открыть output/mods_graph.html

## Примечание для фронтенда
См документ "Инструкция фронтендеру"
