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

		// $('.cd-header').animate({
		// top: "0px"
		// }, 1200);

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

	$('.cd-container').on( "click", ".bill-like", function () {
		var cur_item = $(this);
		$.ajax({
				url: "/bill/detail_like",
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

				var $timeline_block = $('.cd-timeline-block');

		//hide timeline blocks which are outside the viewport
		$timeline_block.each(function(){
				if($(this).offset().top > $(window).scrollTop()+$(window).height()*0.75) {
						$(this).find('.cd-timeline-img, .cd-timeline-content').addClass('is-hidden');
				}
		});

		//on scolling, show/animate timeline blocks when enter the viewport
		$(window).on('scroll', function(){
				$timeline_block.each(function(){
						if( $(this).offset().top <= $(window).scrollTop()+$(window).height()*0.75 && $(this).find('.cd-timeline-img').hasClass('is-hidden') ) {
								$(this).find('.cd-timeline-img, .cd-timeline-content').removeClass('is-hidden').addClass('bounce-in');
						}
				});
		});

	var visionTrigger = $('.cd-3d-trigger'),
		galleryItems = $('.no-touch #cd-gallery-items').children('li'),
		galleryNavigation = $('.cd-item-navigation a');

	//on mobile - start/end 3d vision clicking on the 3d-vision-trigger
	visionTrigger.on('click', function(){
		$this = $(this);
		if( $this.parent('li').hasClass('active') ) {
			$this.parent('li').removeClass('active');
			hideNavigation($this.parent('li').find('.cd-item-navigation'));
		} else {
			$this.parent('li').addClass('active');
			updateNavigation($this.parent('li').find('.cd-item-navigation'), $this.parent('li').find('.cd-item-wrapper'));
		}
	});

	//on desktop - update navigation visibility when hovering over the gallery images
	galleryItems.hover(
		//when mouse enters the element, show slider navigation
		function(){
			$this = $(this).children('.cd-item-wrapper');
			updateNavigation($this.siblings('nav').find('.cd-item-navigation').eq(0), $this);
		},
		//when mouse leaves the element, hide slider navigation
		function(){
			$this = $(this).children('.cd-item-wrapper');
			hideNavigation($this.siblings('nav').find('.cd-item-navigation').eq(0));
		}
	);

	//change image in the slider
	galleryNavigation.on('click', function(){
		var navigationAnchor = $(this);
			direction = navigationAnchor.text(),
			activeContainer = navigationAnchor.parents('nav').eq(0).siblings('.cd-item-wrapper');
		
		( direction=="Next") ? showNextSlide(activeContainer) : showPreviousSlide(activeContainer);
		updateNavigation(navigationAnchor.parents('.cd-item-navigation').eq(0), activeContainer);
	});
		
});

function showNextSlide(container) {
	var itemToHide = container.find('.cd-item-front'),
		itemToShow = container.find('.cd-item-middle'),
		itemMiddle = container.find('.cd-item-back'),
		itemToBack = container.find('.cd-item-out').eq(0);

	itemToHide.addClass('move-right').removeClass('cd-item-front').one('webkitTransitionEnd otransitionend oTransitionEnd msTransitionEnd transitionend', function(){
		itemToHide.addClass('hidden');
	});
	itemToShow.addClass('cd-item-front').removeClass('cd-item-middle');
	itemMiddle.addClass('cd-item-middle').removeClass('cd-item-back');
	itemToBack.addClass('cd-item-back').removeClass('cd-item-out');
}

function showPreviousSlide(container) {
	var itemToMiddle = container.find('.cd-item-front'),
		itemToBack = container.find('.cd-item-middle'),
		itemToShow = container.find('.move-right').slice(-1),
		itemToOut = container.find('.cd-item-back');

	itemToShow.removeClass('hidden').addClass('cd-item-front');
	itemToMiddle.removeClass('cd-item-front').addClass('cd-item-middle');
	itemToBack.removeClass('cd-item-middle').addClass('cd-item-back');
	itemToOut.removeClass('cd-item-back').addClass('cd-item-out');

	//wait until itemToShow does'n have the 'hidden' class, then remove the move-right class 
	//in this way, transition works also in the way back
	var stop = setInterval(checkClass, 100);
	
	function checkClass(){
		if( !itemToShow.hasClass('hidden') ) {
			itemToShow.removeClass('move-right');
			window.clearInterval(stop);
		}
	}
}

function updateNavigation(navigation, container) {
	var isNextActive = ( container.find('.cd-item-middle').length > 0 ) ? true : false,
		isPrevActive = 	( container.children('li').eq(0).hasClass('cd-item-front') ) ? false : true;
	(isNextActive) ? navigation.find('a').eq(1).addClass('visible') : navigation.find('a').eq(1).removeClass('visible');
	(isPrevActive) ? navigation.find('a').eq(0).addClass('visible') : navigation.find('a').eq(0).removeClass('visible');
}

function hideNavigation(navigation) {
	navigation.find('a').removeClass('visible');
}