const input  = document.getElementById("searchInput");
const rows   = document.querySelectorAll("#clientesTable tr.ac-row");
const empty  = document.getElementById("searchEmpty");

input.addEventListener("keyup", function () {
    const value = this.value.toLowerCase();
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
