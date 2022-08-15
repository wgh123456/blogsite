$(document).ready(function(){
	
	var flag = 1;
	var newWidth = $('body').width() - 78;
	
	$('.con').click(function(){
		if(flag==1)
		{
			$(".admin-sidebar").animate({width:'15%'});
		 	$(".admin-content").animate({width:'85%',left:'15%'});
		 	$('.links_name').show(300);
		 	flag=0;
		}else{
			$(".admin-sidebar").animate({width:'78px'});
		 	$(".admin-content").animate({width:newWidth,left:'78px'});
		 	$('.links_name').hide(300);
		 	flag=1;
		}
//		$('.links_name').toggle();
	});
	
	
	
});