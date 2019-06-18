$(document).ready(function(){

//get height of right div

var eRightHt = $(".section_splash").outerHeight();
var eRighttrue = eRightHt + 160
// apply height to image in leftdiv

$(".splash").css("height",eRighttrue);

$(".hamburger").click(function(){
    $(".nav_menu").toggle();
  });

var $hamburger = $(".hamburger");
  $hamburger.on("click", function(e) {
    $hamburger.toggleClass("is-active");
    // Do something else, like open/close menu
  });

  $('.flash_message').delay(500).fadeIn('normal', function() {
        $(this).delay(2500).fadeOut();
     });
});
