$(document).ready(function() {

  image_creator = function(){
      var thumbnails = []
      var canvas = $("#loop_canvas");
      var img = $("#loop_preview");
      var ctx = canvas.get(0).getContext("2d");
      ctx.clearRect(0, 0, 540, 405);
      $('#playlist').find('img').each(function(){
        thumbnails.push($(this).attr("src"));
      });
      if (thumbnails.length >= 4){
          var image1 = new Image();
          var image2 = new Image();
          var image3 = new Image();
          var image4 = new Image();
          image1.crossOrigin = "";
          image2.crossOrigin = "";
          image3.crossOrigin = "";
          image4.crossOrigin = "";
          image1.src = thumbnails[0]
          image2.src = thumbnails[1]
          image3.src = thumbnails[2]
          image4.src = thumbnails[3]
          image1.onload = function() {
          ctx.drawImage(image1, 0, 0, 270, 205.5);
          img.attr("src", canvas[0].toDataURL("image/png"));
          }
          image2.onload = function() {
          ctx.drawImage(image2, 270, 0, 270, 205.5);
          img.attr("src", canvas[0].toDataURL("image/png"));
          }
          image3.onload = function() {
          ctx.drawImage(image3, 0, 205.5, 270, 205.5);
          img.attr("src", canvas[0].toDataURL("image/png"));
          }
          image4.onload = function() {
          ctx.drawImage(image4, 270, 205.5, 270, 205.5);
          img.attr("src", canvas[0].toDataURL("image/png"));
          }
      }
      if (thumbnails.length == 3){
          var image1 = new Image();
          var image2 = new Image();
          var image3 = new Image();
          image1.crossOrigin = "";
          image2.crossOrigin = "";
          image3.crossOrigin = "";
          image1.src = thumbnails[0]
          image2.src = thumbnails[1]
          image3.src = thumbnails[2]
          ctx.fillStyle = "#232323";
          ctx.fillRect(0, 0, 540, 405);
          image1.onload = function() {
          ctx.drawImage(image1, 0, 0, 270, 205.5);
          img.attr("src", canvas[0].toDataURL("image/png"));
          }
          image2.onload = function() {
          ctx.drawImage(image2, 270, 0, 270, 205.5);
          img.attr("src", canvas[0].toDataURL("image/png"));
          }
          image3.onload = function() {
          ctx.drawImage(image3, 135, 205.5, 270, 205.5);
          img.attr("src", canvas[0].toDataURL("image/png"));
          }
      }
      if (thumbnails.length == 2){
          var image1 = new Image();
          var image2 = new Image();
          image1.crossOrigin = "";
          image2.crossOrigin = "";
          image1.src = thumbnails[0]
          image2.src = thumbnails[1]
          ctx.fillStyle = "#232323";
          ctx.fillRect(0, 0, 540, 405);
          image1.onload = function() {
          ctx.drawImage(image1, 0, 0, 270, 205.5);
          img.attr("src", canvas[0].toDataURL("image/png"));
          }
          image2.onload = function() {
          ctx.drawImage(image2, 270, 205.5, 270, 205.5);
          img.attr("src", canvas[0].toDataURL("image/png"));
          }
      }v
      ivails.length == 1){
       vage1 = new Image();
       v.crossOrigin = "";
          image1.src = thumbnails[0]
          image1.onload = function() {
            ctx.drawImage(image1, 0, 0, 540, 405);
            img.attr("src", canvas[0].toDataURL("image/png"));
          }
        }
    };

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

  $('body').click(function (event)
  {
    $('.modal').removeClass('is-visible');
  });

  $('#promo_cancel').click(function(event)
  {
    $(document).find('.modal').removeClass('is-visible');
    $(document).find('#promo_file').val('');
    $(document).find('#name').val('');
    $(document).find('#description').val('');
  });

  $("#add_promo").click(function(e) {
    e.preventDefault();
    e.stopPropagation();
    $('.modal').toggleClass('is-visible');
  });

  $(".modal-wrapper").click(function(e) {
    e.stopPropagation();
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
    var image_url = $("#loop_preview").attr("src");
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
            data: JSON.stringify({"name": loopname, "playlist": array, "image_data": image_url, "user_id": user_id}),
            dataType: "json",
            contentType: "application/json",
            headers: {
                       "Access-Control-Allow-Origin": "*",
                       "Access-Control-Allow-Methods": "*",
                       "Access-Control-Allow-Headers": "*"
                    },
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
  image_creator();
});

$(document).on('click','.playlist_list ul li',function(){
  $(this).remove();
  image_creator();
});

/* Promo Video Preview */

$(function() {
    var video = $(".promo_video");
    var thumbnail = $("#promo_canvas");
    var input = $("#promo_file");
    var ctx = thumbnail.get(0).getContext("2d");
    var duration = 0;
    var img = $("#promo_preview");

    input.on("change", function(e) {
        $(document).find('.promo_img').removeClass('after_overlay');
        var file = e.target.files[0];
        // Validate video file type
        if (["video/mp4"].indexOf(file.type) === -1) {
            alert("Only 'MP4' video format allowed.");
            return;
        }
        // Set video source
        video.find("source").attr("src", URL.createObjectURL(file));
        // Load the video
        video.get(0).load();
        // Load metadata of the video to get video duration and dimensions
        video.on("loadedmetadata", function(e) {
            duration = video.get(0).duration;
            // Set canvas dimensions same as video dimensions
            thumbnail[0].width = 512;
            thumbnail[0].height = 288;
            // Set video current time to get some random image
            video[0].currentTime = 5;
            // Draw the base-64 encoded image data when the time updates
            video.one("timeupdate", function() {
                ctx.drawImage(video[0], 0, 0, 512, 288);
                img.attr("src", thumbnail[0].toDataURL());
            });
        });
    });
});
