let contenedorModal;
let modal;
let formReceta;
let recetaId;
let btnAgregarMedicamento; 
let contenedorMedicamentos; 
let sectionReceta;
let contadorMedicamentos = 0;

document.addEventListener('DOMContentLoaded',()=>{
    btnAgregarMedicamento = document.getElementById('btn-agregar-medicamento');
    contenedorMedicamentos = document.getElementById('contenedor-medicamentos');
    formReceta = document.querySelector('#formReceta')
    divReceta = document.querySelector('.receta')
    sectionReceta = document.querySelector('.sectionReceta')

    btnAgregarMedicamento.addEventListener('click', (e)=>{
        e.preventDefault()
        agregarMedicamentoFormulario()
    });
    formReceta.addEventListener('submit', enviarFormulario)
   
})

function enviarFormulario(e){
    e.preventDefault(); // Evita que el formulario se envíe normalmente
    document.querySelector('.titulo-receta').textContent='Edición de Receta'
    // Crea un nuevo objeto FormData
    const formData = new FormData(formReceta);

    const primerMedicamento = formData.get('medicamento1');
    const primerIndicaciones = formData.get('indicaciones1');

    if (!primerMedicamento || !primerIndicaciones) {
        Toastify({
            text: "Por favor, Ingrese al menos un medicamento",
            duration: 3000, 
            gravity: "top-center", 
            backgroundColor: "linear-gradient(to right, #ff0000, #ff3333)", // 
            close: true, 
            stopOnFocus: true, 
            className: "toastify-error",
            icon: "error" 
        }).showToast();
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
    };
    
    // Enviar los datos mediante fetch
    fetch(`/pos/crm/receta/add/`, {
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
                text: "Receta Registrada de manera exitosa",
                duration: 3000, // Duración en milisegundos
                gravity: "top", // Posición de la notificación: "top", "bottom", "center"
                backgroundColor: "linear-gradient(to right, #00b09b, #96c93d)", // Color de fondo
            }).showToast();
            actualizarDataTable()
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