function getData() {
    $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: pathname,
            type: 'POST',
            headers: {
                'X-CSRFToken': csrftoken
            },
            data: {
                'action': 'search'
            },
            dataSrc: ""
        },
        columns: [
            {"data": "id"},
            {"data": "paciente.nombre"},
            {"data": "fecha_diagnostico"},
            {"data": "medico.full_name"},
            {"data": "sintomas"},
            {"data": "examenes_fisicos"},
            {"data": "observacion_veterinario"},
            {"data": "diagnostico_provicional"},
            {"data": null},
        ],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return `
                        <div class="dropdown">
                            <button class="btn-list-actas dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Acciones</button>
                            <div 
                                class="dropdown-menu" aria-labelledby="dropdownMenuButton"
                            >
                                <a 
                                    class="dropdown-item" 
                                    href="/pos/crm/diagnostico/update/${row.id}/"
                                >
                                    <i class="fas fa-edit text-warning"></i> Editar
                                </a>

                                <a class="dropdown-item" href="/pos/crm/diagnostico/delete/${row.id}/"><i class="fas fa-trash-alt text-danger"></i> Eliminar</a>

                                <button 
                                    type="button" 
                                    class="dropdown-item" 
                                    data-id="${row.id}" onclick="registrarHospitalizacion(${row.id})"
                                >
                                    <i class="fas fa-hospital"></i> Hospitalización
                                </button>

                                <button 
                                    type="button" 
                                    class="dropdown-item" 
                                    data-id="${row.id}" 
                                    onclick="agregarReceta(${row.paciente.id})"
                                >
                                    <i class="fas fa-prescription"></i> Generar Receta
                                </button>

                                <button 
                                    type="button" 
                                    class="dropdown-item" 
                                    data-id="${row.id}" 
                                    onclick="agregarCirugia(${row.paciente.id},${row.cliente.id},${row.medico.id})"
                                >
                                    <i class="fas fa-syringe"></i> Registrar Cirugia
                                </button>
                            </div>
                        </div>
                    `;
                }
            },
            {
                targets: [0,1,2,3,4,5,6,7],
                class: 'text-center',
            },
        ],
        order: [], 
        initComplete: function (settings, json) {

        }
    });
}

$(function () {
    getData();
});
