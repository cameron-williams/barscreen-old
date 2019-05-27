$(document).ready(function() {

  $.each(loop_playlist, function(index, value) {
    var playlist_item = '<li><div><img src="'+value.image_url+'"/></div><div><span>'+value.id+'</span><h4>'+value.name+'</h4><h5>'+value.name+'</h5></div></li>';
    $(".playlist_list ul").append(playlist_item);
  });

})
