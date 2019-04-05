$(document).ready(function() {
    $.fn.editable.defaults.mode = 'inline';
    $.fn.editable.defaults.showbuttons = false;

    //  Initialize table for current user

    $('#company').editable();
    $('#email').editable();
    $('#first_name').editable();
    $('#last_name').editable();
    $('#phone_number').editable();
    $('#confirmed').editable({
      source: [
              {value: false, text: 'False'},
              {value: true, text: 'True'}
            ]
    });
    $('#ads').editable({
      source: [
              {value: false, text: 'False'},
              {value: true, text: 'True'}
            ]
    });

})
