// get keyword from last page
var key = decodeURI(document.location.href.split("=")[1]);
document.title = key;

document.getElementById("img").src = "./res/cloud/".concat(key).concat(".png");
