$(document).ready(function(){
  $(".forgot_password").click(function() {
    $(document).find(".main").fadeOut(250)
    $(document).find(".alternate").delay(250).fadeIn(250)
  });
  $("#reset_submit").click(function() {
    $(document).find(".alternate").fadeOut(250)
    var email = $(document).find('#reset_email').val();
    $.ajax({
        url: password_url,
        method: "POST",
        data: JSON.stringify({"email": email}),
        dataType: "json",
        contentType: "application/json",
        error: function(errMsg){alert("Sorry email doesn't exist")},
    });
    $(document).find(".alternate2").delay(250).fadeIn(250)
  });
  $("#return_submit").click(function() {
    $(document).find(".alternate2").fadeOut(250)
    $(document).find(".main").delay(250).fadeIn(250)
  });
});
