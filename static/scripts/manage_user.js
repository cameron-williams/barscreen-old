$(document).ready(function() {
    $.fn.editable.defaults.mode = 'inline';
    $.fn.editable.defaults.showbuttons = false;

    //  Initialize table for current user
    $('#user_details').DataTable({
        searching: false,
        paging: false,
        info: false,
        filter: false,
    });

    $('#company').editable();
    $('#email').editable();
    $('#first_name').editable();
    $('#last_name').editable();
    $('#phone_number').editable();
    $('#confirmed').editable();
    $('#ads').editable();

})