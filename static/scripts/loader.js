$(document).ready(function(){
  function preloader(){
      document.getElementById("loader").style.display = "none";
      document.getElementById("content").style.display = "block";
  }//preloader
  window.onload = preloader;

});
