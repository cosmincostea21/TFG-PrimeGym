(function () {
    const filters = document.querySelectorAll('.rsv-filter');
    const items   = document.querySelectorAll('.rsv-timeline-item');
    const empty   = document.querySelector('.rsv-filter-empty');
    if (!filters.length) return;

    filters.forEach(btn => {
        btn.addEventListener('click', () => {
            filters.forEach(b => b.classList.remove('is-active'));
            btn.classList.add('is-active');

            const filter = btn.dataset.filter;
            let visible = 0;

            items.forEach(item => {
                const match = filter === 'all' || item.dataset.estado === filter;
                item.hidden = !match;
                if (match) visible++;
            });

            if (empty) empty.hidden = visible !== 0;
        });
    });
})();