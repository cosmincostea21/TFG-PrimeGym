/**
 * Buscador genérico para tablas de admin.
 * Uso en HTML:
 *   <input id="searchInput"
 *          data-admin-search="ID_DEL_TBODY"
 *          data-admin-empty="ID_DEL_DIV_VACIO_OPCIONAL">
 *
 * Cada <tr> debe tener una celda con class="nombre".
 */
document.querySelectorAll("[data-admin-search]").forEach(input => {
    const tbody = document.getElementById(input.dataset.adminSearch);
    if (!tbody) return;

    const empty = input.dataset.adminEmpty
        ? document.getElementById(input.dataset.adminEmpty)
        : null;

    const rows = tbody.querySelectorAll("tr");

    input.addEventListener("keyup", function () {
        const value = this.value.toLowerCase().trim();
        let visibles = 0;

        rows.forEach(row => {
            const nombreEl = row.querySelector(".nombre");
            if (!nombreEl) return;

            const nombre = nombreEl.innerText.toLowerCase();
            const match  = nombre.includes(value);

            row.style.display = match ? "" : "none";
            if (match) visibles++;
        });

        if (empty) empty.hidden = visibles !== 0;
    });
});