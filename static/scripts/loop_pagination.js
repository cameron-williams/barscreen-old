$(document).ready(function() {
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

	var pageCount =  $(".loop_item").length / listSize;

     for(var i = 0 ; i<pageCount;i++){

       $(".pagination").append('<a href="#">'+(i+1)+'</a> ');
     }
        $(".pagination a").first().addClass("active")
    showPage = function(page) {
	    $(".loop_item").hide();
	    $(".loop_item").each(function(n) {
	        if (n >= listSize * (page - 1) && n < listSize * page)
	            $(this).show();
	    });
	}

	showPage(1);

	$(".pagination a").click(function() {
	    $(".pagination a").removeClass("active");
	    $(this).addClass("active");
	    showPage(parseInt($(this).text()))
	});



  console.log(listSize);

})
