// Document Dot Ready
$(document).ready(function() {

    // Init a Clipboard for .copy-data and preventDefault
    new Clipboard('.copy-data');
    $( ".copy-data" ).click(function( event ) {
        event.preventDefault();
    });

});
