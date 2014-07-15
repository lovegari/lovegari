$(document).ready(function() {

	$('img').mouseenter(function() {
		$(this).fadeTo('fast',0.25);
	});

  $('img').mouseleave(function() {
    $(this).fadeTo('fast',1);
  });

	$('#m1').mouseenter(function() {
       $('#m2').animate({top:"+=10px"},'fast');
       $('#m3').animate({top:"+=10px"},'fast');
       $('#m4').animate({top:"+=10px"},'fast');
  });

  $('#m1').mouseleave(function() {
       $('#m2').animate({top:"-=10px"},'fast');
       $('#m3').animate({top:"-=10px"},'fast');
       $('#m4').animate({top:"-=10px"},'fast');
  });

  $('#m2').mouseenter(function() {
       $('#m3').animate({top:"+=10px"},'fast');
       $('#m4').animate({top:"+=10px"},'fast');
       $('#m1').animate({top:"+=10px"},'fast');
  });

  $('#m2').mouseleave(function() {
       $('#m3').animate({top:"-=10px"},'fast');
       $('#m4').animate({top:"-=10px"},'fast');
       $('#m1').animate({top:"-=10px"},'fast');
  });

  $('#m3').mouseenter(function() {
       $('#m4').animate({top:"+=10px"},'fast');
       $('#m1').animate({top:"+=10px"},'fast');
       $('#m2').animate({top:"+=10px"},'fast');
  });

  $('#m3').mouseleave(function() {
       $('#m4').animate({top:"-=10px"},'fast');
       $('#m1').animate({top:"-=10px"},'fast');
       $('#m2').animate({top:"-=10px"},'fast');
  });

  $('#m4').mouseenter(function() {
       $('#m1').animate({top:"+=10px"},'fast');
       $('#m2').animate({top:"+=10px"},'fast');
       $('#m3').animate({top:"+=10px"},'fast');
  });

  $('#m4').mouseleave(function() {
       $('#m1').animate({top:"-=10px"},'fast');
       $('#m2').animate({top:"-=10px"},'fast');
       $('#m3').animate({top:"-=10px"},'fast');
  });

});