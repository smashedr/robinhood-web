// Document Dot Ready
$(document).ready(function() {
    var table = $('#stock-table').DataTable( {
        lengthChange: false,
        buttons: [ 'copy', 'excel', 'pdf', 'colvis' ],
        paging: false,
        "order": [[ 5, 'desc' ]],
        "columnDefs": [
            { "orderSequence": [ "asc", "desc" ], "targets": [ 0, 1 ] },
            { "orderSequence": [ "desc", "asc" ], "targets": [ 2, 3, 4, 5 ] },
            { "orderable": true, "targets": [0, 1, 2, 3, 4, 5] }
            // { "type": "html-num-fmt", "targets": [ 2, 3, 4, 5 ] }
        ]
    } );

    table.buttons().container()
        .appendTo( '#stock-table_wrapper .col-md-6:eq(0)' );

    $( "#stock-table_wrapper :button" ).addClass( "btn-sm" );
} );
