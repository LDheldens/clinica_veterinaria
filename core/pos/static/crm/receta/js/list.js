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
            { data: 'id', width:'5%'},  // Columnas que corresponden a los campos de tu modelo Receta
            { data: 'mascota', width:'20%' },
            { data: null },  // Accede al primer medicamento de la lista de medicamentos
            { data: null},  
        ],
        columnDefs: [
            {
                targets: [2], // Índice de la columna de medicamentos
                class: 'text-left',
                orderable: false,
                render: function (data, type, row, meta) {
                    let medicamentosHtml = "";
                    row.medicamentos.forEach(function (medicamento) {
                        medicamentosHtml += `<b>${medicamento.medicamento}</b>: ${medicamento.indicaciones}<br>`;
                    });
                    return medicamentosHtml;
                }
            },            
            {
                targets: [1,2],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return data
                }
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return `
                        <a href="/pos/crm/receta/print/${row.id}/" target="_blank" class="btn btn-primary btn-xs btn-flat"><i class="fas fa-print"></i></a> 
                        <a class="btn btn-warning btn-xs btn-flat" data-id="${row.id}" onclick="editarReceta(${row.id})"><i class="fas fa-edit"></i></a>
                        <a href="/pos/crm/receta/delete/${row.id}/" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>
                    `;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });
}

$(function () {
    getData();
});

function actualizarDataTable() {
    // Destruir la tabla actual
    $('#data').DataTable().destroy();

    // Volver a cargar los datos actualizados
    getData();
}