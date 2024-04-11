document.addEventListener('DOMContentLoaded', function() {
    fetch('/pos/obtener-datos/')
    .then(response => response.json())
    .then(data => {
        // Procesar los datos recibidos
        const medicos = data.medicos;
        const pacientes = data.pacientes;
        const clientes = data.clientes;

        // Llenar el select de médicos
        const selectMedicos = document.getElementById('doctor');
        medicos.forEach(medico => {
            selectMedicos.innerHTML += `<option class="text-center" value="${medico.id}">${medico.user__first_name} ${medico.user__last_name}</option>`;
        });

        // Llenar el select de pacientes
        const selectPacientes = document.getElementById('mascota');
        pacientes.forEach(paciente => {
            selectPacientes.innerHTML += `<option class="text-center" value="${paciente.id}">${paciente.nombre_completo}</option>`;
        });

        // Llenar el select de clientes
        const selectClientes = document.getElementById('propietario');
        clientes.forEach(cliente => {
            selectClientes.innerHTML += `<option class="text-center" value="${cliente.id}">${cliente.user__first_name} ${cliente.user__last_name}</option>`;
        });
    })
    .catch(error => {
        console.error('Error al llamar al endpoint:', error);
    });

    // #selctores propios
    let citas = []
    let modal = document.querySelector('#myModal');
    let tipeModal;
    const modalMensaje1 = document.querySelector('.mensaje1');
    const modalMensaje2 = document.querySelector('.mensaje2');
    let btnCloseModal = document.querySelector('.close-modal');
    let formularioCita = document.querySelector('.formulario-cita')
    const btnEditar = document.querySelector('.btn-editar');
    const btnEliminar = document.querySelector('.btn-delete');
    let btnSubmitCita = document.querySelector('.btn-submit-cita')
    let tipoAction;
    let citaId=null

    btnEditar.addEventListener('click', function(e) {
        btnSubmitCita.textContent='Guardar Cambios'
        const id = e.target.closest('.mensaje1').getAttribute('data-id');
        citaId=id
        tipeModal = 2
        tipoAction='edit'
        const cita = citas.filter(cita => cita.id==id)[0]
        console.log(cita)
        llenarFormulario(cita);
        mostrarModal()
        mostrarContenidoModal()
    });

    btnEliminar.addEventListener('click', function(e) {
        // Obtener el ID de la cita desde el atributo data
        const id = e.target.closest('.mensaje1').getAttribute('data-id');
        
        // Mostrar un mensaje de confirmación antes de eliminar
        Swal.fire({
            title: '¿Estás seguro?',
            text: "No podrás revertir esto",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Sí, eliminar cita'
        }).then((result) => {
            // Si el usuario confirma la eliminación
            if (result.isConfirmed) {
                // Realizar la eliminación de la cita
                eliminarCita(id);
            }
        });
    });

    const pElementsMensaje1 = modalMensaje1.querySelectorAll('p');

    const asunto = pElementsMensaje1[0];
    console.log(asunto)
    const descripcion = pElementsMensaje1[1];
    const fechaCita = pElementsMensaje1[2];
    const horaCita = pElementsMensaje1[3];
    const estado = pElementsMensaje1[4];
    const medico = pElementsMensaje1[5];
    const propietario = pElementsMensaje1[6];
    const paciente = pElementsMensaje1[7];


    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
        firstDay: 1, 
        initialView: 'dayGridMonth',
        locale: 'es',
        headerToolbar: {
            left: 'prevYear prev,next nextYear',
            center: 'title',
            right: 'today dayGridMonth,timeGridWeek,listWeek'
        },
        buttonText: {
            today: 'Hoy',
            month: 'Mes',
            week: 'Semana',
            day: 'Día',
            list: 'Lista'
        },
        views: {
            timeGrid: {
                buttonText: 'Día'
            }
        },
        events: {
            url: '/pos/api/citas/',  // URL de tu endpoint que devuelve las citas
            method: 'GET',
            failure: function() {
                alert('Error al cargar las citas');
            },
            success: function(data) {
                citas = data
                // Procesar los datos de las citas
                var eventos = data.map(function(cita) {
                    return {
                        id: cita.id,
                        title: cita.asunto,  // Puedes usar el asunto como título del evento
                        start: cita.fecha_cita + 'T' + cita.hora_cita,  // Combinar fecha y hora
                        cita: cita
                    };
                });
                calendar.removeAllEvents();
                // Agregar los nuevos eventos al calendario
                calendar.addEventSource(eventos);
            }
        },
        dateClick: function(info) {
            btnSubmitCita.textContent='Registrar'
            tipeModal = 2;
            tipoAction = 'add'
            citaId=null
            mostrarModal();
            mostrarContenidoModal()
            const fechaInput = document.getElementById('fecha');
            const date = info.date;
            const formattedDate = date.getFullYear() + '-' + (date.getMonth() + 1).toString().padStart(2, '0') + '-' + date.getDate().toString().padStart(2, '0');
            fechaInput.value = formattedDate;
        },
        eventClick: function(info) {
            var eventoCompleto = info.event.extendedProps.cita;
            tipeModal = 1;
            mostrarModal();
            mostrarContenidoModal(eventoCompleto);
        }
    });
    calendar.render();
    
    formularioCita.addEventListener('submit', (e) => {
        e.preventDefault();
        console.log(tipoAction);
        const formData = new FormData(formularioCita);
        let camposVacios = false;
        for (let pair of formData.entries()) {
            if (pair[1].trim() === '') { 
                camposVacios = true;
                break;
            }
        }
        if (camposVacios) {
            Swal.fire({
                icon: 'error',
                title: 'Error al registrar la cita',
                text: 'Porfavor ingresa todos los datos'
            });
        } else {
            enviarFormulario(formData)
        }
    });
    function llenarFormulario(cita) {
        document.getElementById('asunto').value = cita.asunto;
        document.getElementById('descripcion').value = cita.descripcion;
        document.getElementById('fecha').value = cita.fecha_cita;
        document.getElementById('hora').value = cita.hora_cita;
        document.getElementById('doctor').value = cita.medico.id;
        document.getElementById('mascota').value = cita.mascota.id; 
        document.getElementById('propietario').value = cita.propietario.id;
    }
    function mostrarModal() {
        modal.style.display = 'block';
    }

    btnCloseModal.addEventListener('click', () => {
        modal.style.display = 'none';
        formularioCita.reset()
    });

    function mostrarContenidoModal(eventoCompleto) {
        if (tipeModal==1) {
            modalMensaje1.style.display = 'block';
            modalMensaje2.style.display = 'none';
            cargarDatosDetalle(eventoCompleto)
            
        }else{
            modalMensaje1.style.display = 'none';
            modalMensaje2.style.display = 'block';
        }
    }

    function cargarDatosDetalle(evento){
        asunto.textContent = evento.asunto
        descripcion.textContent = evento.descripcion
        fechaCita.textContent = evento.fecha_cita
        horaCita.textContent = evento.hora_cita
        if (evento.estado == false) {
            estado.textContent = 'Pendiente'
        }else{
            estado.textContent = 'Atendido'
        }
        medico.textContent = evento.medico.nombre + ' ' + evento.medico.apellidos
        propietario.textContent = evento.propietario.nombre + ' ' + evento.propietario.apellidos
        paciente.textContent = evento.mascota.nombre

        modalMensaje1.setAttribute('data-id', evento.id);
    }

    function enviarFormulario(formData){
        let url;
        if (citaId!=null) {
            url = `/pos/crm/cita/js/edit/${citaId}/`
        }else{
            url = '/pos/crm/cita/js/add/'
        }
        console.log(url)
        fetch(url, {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.mensaje) {
                // Mostrar SweetAlert de éxito
                Swal.fire({
                    icon: 'success',
                    title: data.mensaje,
                    text: 'ID de la cita: ' + data.id_cita,
                });
                btnCloseModal.click();
                calendar.getEvents().forEach(event => event.remove());
                calendar.refetchEvents();
            } else {
                // Mostrar SweetAlert de error
                Swal.fire({
                    icon: 'error',
                    title: 'Error al registrar la cita',
                    text: data.error
                });
            }
        })
        .catch(error => {
            // Mostrar SweetAlert de error en caso de falla en la solicitud
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: 'Error al registrar la cita. Por favor, inténtelo de nuevo.'
            });
            console.error(error)
        });
    }

    function eliminarCita(id) {
        const csrftoken = getCookie('csrftoken');
        fetch(`/pos/crm/cita/js/delete/${id}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.mensaje) {
                Swal.fire(
                    '¡Eliminada!',
                    data.mensaje,
                    'success'
                );
                btnCloseModal.click();
                calendar.getEvents().forEach(event => event.remove());
                calendar.refetchEvents();
            }else{
                Swal.fire(
                    'Error',
                    'Hubo un problema al eliminar la cita.',
                    data.error
                );
            }
            
        })
        .catch(error => {
            // Mostrar mensaje de error si la eliminación falla
            Swal.fire(
                'Error',
                'Hubo un problema al eliminar la cita.',
                'error'
            );
            console.error(error)
        });
    }
});
