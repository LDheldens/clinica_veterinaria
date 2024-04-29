let contenedorModal;
let modal;
let btnCloseModal;
let formReceta;
let formHospitalizacion;
let formCirugia;
let pacienteId = null;
let clienteId = null;
let medicoId = null;
let tableTitulares;
let btnAgregarMedicamento; 
let contenedorMedicamentos; 
let divReceta;
let sectionReceta;
let sectionHospitalizacion;
let sectionCirugia;
let contadorMedicamentos = 0;

document.addEventListener('DOMContentLoaded',()=>{
    contenedorModal = document.querySelector('#contenedor-modal')
    modal = document.querySelector('#modalXd')
    btnCloseModal = document.querySelector('.btn-close-modal')
    btnAgregarMedicamento = document.getElementById('btn-agregar-medicamento');
    contenedorMedicamentos = document.getElementById('contenedor-medicamentos');
    btnCloseModal.addEventListener('click',cerrarModal)
    formReceta = document.querySelector('#formReceta')
    formHospitalizacion= document.querySelector('#formHospitalizacion')
    formCirugia = document.querySelector('#formCirugia')
    divReceta = document.querySelector('.receta')
    sectionReceta = document.querySelector('.sectionReceta')
    sectionHospitalizacion = document.querySelector('.sectionHospitalizacion')
    sectionCirugia = document.querySelector('.sectionCirugia')
    const btnFormato = document.querySelector('#btn-formato-pdf')

    btnAgregarMedicamento.addEventListener('click', (e)=>{
        e.preventDefault()
        agregarMedicamentoFormulario()
    });
    formReceta.addEventListener('submit', enviarFormulario)
    formHospitalizacion.addEventListener('submit', enviarFormularioH)
    formCirugia.addEventListener('submit',enviarFormularioC)

    // #logica para obtener el formato pdf
    btnFormato.addEventListener('click', (e) => {
        if (medicoId == null || clienteId == null || pacienteId == null) {
            alert('Ingresa todos los campos')
            return;
        } 
        const fecha = document.getElementById('fecha').value; // Obtener el valor del campo fecha
        const hora = document.getElementById('hora').value; // Obtener el valor del campo hora

        if (fecha=='' || hora=='') {
            alert('Ingresa todos los campos de fecha y hora')
            return;
        }
        const url = `/pos/crm/cirugia/print/${pacienteId}/${clienteId}/${medicoId}/${fecha}/${hora}`;
        

        // Abre una nueva pestaña en el navegador con la URL especificada
        window.open(url, '_blank');
    });
   
})

function enviarFormularioC(e){
    e.preventDefault(); // Evita que el formulario se envíe normalmente

    // Crea un nuevo objeto FormData
    const formData = new FormData(formCirugia);

    formData.append('paciente', pacienteId);
    formData.append('cliente', clienteId);
    formData.append('medico', medicoId);
    formData.append('action', 'add2');
    const firmaInput = document.getElementById('firma_propietario');

    formData.append('firma_propietario', firmaInput.files[0]);


    for (const pair of formData.entries()) {
        console.log(pair[0] + ': ' + pair[1]);
    }

    let campoVacioEncontrado = false;

    for (let pair of formData.entries()) {
        if (!pair[1]) { // Si el valor del campo es vacío (falsy)
            campoVacioEncontrado = true;
            break; // Detener la iteración
        }
    }

    if (campoVacioEncontrado) {
        Toastify({
            text: "Por favor, complete todos los campos antes de enviar el formulario.",
            duration: 3000, 
            gravity: "top-center", 
            backgroundColor: "linear-gradient(to right, #ff0000, #ff3333)", // 
            close: true, 
            stopOnFocus: true, 
            className: "toastify-error",
            icon: "error" 
        }).showToast();
        return; 
    }
    
    // Enviar los datos mediante fetch
    fetch('/pos/crm/cirugia/add/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken') // Asegúrate de tener la función getCookie definida
        },
        body: formData
    })
    .then(response => {
        if (response.ok) {
            console.log('Cirugia creada exitosamente');
            btnCloseModal.click()
            Toastify({
                text: "Cirugia generada de manera exitosa",
                duration: 3000, // Duración en milisegundos
                gravity: "top", // Posición de la notificación: "top", "bottom", "center"
                backgroundColor: "linear-gradient(to right, #00b09b, #96c93d)", // Color de fondo
            }).showToast();
        } else {
            console.error('Error al crear la receta');
        }
    })
    .catch(error => {
        console.error('Error al enviar el formulario:', error);
    });
}
function enviarFormulario(e){
    e.preventDefault(); // Evita que el formulario se envíe normalmente

    // Crea un nuevo objeto FormData
    const formData = new FormData(formReceta);

    // Verificar si al menos el primer par de inputs está lleno
    const primerMedicamento = formData.get('medicamento1');
    const primerIndicaciones = formData.get('indicaciones1');

    if (!primerMedicamento || !primerIndicaciones) {
        alert('Por favor, ingrese el medicamento y sus indicaciones.');
        return; // Detener la ejecución si los campos no están completos
    }

    const medicamentos = [];

    // Itera sobre los campos del formulario
    for (let [key, value] of formData.entries()) {
        // Verifica si el nombre del campo incluye 'medicamento'
        if (key.includes('medicamento')) {
            // Obtiene el número del medicamento
            const numMedicamento = key.replace('medicamento', '');
            // Obtiene las indicaciones correspondientes al medicamento
            const indicaciones = formData.get(`indicaciones${numMedicamento}`);
            // Crea un objeto con el medicamento y sus indicaciones y lo agrega al array
            const medicamentoObj = {
                medicamento: value,
                indicaciones: indicaciones
            };
            if (medicamentoObj.medicamento != '' || medicamentoObj.indicaciones!=='') {
                medicamentos.push(medicamentoObj);
            }
        }
    }

    // Objeto con los datos a enviar al servidor
    const data = {
        medicamentos: medicamentos,
        pacienteId
    };

    // Enviar los datos mediante fetch
    fetch('/pos/crm/receta/add/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') // Asegúrate de tener la función getCookie definida
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (response.ok) {
            console.log('Receta creada exitosamente');
            btnCloseModal.click()
            Toastify({
                text: "Receta generada de manera exitosa",
                duration: 3000, // Duración en milisegundos
                gravity: "top", // Posición de la notificación: "top", "bottom", "center"
                backgroundColor: "linear-gradient(to right, #00b09b, #96c93d)", // Color de fondo
            }).showToast();
            
        } else {
            console.error('Error al crear la receta');
        }
    })
    .catch(error => {
        console.error('Error al enviar el formulario:', error);
    });
}

function enviarFormularioH(e) {
    e.preventDefault();

    // Crear un nuevo objeto FormData a partir del formulario
    const formData = new FormData(formHospitalizacion);

    formData.append('action', 'add2');
    formData.append('mascota', pacienteId);
    console.log(pacienteId)

    let campoVacioEncontrado = false;

    for (let pair of formData.entries()) {
        if (!pair[1]) { // Si el valor del campo es vacío (falsy)
            campoVacioEncontrado = true;
            break; // Detener la iteración
        }
    }

    if (campoVacioEncontrado) {
        Toastify({
            text: "Por favor, complete todos los campos antes de enviar el formulario.",
            duration: 3000, 
            gravity: "top-center", 
            backgroundColor: "linear-gradient(to right, #ff0000, #ff3333)", // 
            close: true, 
            stopOnFocus: true, 
            className: "toastify-error",
            icon: "error" 
        }).showToast();
        return; 
    }
    fetch('/pos/crm/hospitalizacion/add/', {
        method: 'POST',
        body: formData,
        headers:{
            'X-CSRFToken': getCookie('csrftoken') 
        }
    })
    .then(response => {
        if (response.ok) {
            // La respuesta fue exitosa, puedes mostrar una notificación de éxito o redireccionar
            console.log(response)
            btnCloseModal.click()
        } else {
            // Hubo un error en la respuesta, puedes mostrar una notificación de error
            console.error('Error al enviar el formulario');
        }
        return response.json()
    })
    .then(data=>{
        if (data.error) {
            Toastify({
                text: `${data.error}`,
                duration: 3000, 
                gravity: "top-center", 
                backgroundColor: "linear-gradient(to right, #ff0000, #ff3333)", // 
                close: true, 
                stopOnFocus: true, 
                className: "toastify-error",
                icon: "error" 
            }).showToast();
        }else{
            Toastify({
                text: "Hospitalización registrada de manera exitosa",
                duration: 3000, // Duración en milisegundos
                gravity: "top", // Posición de la notificación: "top", "bottom", "center"
                backgroundColor: "linear-gradient(to right, #00b09b, #96c93d)", // Color de fondo
            }).showToast();
        }
    })
    .catch(error => {
        // Hubo un error en el proceso de envío, puedes mostrar una notificación de error
        console.error('Error al enviar el formulario:', error);
    });


}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

function mostrarModal(){
    contenedorModal.style.display="flex"
    formReceta.reset()    
    formHospitalizacion.reset()    
    formCirugia.reset()
}

function cerrarModal(){
    contadorMedicamentos = 0
    console.log(contadorMedicamentos)
    contenedorMedicamentos.innerHTML = '';
    contenedorModal.style.display="none"
    formReceta.reset()
    formHospitalizacion.reset()
    formCirugia.reset()
}

function agregarReceta(id){
    pacienteId= id
    sectionReceta.style.display='block'
    sectionHospitalizacion.style.display='none'
    sectionCirugia.style.display='none'
    mostrarModal()
}

function agregarCirugia(idPaciente, idCliente, idMedico, idDiagnostico){
    obtenerDetalleDiagnostico(idDiagnostico,'#id_motivo')
    pacienteId= idPaciente
    clienteId = idCliente
    medicoId = idMedico
    sectionReceta.style.display='none'
    sectionHospitalizacion.style.display='none'
    sectionCirugia.style.display='block'
    mostrarModal()
}

function obtenerDetalleDiagnostico(id, selectorId) {
    // URL de la vista para obtener el detalle de la cirugía
    const url = `/pos/crm/diagnostico/${id}/`;
    fetch(url)
        .then(response => {

            if (!response.ok) {
                throw new Error('Ocurrió un error al obtener el detalle de la cirugía.');
            }

            return response.json();
        })
        .then(data => {
           document.querySelector(selectorId).value= data.motivo
        })
        .catch(error => {
            console.error(error); 
        });
}


function registrarHospitalizacion(id, idDiagnostico){
    obtenerDetalleDiagnostico(idDiagnostico,'#motivo')
    pacienteId = id
    sectionReceta.style.display='none'
    sectionCirugia.style.display='none'
    sectionHospitalizacion.style.display='block'
    mostrarModal()
}

function agregarMedicamentoFormulario() {
    contadorMedicamentos++;
    const nuevoMedicamentoDiv = document.createElement('div');
    nuevoMedicamentoDiv.classList.add('row');
    nuevoMedicamentoDiv.innerHTML = `
        <div class="form-group col-4 mb-0">
            <label for="medicamento${contadorMedicamentos}">Medicamento:</label>
            <input type="text" name="medicamento${contadorMedicamentos}" class="form-control">
        </div>
        <div class="form-group col-8 mb-0">
            <label for="indicaciones${contadorMedicamentos}">Indicaciones:</label>
            <input type="text" name="indicaciones${contadorMedicamentos}" class="form-control">
        </div>
    `;
    contenedorMedicamentos.appendChild(nuevoMedicamentoDiv);
}