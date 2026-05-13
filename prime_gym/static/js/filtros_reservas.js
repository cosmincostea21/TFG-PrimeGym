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


document.addEventListener('DOMContentLoaded', function () {

  // --- ALERTA PARA ANULAR (CANCELAR) ---
  // Cambiado de .js-confirm-eliminar a .js-confirm-cancel
  document.querySelectorAll('.js-confirm-cancel').forEach(form => {
    form.addEventListener('submit', function (e) {
      e.preventDefault(); 

      Swal.fire({
        title: '¿Anular reserva?',
        text: 'Esta acción no se puede deshacer',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Sí, anular',
        cancelButtonText: 'No',
        confirmButtonColor: '#e3342f',
        cancelButtonColor: '#6c757d',
      }).then((result) => {
        if (result.isConfirmed) {
          form.submit();
        }
      });
    });
  });

  // --- ALERTA PARA ASISTENCIA ---
  document.querySelectorAll('.js-confirm-asistir').forEach(form => {
    form.addEventListener('submit', function (e) {
      e.preventDefault();

      const fechaInput = form.querySelector('input[name="fecha"]');
      if (!fechaInput) return; // Seguridad por si no encuentra el input

      const fechaReserva = new Date(fechaInput.value);
      const hoy = new Date();
      hoy.setHours(0, 0, 0, 0);

      // Si la reserva es en el futuro, no dejar marcar asistencia
      if (fechaReserva > hoy) {
        Swal.fire({
          icon: 'info',
          title: 'Aún no disponible',
          text: 'Solo puedes marcar asistencia el día de la clase o después.',
          confirmButtonText: 'Entendido',
        });
        return;
      }

      Swal.fire({
        title: '¿Marcar asistencia?',
        text: 'Confirma si asististe a esta clase',
        icon: 'question',
        showCancelButton: true,
        confirmButtonText: 'Sí, asistí',
        cancelButtonText: 'Cancelar',
      }).then(result => {
        if (result.isConfirmed) {
          form.submit();
        }
      });
    });
  });
});