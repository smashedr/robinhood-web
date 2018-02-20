// Document Dot Ready
$(document).ready(function() {

    // Init a Clipboard for .copy-data and preventDefault
    new Clipboard('.copy-data');
    $( ".copy-data" ).click(function( event ) {
        event.preventDefault();
    });

    // Log Out Form Activator Button
    $('.log-out').click(function () {
        $('#log-out').submit();
        return false;
    });

});
