$(document).ready(function() {
  $(".content_channel").click(function() {
    $(document).find(".channel").hide()
    $t = $(this)
    var channel_id = $(this).find(".content_id").text();
    console.log(channel_id)
    $.ajax({
        url: post_url,
        method: "POST",
        data: JSON.stringify({"channel_id": channel_id}),
        dataType: "json",
        contentType: "application/json",
        success: function(resp){
          $t.parent().parent().parent().parent().after(
            resp.data
          )
        },
        error: function(errMsg){alert("Error find channel: " + errMsg)},
    })
  });
})
