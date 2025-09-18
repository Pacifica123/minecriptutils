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


// Панель инструментов
(function() {
    if (typeof network === 'undefined') {
        setTimeout(initToolbar, 300);
    } else {
        initToolbar();
    }

    function initToolbar() {
        if (typeof network === 'undefined' || !network.body) return;

        const toolbar = document.createElement('div');
        toolbar.id = 'toolbar';

        toolbar.innerHTML = `
        <button id="btnUndo">Undo (Ctrl+Z)</button>
        <button id="btnRedo">Redo (Ctrl+Y)</button>
        <button id="btnExport">Export JSON</button>
        <input type="file" id="btnImport" style="display:none" />
        <button id="btnImportTrigger">Import JSON</button>
        `;

        document.body.appendChild(toolbar);

        // Undo — просто триггерим Ctrl+Z событие, чтобы не плодить дублей
        document.getElementById('btnUndo').addEventListener('click', () => {
            const event = new KeyboardEvent('keydown', {key: 'z', ctrlKey: true});
            document.dispatchEvent(event);
        });

        // Redo — пока пустая заглушка
        document.getElementById('btnRedo').addEventListener('click', () => {
            alert("Redo пока не реализован");
        });

        // Export
        document.getElementById('btnExport').addEventListener('click', () => {
            const nodes = network.body.data.nodes.get();
            const edges = network.body.data.edges.get();
            const json = JSON.stringify({nodes, edges}, null, 2);
            const blob = new Blob([json], {type: 'application/json'});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = "graph.json";
            a.click();
            URL.revokeObjectURL(url);
        });

        // Import
        const importFile = document.getElementById('btnImport');
        document.getElementById('btnImportTrigger').addEventListener('click', () => importFile.click());
        importFile.addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (!file) return;
            const reader = new FileReader();
            reader.onload = function(evt) {
                const json = JSON.parse(evt.target.result);
                network.body.data.nodes.clear();
                network.body.data.edges.clear();
                network.body.data.nodes.add(json.nodes);
                network.body.data.edges.add(json.edges);
            };
            reader.readAsText(file);
        });
    }
})();
