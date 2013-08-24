// ===============
// MAIN

window.onload = function() {
	

	$.subscribe("/district/ellipse_click", DISTRICT.visgen);
	$.subscribe("/district/ellipse_hover", DISTRICT.el_hover);
	$.subscribe("/slider/slide", DISTRICT.slide_fcn);
	
	// HACK: initial district to center on
	var district_id = 162;
	
	// Generate initial vis
	DISTRICT.visgen(district_id);
};