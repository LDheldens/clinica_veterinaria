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
                    var buttons = '<a href="/pos/crm/diagnostico/update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/pos/crm/diagnostico/delete/' + row.id + '/" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    return buttons;
                }
            },
            {
                targets: [0,1,2,3,4,5,6,7],
                class: 'text-center',
            },
        ],
        initComplete: function (settings, json) {

        }
    });
}

$(function () {
    getData();
});
