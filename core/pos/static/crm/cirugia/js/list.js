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
            {"data": "cliente.user.first_name"},
            {"data": "medico.full_name"},
            {"data": null},
            {"data": "fecha"},
            {"data": "hora"},
            {"data": null},
        ],
        columnDefs: [
            {
                targets: [4],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    if (row.firma_propietario!=null) {
                        return `
                            <a href="${row.firma_propietario}" class="btn btn-danger btn-sm" target="_blank">
                                <i class="fas fa-file-pdf mr-1"></i> Ver documento
                            </a>
                        `;
                    }else{
                        return `
                            <span class="badge badge-warning">Sin documento</span>
                        `
                    }
                }
                
            },
            {
                targets: [7],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="/pos/crm/cirugia/update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/pos/crm/cirugia/delete/' + row.id + '/" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    return buttons;
                }
            },
        ],
    });
}

$(function () {
    getData();
});
