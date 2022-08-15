$(document).ready(function(){
    $('.backtop').click(function(){
        $('body,html').animate({scrollTop:0},500);
    });

    $('.unit').mouseenter(function(){
        $('.chat-enter').css("display","block");
        $('.unit').css("overflow","visible");
        $('.unit').animate({height:"80px"},100);
    });

    $('.unit').mouseleave(function(){
        $('.chat-enter').css("display","none");
        $('.unit').css("overflow","hidden");
        $('.unit').animate({height:"40px"},100);
    });
});