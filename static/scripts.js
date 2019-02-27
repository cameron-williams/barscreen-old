$(document).ready(function(){

//get height of right div

var eRightHt = $(".section_splash").outerHeight();
var eRighttrue = eRightHt + 160
// apply height to image in leftdiv

$(".splash").css("height",eRighttrue);

var $hamburger = $(".hamburger");
  $hamburger.on("click", function(e) {
    $hamburger.toggleClass("is-active");
    // Do something else, like open/close menu
  });

});
