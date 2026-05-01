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

  document.querySelectorAll('.js-confirm-cancel').forEach(form => {

    form.addEventListener('submit', function (e) {
      e.preventDefault(); // ⛔ detenemos el submit NORMAL

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
          form.submit(); // ✅ enviamos el FORM original
        }
      });

    });

  });

});


document.addEventListener('DOMContentLoaded', function () {

  document.querySelectorAll('.js-confirm-asistir').forEach(form => {

    form.addEventListener('submit', function (e) {
      e.preventDefault();

      const fechaReserva = new Date(form.querySelector('input[name="fecha"]').value);
      const hoy = new Date();
      hoy.setHours(0,0,0,0);

      if (fechaReserva > hoy) {
        Swal.fire({
          icon: 'info',
          title: 'Aún no disponible',
          text: 'Solo puedes marcar asistencia después de la fecha de la clase.',
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

