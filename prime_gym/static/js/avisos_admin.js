document.addEventListener('DOMContentLoaded', function () {

  // ✅ CONFIRMAR CANCELACIÓN (FORM)
  document.querySelectorAll('.js-confirm-cancel').forEach(form => {
    form.addEventListener('click', function (e) {
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

  // ✅ CONFIRMAR ELIMINACIÓN (LINK)
  document.querySelectorAll('.js-confirm-eliminar').forEach(link => {
    link.addEventListener('click', function (e) {
      e.preventDefault(); // ⛔ evitamos navegar directamente

      const url = this.href;

      Swal.fire({
        title: '¿Eliminar entrenador?',
        text: 'Esta acción no se puede deshacer',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Sí, eliminar',
        cancelButtonText: 'No',
        confirmButtonColor: '#e3342f',
        cancelButtonColor: '#6c757d',
      }).then((result) => {
        if (result.isConfirmed) {
          window.location.href = url; // ✅ redirige
        }
      });
    });
  });

});