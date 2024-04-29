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
            {"data": "propietario"},
            {"data": "nombre"},
            {"data": null},
            {"data": "edad"},
            {"data": "tipo_mascota"},
            {"data": "sexo"},
            {"data": null},
            {"data": "id"},
        ],
        columnDefs: [
            {
                targets: [0],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row, meta) {
                    return meta.row + 1;
                }
            },
            {
                targets: [1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row, meta) {
                    return data
                }
            },
            {
                targets: [3],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var imagen = `
                        <img src="${row.imagen}" width="80" height="80" style="object-fit: cover;">
                    `
                    return imagen
                }
            },
            {
                targets: [1,2,3,4],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return data
                }
            },
            {
                targets: [7],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return row.peso + ' KG'
                }
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a target="_blank" href="/pos/crm/historial/print/' + row.paciente_id + '/" class="btn btn-primary btn-xs btn-flat"><i class="fas fa-print"></i></a> ';
                    return buttons
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