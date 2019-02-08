$(document).ready(function() {
    // Highlight the home tab
    $(function () {
      $('ul.primary-nav li a').removeClass('active');
      $('ul.primary-nav li a.home').addClass('active');
    });
});

function scroll_to_anchor(anchor_id){
    var tag = $("#"+ anchor_id);
    $('html,body').animate({scrollTop: tag.offset().top},'fast');
}

$("#main-button").click(function() {
   scroll_to_anchor('examples');
});

$(document).ready(function() {
    $("body").tooltip({ selector: '[data-toggle=tooltip]' });
});

function CopyToClipboard(elementId) {
  var aux = document.createElement("input");
  aux.setAttribute("value", document.getElementById(elementId).innerHTML);
  document.body.appendChild(aux);
  aux.select();
  document.execCommand("copy");
  document.body.removeChild(aux);
  $.notify("Command copied to clipboard",  "success");
}