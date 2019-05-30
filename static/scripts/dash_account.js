$(document).ready(function(){
  $('#phone').mask('(000) 000-0000');

  $('.account_menu ul li').click(function() {
    $('.account_menu ul').find('li').removeClass('acc_menu_active');
    $(this).addClass("acc_menu_active");
    var modal_id = $(this).text();
    console.log(modal_id);
    $('.account_content').children().fadeOut(250);
    $('.account_content').find("div[id*='" + modal_id + "']").delay(250).fadeIn(250);
  });
});
