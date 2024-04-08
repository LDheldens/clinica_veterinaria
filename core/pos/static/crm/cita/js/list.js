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
            {"data": "medico.nombre"},
            {"data": "propietario.nombre"},
            {"data": "mascota"},
            {"data": "fecha_cita"},
            {"data": "hora_cita"},
            {"data": null},
            {"data": null},
        ],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false
            },
            {
                targets: [6], // Índice de la columna del estado en los datos
                class: 'text-center',
                orderable: true, // Opcional, para permitir o no que la columna sea ordenable
                render: function (data, type, row) {
                    if (row.estado === false) {
                        return '<span class="badge badge-warning">Pendiente</span>';
                    } else {
                        return '<span class="badge badge-success">Confirmado</span>';
                    }
                }
            },
            {
                targets: [7],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="/pos/crm/cita/update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/pos/crm/cita/delete/' + row.id + '/" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    return buttons;
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
