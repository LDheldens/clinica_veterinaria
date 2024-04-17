let contenedorModal;
let modal;
let btnCloseModal;
let formReceta;
let formHospitalizacion;
let pacienteId;
let recetaId;
let tableTitulares;
let btnAgregarMedicamento; 
let contenedorMedicamentos; 
let divReceta;
let sectionReceta;
let sectionHospitalizacion;
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
    divReceta = document.querySelector('.receta')
    sectionReceta = document.querySelector('.sectionReceta')
    sectionHospitalizacion = document.querySelector('.sectionHospitalizacion')

    btnAgregarMedicamento.addEventListener('click', (e)=>{
        e.preventDefault()
        agregarMedicamentoFormulario()
    });
    formReceta.addEventListener('submit', enviarFormulario)
   
})

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
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

function mostrarModal(){
    contenedorModal.style.display="flex"
    formReceta.reset()    
    formHospitalizacion.reset()    
}

function cerrarModal(){
    contenedorModal.style.display="none"
    formReceta.reset()
    formHospitalizacion.reset()
}

function agregarReceta(id, action){
    if (action=='edit') {
        recetaId = id
        pacienteId=null
        obtenerDetalleReceta(recetaId)
        console.log('Editando una receta')
    }else{
        pacienteId= id
        recetaId=null
        console.log('Agregando una receta')
    }
    sectionReceta.style.display='block'
    sectionHospitalizacion.style.display='none'
    mostrarModal()
}

function obtenerDetalleReceta(recetaId) {
    fetch(`/pos/crm/receta/${recetaId}/`) // Reemplaza '/ruta/a/la/vista/de/detalle/de/receta/' por tu ruta real
        .then(response => {
            if (!response.ok) {
                throw new Error('Error al obtener el detalle de la receta');
            }
            return response.json();
        })
        .then(data => {
            contenedorMedicamentos.innerHTML = '';
            // Iterar sobre los medicamentos y agregarlos al formulario
            data.medicamentos.forEach(medicamento => {
                agregarMedicamentoFormulario(medicamento.medicamento, medicamento.indicaciones);
            });
            
        })
        .catch(error => {
            console.error('Error al obtener el detalle de la receta:', error);
            // Aquí puedes manejar el error, por ejemplo, mostrar un mensaje de error al usuario
        });
}

function registrarHospitalizacion(id){
    sectionReceta.style.display='none'
    sectionHospitalizacion.style.display='block'
    mostrarModal()
}

function agregarMedicamentoFormulario(medicamento, indicaciones) {
    contadorMedicamentos++;
    const nuevoMedicamentoDiv = document.createElement('div');
    nuevoMedicamentoDiv.classList.add('row');
    nuevoMedicamentoDiv.innerHTML = `
        <div class="form-group col-4">
            <label for="medicamento${contadorMedicamentos}">Medicamento:</label>
            <input type="text" name="medicamento${contadorMedicamentos}" class="form-control" value="${medicamento || ''}">
        </div>
        <div class="form-group col-8">
            <label for="indicaciones${contadorMedicamentos}">Indicaciones:</label>
            <input type="text" name="indicaciones${contadorMedicamentos}" class="form-control" value="${indicaciones || ''}">
        </div>
    `;
    contenedorMedicamentos.appendChild(nuevoMedicamentoDiv);
}