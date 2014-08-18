$(document).ready(function () {

	$(function(){
		jQuery('#maximage').maximage();
	});

	$('.llArticleCreate #article_create_content').summernote();

	$('.llArticleCreate').submit(function () {
		setTimeout(function () {
			$('#article_create_content').val($('.llArticleCreate #article_create_content').code());
		}, 50);
	});

    $('.navbar-default').animate({
    top: "0px"
    }, 1200);
});