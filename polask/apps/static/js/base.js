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

//if you change this breakpoint in the style.css file (or _layout.scss if you use SASS), don't forget to update this value as well
    var MQL = 1170;

    //primary navigation slide-in effect
    if($(window).width() > MQL) {
        var headerHeight = $('.cd-header').height();
        $(window).on('scroll',
        {
            previousTop: 0
        }, 
        function () {
            var currentTop = $(window).scrollTop();
            //check if user is scrolling up
            if (currentTop < this.previousTop ) {
                //if scrolling up...
                if (currentTop > 0 && $('.cd-header').hasClass('is-fixed')) {
                    $('.cd-header').addClass('is-visible');
                } else {
                    $('.cd-header').removeClass('is-visible is-fixed');
                }
            } else {
                //if scrolling down...
                $('.cd-header').removeClass('is-visible');
                if( currentTop > headerHeight && !$('.cd-header').hasClass('is-fixed')) $('.cd-header').addClass('is-fixed');
            }
            this.previousTop = currentTop;
        });
    }

    //open/close primary navigation
    $('.cd-primary-nav-trigger').on('click', function(){
        $('.cd-menu-icon').toggleClass('is-clicked'); 
        $('.cd-header').toggleClass('menu-is-open');
        
        //in firefox transitions break when parent overflow is changed, so we need to wait for the end of the trasition to give the body an overflow hidden
        if( $('.cd-primary-nav').hasClass('is-visible') ) {
            $('.cd-primary-nav').removeClass('is-visible').one('webkitTransitionEnd otransitionend oTransitionEnd msTransitionEnd transitionend',function(){
                $('body').removeClass('overflow-hidden');
            });
        } else {
            $('.cd-primary-nav').addClass('is-visible').one('webkitTransitionEnd otransitionend oTransitionEnd msTransitionEnd transitionend',function(){
                $('body').addClass('overflow-hidden');
            }); 
        }
    });
    
});