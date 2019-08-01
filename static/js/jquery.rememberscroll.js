// jquery.rememberscroll.js a jQuery plugin that remembers where user scrolls in a web page. When the user comes back to the page later, it automatically jumps to the most recent scroll position 
// Author: Steve
//
// function $.scrollTrack
// Description: Enable tracking of web page scroll position
// parameters:
//     seconds: the frequency, i.e. in every this number of seconds the page scroll position will be queried, default is 2 seconds
//     expiredays: number of days cookies will be effective to store position data, default is 365 days
// Usage example 1: $.positionTrack()
// Usage example 2: $.positionTrack(1)
// Usage example 2: $.positionTrack(1, 365*5)
//
// The function can normally be called from within jQuery $(document).ready block.

$.scrollTrack = function(seconds, expiredays) {

	if (typeof seconds === 'undefined') seconds = 2;
	if (typeof expiredays === 'undefined') expiredays = 365;
	
	var position = $.cookie('position');
	if (typeof position === 'undefined') {
		position = 0;
		$.cookie('position',position,{expires: expiredays});
	}
	window.scrollBy(0,position);
	
	setInterval(function() {
		var position = $.cookie('position');
		if (this.scrollY == position) return;
		position = this.scrollY;
		$.cookie('position',position,{expires: expiredays});
	},1000*seconds);
	
};
// $(document).ready(function () {
// 	$("#main-table").scroll(function () {
// 		/*alert("scrolTop:"+$(this).scrollTop()+
// 			"offset:"+$(".getoffset").offset());*/
// 		console.log(
// 			"scrolTop:"+$("#main-table body").scrollTop()+
// 			"offset:"+($("#main-table body").offset().top - $("#main-table body").offsetParent().offset().top))
// 	});
// 	var scrollOffset = $(".container-fluid #main-table body")[0].offsetTop - $(".container-fluid")[0].offsetTop
// 	console.log(scrollOffset)
// });
// $(document).ready(function () {
//
// 	// var scrollOffset = $(".container-fluid #main-table body")[0].offsetTop - $(".container-fluid")[0].offsetTop
// 	// console.log(scrollOffset)
// 	const container = document.querySelector('tr')
//     console.log(container.scrollTop)
//     console.log(container.scrollLeft)
// });
