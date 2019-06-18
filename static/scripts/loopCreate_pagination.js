$(document).ready(function() {

  var lists = document.getElementsByClassName('content_display');
  listSize = 5;
  var fourWide = window.matchMedia("(max-width: 850px)");
  var threeWide = window.matchMedia("(max-width: 600px)")
  if (fourWide.matches){
      // Screen is less than 800px
      listSize = 4;
  }
  if (threeWide.matches){
      // Screen is less than 600px
      listSize = 3;
  }
  console.log(listSize);

  $(lists).each(function() {
    var contentCount = $(this).find('ul li').length
    var listPresent = $(this).find('ul').has("li").length ? "Yes" : "No"
    var pageCount =  contentCount / listSize;
    if (contentCount < listSize)
      $(this).find(".content_more").hide()
    if (listPresent == "No")
      $(this).parent(".content_row").hide()
    var $e = $(this)
    var $f =  $(this).find('.content_item')
       for(var i = 0 ; i<pageCount;i++){

         $(this).find(".pagination").append('<a href="#"><span>'+(i+1)+'</span></a> ');
       }
        $(this).find(".pagination a").first().addClass("active")
    var showPage = function(page) {
    	    $f.hide();
    	    $f.each(function(n) {
    	        if (n >= listSize * (page - 1) && n < listSize * page)
    	            $(this).show();
          });
  	}

    showPage(1);

  	$(this).find(".pagination a").click(function() {
  	    $e.find(".pagination a").removeClass("active");
        $(this).addClass("active");
        showPage(parseInt($(this).text()))
  	});

    $(this).find(".content_more").click(function() {
  	    var reference = $e.find(".pagination a.active")
        var oneOver = $e.find(".pagination a.active").next()
        if ( oneOver.length == 0){
          oneOver = $e.find(".pagination a").first();
        }

        $e.find(".pagination a").removeClass("active");
        $(oneOver).addClass("active");
        showPage(parseInt($(oneOver).text()))
  	});
  });

  if($('.content_row .addpromo').css('display') != 'none')
  {
    $(".first_promo").hide();
  }
  
})
