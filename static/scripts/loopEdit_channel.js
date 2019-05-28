$(document).ready(function() {

  $.each(loop_playlist, function(index, value) {
    var playlist_item = '<li><div><img src="'+value.image_url+'"/></div><div><span>'+value.id+'</span><h4>'+value.name+'</h4><h5>'+value.name+'</h5></div></li>';
    $(".playlist_list ul").append(playlist_item);
  });

  $(".content_channel").click(function() {
    $(document).find(".channel").hide()
    $t = $(this)
    var channel_id = $(this).find(".content_id").text();
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

  $('#title_edit2').on('click',function(){
    if($(".title_input input").is(":visible")) {
        $(".title_input input").hide();
        $(".title_input span").text(
            $(".title_input input").val()
        ).show();
        $("#title_edit2").hide();
        $("#title_edit1").show();
    } else {
        $("span").hide();
        $("input").text(
            $("span").val()
        ).show();
        $("button").text("Update");
    }
  });

  $('#title_edit1').on('click',function(){
    if($(".title_input span").is(":visible")){
        $(".title_input span").hide();
        $(".title_input input").text(
            $(".title_input span").val()
        ).show();
        $("#title_edit1").hide();
        $("#title_edit2").show();
    }
  });

  var array = [];
  $('#save_button').on('click',function(){
    $('#playlist').has('li').each(function() {
      var loop_type = $(this).find('h5').map(function(){
        return $(this).text();})
      var loop_id = $(this).find('span').map(function(){
        return $(this).text();});
      for (var i=0; i<loop_id.length && i<loop_type.length; i++)
        array[i] = loop_type[i] + loop_id[i];
    });
    console.log(array);
    var loopname = $(".title_input span").text();
    console.log(loopname);
    if ( loopname.length < 1 || $('#playlist').children().length < 1 ){
        if ( loopname.length < 1){
          alert("Please Give your Loop a Title.");
        }else{
          alert("Please Add Shows and Promos to your Loop.");
        }
      }else{
        $.ajax({
            url: save_url,
            method: "POST",
            data: JSON.stringify({"loop_id": loop_id, "name": loopname, "playlist": array, "user_id": user_id}),
            dataType: "json",
            contentType: "application/json",
            success: function(data){alert("Sumbited " + loopname + " successfully.")},
            error: function(errMsg){alert("Sorry: " + errMsg)},
        });
      }
  });
})


$(document).delegate(".show_item",'click',function(){
  $("show_item").hide();
  if ($(this).find(".show_info").is(':visible'))
    {
      $(this).find(".show_info").hide();
    }else{
      $(this).find(".show_info").show();
    }
});

$(document).delegate(".show_clip",'click',function(e){
  e.stopPropagation();
});

$(document).delegate(".playlist_add",'click',function(e){
  e.stopPropagation();
});

$(document).delegate(".playlist_add",'click',function(){
  $e = $(this)
  var ul = $(".playlist_list ul");
  if ( $(this).find("div.promo_id").length ) {
    var loopItem_id = $(this).find(".promo_id").text();
    var loopItem_type = "Promo";
    var loopItem_img = $(this).find(".content_img img").attr('src');
    var loopItem_name = $(this).find(".content_title span").text();
  } else {
    var loopItem_id = $(this).parent().find(".show_id").text();
    var loopItem_type = "Show";
    var loopItem_img = $(this).parent().find(".clip_container video").attr('poster');
    var loopItem_name = $(this).parent().find(".show_name").text();
  }
  var playlist_item = '<li><div><img src="'+loopItem_img+'"/></div><div><span>'+loopItem_id+'</span><h4>'+loopItem_name+'</h4><h5>'+loopItem_type+'</h5></div></li>';
  ul.append(playlist_item);
});

$(document).on('click','.playlist_list ul li',function(){
  $(this).remove();
});
