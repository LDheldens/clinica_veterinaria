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
            {"data": "paciente"},
            {"data": "fecha_ingreso"},
            {"data": "medicinas_aplicadas"},
            {"data": "dias_internados"},
            {"data": "internado"},
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
                targets: [0,1,2,3,4],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return data
                }
            },
            {
                targets: [5],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    console.log({
                        data
                    })
                    if (data) {
                        return '<span class="badge bg-warning text-dark">Internado</span>'
                    }
                    return '<span class="badge bg-success">Dado de alta</span>'
                }
            },
            {
                targets: [6],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="/pos/crm/hospitalizacion/update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/pos/crm/hospitalizacion/delete/' + row.id + '/" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a> ';
                    if(row.internado) {
                        buttons += '<a href="/pos/crm/hospitalizacion/update_internamiento/' + row.id + '/" class="btn btn-success btn-xs btn-flat"> <span class="text-white">Dar de alta</span> <i class="fas fa-check"></i></a>';
                    } else {
                        buttons += '<a href="/pos/crm/hospitalizacion/update_internamiento/' + row.id + '/" class="btn btn-danger btn-xs btn-flat"> <span class="text-white">Dar de baja</span> <i class="fas fa-check"></i></a>';
                    }
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