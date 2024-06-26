function getData() {
    $('#data').DataTable({
        responsive: true,
        dom: 'Bfrtilp',
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
            {"data": "raza"},
            {"data": "nombre"},
            {"data": "edad"},
            {"data": "tipo_mascota"},
            {"data": "sexo"},
            {"data": "peso"},
        ],
        // columnDefs:[
        //     {
        //         targets: [0,1,2,3,4,5,6,7],
        //         class: 'text-center',
        //         orderable: false,
        //         render: function (data, type, row) {
        //             return data
        //         }
        //     },

        // ],
        buttons: [
            {
                extend: 'excelHtml5',
                text: 'Descargar Excel <i class="fas fa-file-excel"></i>',
                titleAttr: 'Excel',
                className: 'btn btn-success btn-flat btn-xs'
            },
            {
                extend: 'pdfHtml5',
                text: 'Descargar Pdf <i class="fas fa-file-pdf"></i>',
                titleAttr: 'PDF',
                className: 'btn btn-danger btn-flat btn-xs',
                download: 'open',
                orientation: 'landscape',
                pageSize: 'LEGAL',
                customize: function (doc) {
                    var currentDate = new Date().toLocaleDateString();
                    var widths = [];
                    $('#data').DataTable().columns().header().each(function() {
                        widths.push($(this).width());
                    });

                    doc.content[1].table.widths = widths;
                    doc.content[1].margin = [100, 0, 100, 20]; // Ajusta el margen izquierdo y derecho
                    doc.content[1].layout = {
                        hLineWidth: function (i, node) {
                            return (i === 0 || i === node.table.body.length) ? 0 : 1;
                        },
                        vLineWidth: function (i, node) {
                            return 0;
                        },
                        hLineColor: function (i, node) {
                            return 'white';
                        }
                    };
                    doc['footer'] = function (page, pages) {
                        return {
                            columns: [
                                {
                                    alignment: 'left',
                                    text: ['Fecha de creación: ', {text: currentDate}]
                                },
                                {
                                    alignment: 'right',
                                    text: ['Página ', {text: page.toString()}, ' de ', {text: pages.toString()}]
                                }
                            ],
                            margin: 20
                        };
                    };
                }
            }
        ]
    });
}

$(function () {
    getData();
});
