// Простая точка расширения: hotkey Ctrl+Z для отката состояния (undo).
// Примечание: pyvis/vis-network не хранит built-in историю. Это простая реализация
// которая сохраняет snapshot данных nodes/edges при изменениях из панели.
(function() {
    if (typeof network === 'undefined') {
        // network создаётся pyvis'ом позже. Попробуем найти объект через setTimeout
        setTimeout(initUndo, 300);
    } else {
        initUndo();
    }

    function initUndo() {
        if (typeof network === 'undefined' || !network.body) return;
        const history = [];
        function snapshot() {
            const nodes = network.body.data.nodes.get();
            const edges = network.body.data.edges.get();
            history.push({nodes: JSON.parse(JSON.stringify(nodes)), edges: JSON.parse(JSON.stringify(edges))});
            if (history.length > 50) history.shift();
        }
        // initial
        snapshot();

        // listen to manipulation via events
        network.on('selectNode', snapshot);
        network.on('selectEdge', snapshot);
        network.on('deselectNode', snapshot);

        document.addEventListener('keydown', function(e) {
            if ((e.ctrlKey || e.metaKey) && e.key === 'z') {
                e.preventDefault();
                if (history.length <= 1) return;
                history.pop();
                const s = history[history.length-1];
                network.body.data.nodes.clear();
                network.body.data.edges.clear();
                network.body.data.nodes.add(s.nodes);
                network.body.data.edges.add(s.edges);
            }
        });
    }
})();
