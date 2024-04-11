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
            {"data": "mascota.nombre"},
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
                orderable: true,
                render: function (data, type, row) {
                    if (row.estado === false) {
                        return '<button class="btn btn-warning btn-xs btn-flat btn-change-status" onclick="cambiarEstado(' + row.id + ')">Pendiente</button>';
                    } else {
                        return '<button class="btn btn-success btn-xs btn-flat btn-change-status" onclick="cambiarEstado(' + row.id + ')">Atendido</button>';
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
    });
}

$(function () {
    getData();
});

function cambiarEstado(citaId) {
    console.log(citaId);
    fetch('/pos/crm/cita/cambiar_estado/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            cita_id: citaId,
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error al cambiar el estado de la cita');
        }
        console.log('Estado cambiado con éxito.');
        // Actualizar la tabla de datos si es necesario
        $('#data').DataTable().ajax.reload();
    })
    .catch(error => {
        console.error('Error:', error);
    });
}