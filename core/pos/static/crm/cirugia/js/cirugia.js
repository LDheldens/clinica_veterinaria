document.addEventListener('DOMContentLoaded', () => {
    const propietarioField = document.querySelector('#id_cliente');
    const mascotaField = document.querySelector('#id_paciente');

    propietarioField.addEventListener('change', async (e) => {
        const propietarioId = e.target.value;

        // Limpia las opciones actuales del campo de mascota
        mascotaField.innerHTML = '';

        if (!propietarioId) {
            return;
        }

        try {
            const response = await fetch(`/pos/crm/cita/cargar_mascotas/?propietario_id=${propietarioId}`);
            const data = await response.json();
            console.log(data);
            // Agrega las opciones de mascotas al campo de mascota
            data.mascotas.forEach(mascota => {
                const option = document.createElement('option');
                option.value = mascota.id;
                option.textContent = mascota.nombre;
                mascotaField.appendChild(option);
            });
        } catch (error) {
            console.error('Error al cargar las mascotas:', error);
        }
    });
});
