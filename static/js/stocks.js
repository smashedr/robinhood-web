// Document Dot Ready
$(document).ready(function() {
    var table = $('#stock-table').DataTable( {
        lengthChange: false,
        buttons: [ 'copy', 'excel', 'pdf', 'colvis' ],
        paging: false,
        "order": [[ 7, 'desc' ]],
        "columnDefs": [
            { "orderSequence": [ "asc", "desc" ], "targets": [ 0, 1 ] },
            { "orderSequence": [ "desc", "asc" ], "targets": [ 2, 3, 4, 5, 6, 7, 8, 9 ] },
            { "orderable": true, "targets": [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 ] },
            { "visible": false, "targets": [ 1, 4 ] }
            // { "type": "html-num-fmt", "targets": [ 2, 3, 4, 5 ] }
        ]
    } );

    table.buttons().container()
        .appendTo( '#stock-table_wrapper .col-md-6:eq(0)' );

    $( "#stock-table_wrapper :button" ).addClass( "btn-sm" );
} );
