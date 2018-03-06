 jQuery(document).ready(function(){
				
	//
	jQuery(".slogan-wrapper").parents(".col-md-12").css({"padding":0});
	//
	
			jQuery(".site-nav-toggle").click(function(){
				jQuery(".site-nav").toggle();
			});
	
			jQuery(".site-search-toggle").click(function(){
				jQuery(".search-form").toggle();
			
		});
			
 	// carousel
     if( jQuery(".owl-carousel").length ) {
	 var owl = jQuery(".owl-carousel");
      owl.owlCarousel({
      items : owl.data("num"), // items num above 1000px browser width
      itemsDesktop : [1000,4], //5 items between 1000px and 901px
      itemsDesktopSmall : [900,3], // 3 items betweem 900px and 601px
      itemsTablet: [600,2], //2 items between 600 and 0;
      itemsMobile : false, // itemsMobile disabled - inherit from itemsTablet option
	  afterInit:torch_clients_tip
      
      });
	 }
	// clients tip
	function torch_clients_tip(){
	jQuery('.owl-carousel .item img').tooltip('hide');
	}
		
	
 });
 
/* if(typeof torch_js_var !== 'undefined' && typeof torch_js_var.global_color !== 'undefined'){
 less.modifyVars({
        '@color-main': torch_js_var.global_color
    });
   }*/