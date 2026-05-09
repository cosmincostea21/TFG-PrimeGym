AOS.init();

// Obtener el botón
const scrollTopBtn = document.getElementById('scrollTopButton');

// Mostrar/ocultar el botón al hacer scroll
window.onscroll = function () {
    scrollFunction();
};

function scrollFunction() {
    // Muestra el botón después de 300px de scroll
    if (document.body.scrollTop > 300 || document.documentElement.scrollTop > 300) {
        scrollTopBtn.classList.add('show');
    } else {
        scrollTopBtn.classList.remove('show');
    }
}

// Acción al hacer clic: volver arriba suavemente
scrollTopBtn.onclick = function (e) {
    e.preventDefault(); // Prevenir comportamiento por defecto
    window.scrollTo({
        top: 0,
        behavior: 'smooth' // Desplazamiento suave
    });
}