"use strict"

function viewList(location) {
	window.location = "/list/" + location;
}

function viewSortedList(location) {
	window.location = "/list/" + location + "?sort=type";
}