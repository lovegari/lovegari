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

    $('.llArticleDetail').on( "click", ".btn-warning", function () {
        var cur_item = $(this);
        $.ajax({
            url: "/article/detail_like",
            dataType:'JSON',
            data: {
                id : cur_item.children().last().val()
            },
            success: function() {
                var cur_value = cur_item.children().last().prev().text();
                cur_item.children().last().prev().text(parseInt(cur_value) + 1);
            },
            error: function(request,status,error){
                alert("code:"+request.status+"\n"+"error:"+error);
            }
        });
    });

        $('.llCommentList').on( "click", ".well .btn-warning", function () {
        var cur_item = $(this);
        $.ajax({
            url: "/comment/detail_like",
            dataType:'JSON',
            data: {
                id : cur_item.children().last().val()
            },
            success: function() {
                var cur_value = cur_item.children().last().prev().text();
                cur_item.children().last().prev().text(parseInt(cur_value) + 1);
            },
            error: function(request,status,error){
                alert("code:"+request.status+"\n"+"error:"+error);
            }
        });
    });
    
});