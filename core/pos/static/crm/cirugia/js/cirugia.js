document.addEventListener('DOMContentLoaded', () => {
    let idMedico = null;
    let idPropietario = null;
    let idMascota = null;
    const btnFormato = document.querySelector('#btn-formato-pdf')

    const propietarioField = document.querySelector('#id_cliente');
    const mascotaField = document.querySelector('#id_paciente');
    const medicoField = document.querySelector('#id_medico');

    propietarioField.addEventListener('change', async (e) => {
        idPropietario = e.target.value
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
    mascotaField.addEventListener('change',(e)=>{
        idMascota = e.target.value
    })
    medicoField.addEventListener('change',(e)=>{
        idMedico= e.target.value
    })

    btnFormato.addEventListener('click', (e) => {
        if (idMedico == null || idPropietario == null || idMascota == null) {
            alert('Ingresa todos los campos')
            return;
        } 
        const fecha = document.getElementById('id_fecha').value; // Obtener el valor del campo fecha
        const hora = document.getElementById('id_hora').value; // Obtener el valor del campo hora
        const url = `/pos/crm/cirugia/print/${idMascota}/${idPropietario}/${idMedico}/${fecha}/${hora}`;
        

        // Abre una nueva pestaña en el navegador con la URL especificada
        window.open(url, '_blank');
    });

});
