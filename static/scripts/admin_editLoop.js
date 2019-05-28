$(document).ready(function() {
  
  $.each(loop_playlist, function(index, value) {
    var load_item = $("<tr></tr>").append("<td>" + value.name + "</td><td>" + value.type + "</td><td>" + value.id + "</td>")
    $("#loop_content").append(load_item);
  });

})
