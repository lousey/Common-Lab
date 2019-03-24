(function ($) {
$.fn.center = function() {
	return this.each(function(i){
	var ah = $(this).outerHeight();
	var ph = $(this).parent().height();
	var aw = $(this).outerWidth();
	var pw = $(this).parent().width();
	var mh = Math.ceil((ph-ah) / 2);
	var mw = Math.ceil((pw-aw) / 2);
	$(this).css('margin-top', mh);
	$(this).css('margin-left', mw);});
};
})(jQuery);

var carousel, carousel_shift, carousel_margin, carousel_locked;

/**
 * this carousel implementations refers to a <ul> with five <li> slides,
 * ids #slide_1 through #slide_5. #slide_3 is the center slide. #slide_2
 * and #slide_4 hang off the page edges. when next/prev is clicked for the
 * carousel, #slide_5 or #slide_1 is loaded, respectively, and the carousel
 * is shifted. 
 */

// calculate position for caorusels with < 5 slides
var fix_position = function (position) {
	var cl = carousel_content.length;
	if (position < 0) {
		return cl + position;
	} else if (position >= cl) {
		return position - cl;
	} else {
		return position;
	}
};	

var load_slide = function(slide_index, content_index, ccallback) {
	var slide = $("#slide_"+slide_index);
	var content = carousel_content[content_index];
	var video_html = content.video_html;
	var p = slide.find("p").first();
	var caption = (content_index == 0) ? "<em>"+content.caption+"</em>" : content.caption;
	p.html(caption);
	/*if (content_index == 0) {
		//Cufon.replace("#slide_"+slide_index + " .regular_copy_font", {fontFamily: "KnockoutMiddleweight"});
	};*/
	slide.find("iframe").remove();
	var img = slide.find("img");
	if (video_html != "") {		
		var iframe = $(content.video_html);
		iframe.load(function() {$(this).center(); if (ccallback) ccallback(); });
		slide.find(".carousel_media").prepend(iframe);
		img.hide();
	} else {
		img.show();
		img.load (function() {$(this).center(); if (ccallback) ccallback(); });
		img.attr('src', content.url).attr('alt', content.alt);
	};
};

var init_carousel = function(start_position, icallback) {
	carousel = $("#carousel");
	carousel_shift = $("#carousel > li").first().width() + 120;
	carousel_margin = carousel.css("margin-left");
	carousel.data("current_slide", start_position);
	carousel_locked = false;
	$("#carousel_total").html(carousel_content.length);
		
	$("#carousel_next").click(function(){
		move_carousel(-1);
		return false;
	});
	$("#carousel_prev").click(function(){
		move_carousel(1);
		return false;
	});	
	
	$("#carousel").delegate("li", "click", function() {
		if ($(this).attr("id") == "slide_4") 
			move_carousel(-1);
		else if ($(this).attr("id") == "slide_2")
			move_carousel(1);
	});
			
	if (carousel_content.length == 1) {
		$("#carousel").find("li").css("visibility","hidden");
		$("#slide_3").css("visibility","visible");
		load_slide(3, 0, icallback);
		$("#carousel_controls").css("visibility","hidden");
		$("#slide_3").find(".carousel_overlay").hide();
		$("#slide_3").find("p").show();			
		return;
	};

	if (carousel_content.length == 0) {
		$("#carousel_controls").hide();
		$("#carousel_wrapper").hide();
		return;
	}

	load_slide(3, start_position, icallback);
	load_slide(2, fix_position(start_position - 1));
	load_slide(4, start_position + 1);
	$("#carousel").find("p").hide();
	$("#slide_3").find(".carousel_overlay").hide();
	$("#slide_3").find("p").show();		
	
};

var move_carousel = function(direction) {
	if (carousel_locked) return;
	carousel_locked = true;
	
	var current_slide = carousel.data("current_slide");
	if (direction == 1) { 
		load_slide(1, fix_position(current_slide - 2));
	} else {
		load_slide(5, fix_position(current_slide + 2));
	}
	
	var lis = carousel.children("li");
	lis.find("p").fadeOut(200);
	lis.find(".carousel_overlay").fadeIn(200);

	carousel.delay(200).animate({ marginLeft: "+=" + carousel_shift * direction }, 200, "swing", 
		function() {
			var new_slide = fix_position(current_slide + -1 * direction);
			carousel.data("current_slide", new_slide);
			if (direction == 1) {
				var last = $("ul#carousel li:last");
				last.remove();
				$("ul#carousel").prepend(last);
			} else {
				var first = $("ul#carousel li:first");
				first.remove();
				$("ul#carousel").append(first);				
			};
			var counter = 1;
			carousel.children("li").each(function(){
				$(this).attr("id", "slide_"+counter);
				counter += 1;
			});
			carousel.css("marginLeft", carousel_margin);
			
			var slide_3 = $("#slide_3");
			slide_3.find("p").delay(50).fadeIn(200);
			slide_3.find(".carousel_overlay").delay(50).fadeOut(200);		
			setTimeout (function() { carousel_locked = false }, 270);
			$("#carousel_no").html(new_slide + 1);
		}
	);
};


$(document).ready(function() {
	
	// subnavigation link interactions
	$("#subnavigation").delegate("a", "mouseenter", function() {
		var children = $(this).attr("class").split(" ");
		for (var i=0; i<children.length; i++) {
			$("#"+children[i]).addClass("sublink_state");
		}		
	}).delegate("a", "mouseleave", function() {
		$("ul.subnav_links").find("a").removeClass("sublink_state");
	}).delegate(".subnav_cats > li > a", "click", function() {
		return false;
	});
	
	// navigation controls tooltip
	var nav_tooltip = function(){
		var tt = document.createElement('div');
		tt.setAttribute('id', 'navigation_control_text');
		document.body.appendChild(tt);
		tt.style.display='none';
		return {
			show: function (jq_elem, text_align, xoffset, yoffset) {
				var offset = jq_elem.offset();
				tt.style.top = offset.top + yoffset + "px";
				tt.style.display='block';
				tt.style.textAlign=text_align;
				tt.innerHTML = jq_elem.data("name");
				tt.style.left = offset.left + xoffset + "px";
			},
			hide: function () {
				tt.style.display='none';
			}
		};
	}();
	
	$("#project_detail > a.nav_next").mouseenter(function(){
		nav_tooltip.show($(this), 'left', 15, 0);
	}).mouseleave(function(){
		nav_tooltip.hide();
	});

	$("#project_detail > a.nav_previous").mouseenter(function(){
		nav_tooltip.show($(this), 'right', -70, 0);
	}).mouseleave(function(){
		nav_tooltip.hide();
	});
	
	$("#person_prev").mouseenter(function(){
		nav_tooltip.show($(this), 'left', 15, 0);
	}).mouseleave(function(){
		nav_tooltip.hide();
	});

	$("#person_next").mouseenter(function(){
		nav_tooltip.show($(this), 'right', -70, 0);
	}).mouseleave(function(){
		nav_tooltip.hide();
	});

	// project, people grids
	$(".grid_link").mouseenter(function(){
		var a = $(this);
		if (a.data("locked") || a.data("bounced")) return;
		a.data("locked", true);
		a.data("bounced", true);
		a.addClass("hovered");
		a.effect("bounce", { distance: 10 }, 150);
		a.delay(200).data("locked", false);
	}).mouseleave(function(){
		var a = $(this);
		if (a.data("locked")) return;
		$(this).removeClass("hovered");
		a.data("bounced", false);
	}).data("locked", false).data("bounced", false);
	
	// open external links in a new window
	$('a[rel*=external]').click( function() {
		window.open(this.href);
		return false;
	});
	
	// subnavigation slides in/out
	$("#nav_menu_btn").data("open", false).mouseenter(function() {
		var open = $("#nav_menu_btn").data("open")
		if (open) {
			$("#subnavigation").animate({"height": "0px"}, 50, "swing");
			$(this).data("open",false);
			$("#nav_menu_sign").html("+");
		} else {
			$("#subnavigation").animate({"height": "143px"}, 50, "swing");
			$(this).data("open",true);
			$("#nav_menu_sign").html("-");
		};
	});

	
});

