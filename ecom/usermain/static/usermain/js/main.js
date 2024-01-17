
(function ($) {
    "use strict";

    $(".animsition").animsition({
        inClass: 'fade-in',
        outClass: 'fade-out',
        inDuration: 1500,
        outDuration: 800,
        linkElement: '.animsition-link',
        loading: true,
        loadingParentElement: 'html',
        loadingClass: 'animsition-loading-1',
        loadingInner: '<div class="loader05"></div>',
        timeout: false,
        timeoutCountdown: 5000,
        onLoadEvent: true,
        browser: [ 'animation-duration', '-webkit-animation-duration'],
        overlay : false,
        overlayClass : 'animsition-overlay-slide',
        overlayParentElement : 'html',
        transition: function(url){ window.location.href = url; }
    });
    
    var windowH = $(window).height()/2;

    $(window).on('scroll',function(){
        if ($(this).scrollTop() > windowH) {
            $("#myBtn").css('display','flex');
        } else {
            $("#myBtn").css('display','none');
        }
    });

    $('#myBtn').on("click", function(){
        $('html, body').animate({scrollTop: 0}, 300);
    });


    var headerDesktop = $('.container-menu-desktop');
    var wrapMenu = $('.wrap-menu-desktop');

    if($('.top-bar').length > 0) {
        var posWrapHeader = $('.top-bar').height();
    }
    else {
        var posWrapHeader = 0;
    }
    

    if($(window).scrollTop() > posWrapHeader) {
        $(headerDesktop).addClass('fix-menu-desktop');
        $(wrapMenu).css('top',0); 
    }  
    else {
        $(headerDesktop).removeClass('fix-menu-desktop');
        $(wrapMenu).css('top',posWrapHeader - $(this).scrollTop()); 
    }

    $(window).on('scroll',function(){
        if($(this).scrollTop() > posWrapHeader) {
            $(headerDesktop).addClass('fix-menu-desktop');
            $(wrapMenu).css('top',0); 
        }  
        else {
            $(headerDesktop).removeClass('fix-menu-desktop');
            $(wrapMenu).css('top',posWrapHeader - $(this).scrollTop()); 
        } 
    });


    $('.btn-show-menu-mobile').on('click', function(){
        $(this).toggleClass('is-active');
        $('.menu-mobile').slideToggle();
    });

    var arrowMainMenu = $('.arrow-main-menu-m');

    for(var i=0; i<arrowMainMenu.length; i++){
        $(arrowMainMenu[i]).on('click', function(){
            $(this).parent().find('.sub-menu-m').slideToggle();
            $(this).toggleClass('turn-arrow-main-menu-m');
        })
    }

    $(window).resize(function(){
        if($(window).width() >= 992){
            if($('.menu-mobile').css('display') == 'block') {
                $('.menu-mobile').css('display','none');
                $('.btn-show-menu-mobile').toggleClass('is-active');
            }

            $('.sub-menu-m').each(function(){
                if($(this).css('display') == 'block') { console.log('hello');
                    $(this).css('display','none');
                    $(arrowMainMenu).removeClass('turn-arrow-main-menu-m');
                }
            });
                
        }
    });


    $('.js-show-modal-search').on('click', function(){
        $('.modal-search-header').addClass('show-modal-search');
        $(this).css('opacity','0');
    });

    $('.js-hide-modal-search').on('click', function(){
        $('.modal-search-header').removeClass('show-modal-search');
        $('.js-show-modal-search').css('opacity','1');
    });

    $('.container-search-header').on('click', function(e){
        e.stopPropagation();
    });


     
    var $topeContainer = $('.isotope-grid');
    var $filter = $('.filter-tope-group');

    $filter.each(function () {
        $filter.on('click', 'button', function () {
            var filterValue = $(this).attr('data-filter');
            $topeContainer.isotope({filter: filterValue});
        });
        
    });

    $(window).on('load', function () {
        var $grid = $topeContainer.each(function () {
            $(this).isotope({
                itemSelector: '.isotope-item',
                layoutMode: 'fitRows',
                percentPosition: true,
                animationEngine : 'best-available',
                masonry: {
                    columnWidth: '.isotope-item'
                }
            });
        });
    });

    var isotopeButton = $('.filter-tope-group button');

    $(isotopeButton).each(function(){
        $(this).on('click', function(){
            for(var i=0; i<isotopeButton.length; i++) {
                $(isotopeButton[i]).removeClass('how-active1');
            }

            $(this).addClass('how-active1');
        });
    });

    $('.js-show-filter').on('click',function(){
        $(this).toggleClass('show-filter');
        $('.panel-filter').slideToggle(400);

        if($('.js-show-search').hasClass('show-search')) {
            $('.js-show-search').removeClass('show-search');
            $('.panel-search').slideUp(400);
        }    
    });

    $('.js-show-search').on('click',function(){
        $(this).toggleClass('show-search');
        $('.panel-search').slideToggle(400);

        if($('.js-show-filter').hasClass('show-filter')) {
            $('.js-show-filter').removeClass('show-filter');
            $('.panel-filter').slideUp(400);
        }    
    });




    $('.js-show-cart').on('click',function(){
        $('.js-panel-cart').addClass('show-header-cart');
    });

    $('.js-hide-cart').on('click',function(){
        $('.js-panel-cart').removeClass('show-header-cart');
    });

    $('.js-show-sidebar').on('click',function(){
        $('.js-sidebar').addClass('show-sidebar');
    });

    $('.js-hide-sidebar').on('click',function(){
        $('.js-sidebar').removeClass('show-sidebar');
    });

    $('.btn-num-product-down').on('click', function() {
        var numProduct = parseInt($(this).next().val(), 10);
        if (numProduct > 1) {
            $(this).next().val(numProduct - 1);
            document.getElementById('i').value = numProduct - 1;
        }
    });

    $('.btn-num-product-up').on('click', function() {
        var numProduct = parseInt($(this).prev().val(), 10);
        $(this).prev().val(numProduct + 1);
        document.getElementById('i').value = numProduct + 1;
    });
    
    $('.wrap-rating').each(function(){
        var item = $(this).find('.item-rating');
        var rated = -1;
        var input = $(this).find('input');
        $(input).val(0);

        $(item).on('mouseenter', function(){
            var index = item.index(this);
            var i = 0;
            for(i=0; i<=index; i++) {
                $(item[i]).removeClass('zmdi-star-outline');
                $(item[i]).addClass('zmdi-star');
            }

            for(var j=i; j<item.length; j++) {
                $(item[j]).addClass('zmdi-star-outline');
                $(item[j]).removeClass('zmdi-star');
            }
        });

        $(item).on('click', function(){
            var index = item.index(this);
            rated = index;
            $(input).val(index+1);
        });

        $(this).on('mouseleave', function(){
            var i = 0;
            for(i=0; i<=rated; i++) {
                $(item[i]).removeClass('zmdi-star-outline');
                $(item[i]).addClass('zmdi-star');
            }

            for(var j=i; j<item.length; j++) {
                $(item[j]).addClass('zmdi-star-outline');
                $(item[j]).removeClass('zmdi-star');
            }
        });
    });
    
  
   $('.js-show-modal1').on('click', function (e) {
    e.preventDefault();

    var productName = $(this).data('product-name');
    var productPrice = $(this).data('product-price');
    var productDes = $(this).data('product-des');
    var productImages = $(this).data('product-images').split(',');
    
    $('#quick-view-name').text(productName);
    $('#quick-view-price').text(productPrice);
    $('#quick-view-des').text(productDes);
    $('#product_id').val(productName);

    $('#modal-image-gallery').empty();

    for (var i = 0; i < productImages.length; i++) {
        if (i == 1) {
            $('#modal-image-gallery').append(`
                <div class="item-slick3" data-thumb="${productImages[i]}">
                    <div class="wrap-pic-w pos-relative">
                        <img src="${productImages[i]}" alt="IMG-PRODUCT">
                        <a class="flex-c-m size-108 how-pos1 bor0 fs-16 cl10 bg0 hov-btn3 trans-04" href="${productImages[i]}">
                            <i class="fa fa-expand"></i>
                        </a>
                    </div>
                </div>
            `);
        } else {
            $('#modal-image-gallery').append(`
                <div class="item-slick3" style="display: none;" data-thumb="${productImages[i]}">
                    <div class="wrap-pic-w pos-relative">
                        <img src="${productImages[i]}" alt="IMG-PRODUCT">
                        <a class="flex-c-m size-108 how-pos1 bor0 fs-16 cl10 bg0 hov-btn3 trans-04" href="${productImages[i]}">
                            <i class="fa fa-expand"></i>
                        </a>
                    </div>
                </div>
            `);
        }
    }
    $('#quick-view-modal').addClass('show-modal1');
});

$('.js-hide-modal1').on('click', function () {
    $('#quick-view-modal').removeClass('show-modal1');
});






})(jQuery);


const container = document.getElementById('brandContainer');
const scrollAmount = 300; 
	
			function scrollBrandImages(direction) {
				if (direction === 'prev') {
					container.scrollLeft -= scrollAmount;
				} else if (direction === 'next') {
					container.scrollLeft += scrollAmount;
				}
			}

 
const categoryContainer = document.getElementById('categoryContainer');
const categoryScrollAmount = 300; 

function scrollCategory(direction) {
if (direction === 'prev') {
    categoryContainer.scrollLeft -= categoryScrollAmount;
} else if (direction === 'next') {
    categoryContainer.scrollLeft += categoryScrollAmount;
}
}



function setupImageZoom(imgElement) {
    let imgContainer = imgElement.parentElement;
    let lens = imgContainer.querySelector('.lens');
    let ratio = 3;

    lens.style.backgroundImage = `url(${imgElement.src})`;
    lens.style.backgroundSize = (imgElement.width * ratio) + 'px ' + (imgElement.height * ratio) + 'px';

    imgElement.addEventListener('mousemove', moveLens);
    imgElement.addEventListener('touchmove', moveLens);

    function moveLens(event) {
        let pos = getCursorPos(event);
        let positionLeft = pos.x - (lens.offsetWidth / 2);
        let positionTop = pos.y - (lens.offsetHeight / 2);

        if (positionLeft < 0) {
            positionLeft = 0;
        }

        if (positionTop < 0) {
            positionTop = 0;
        }

        if (positionLeft > imgElement.width - lens.offsetWidth) {
            positionLeft = imgElement.width - lens.offsetWidth;
        }

        if (positionTop > imgElement.height - lens.offsetHeight) {
            positionTop = imgElement.height - lens.offsetHeight;
        }

        lens.style.left = positionLeft + 'px';
        lens.style.top = positionTop + 'px';
        lens.style.backgroundPosition = '-' + (pos.x * ratio) + 'px ' + '-' + (pos.y * ratio) + 'px';
    }

    function getCursorPos(event) {
        let bounds = imgElement.getBoundingClientRect();
        let x = event.pageX - bounds.left - window.pageXOffset;
        let y = event.pageY - bounds.top - window.pageYOffset;

        return { 'x': x, 'y': y };
    }
}

document.querySelectorAll('.img-zoom').forEach(imgElement => {
    setupImageZoom(imgElement);
});





document.getElementById('i').value = document.getElementById('in').value;

document.getElementById('in').addEventListener('input', function() {
    document.getElementById('i').value = this.value;
});

function up() {
    var currentValue = parseInt(document.getElementById('i').value, 10);
    document.getElementById('i').value = currentValue + 1;
}

function down() {
    var currentValue = parseInt(document.getElementById('i').value, 10);
    if (currentValue > 1) {
        document.getElementById('i').value = currentValue - 1;
    }
}






