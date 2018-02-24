// Document Dot Ready
$(document).ready(function() {

    // Init a Clipboard for .copy-data and preventDefault
    new Clipboard('.copy-data');
    $( ".copy-data" ).click(function( event ) {
        event.preventDefault();
    });

    // Log Out Form Activator Button
    $('#logout-btn').click(function () {
        $('#logout-form').submit();
        return false;
    });

    // Log Out Form Activator Button
    $('#save-btn').click(function () {
        console.log('clicked save button');
        $('#save-form').submit();
        $('#save-modal').modal('hide');
        return false;
    });
    $('#save-modal').on('shown.bs.modal', function () {
        $('#save-name').focus()
    });
    $('#shared-saves').bind('change', function () { // bind change event to select
        var share = $(this).val(); // get selected value
        if (share != '') { // require a URL
            window.location = '/share/' + share; // redirect
        }
        return false;
    });

});
