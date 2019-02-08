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

// Show the button when scrolled till 100px
window.onscroll = function() {scrollFunction()};

function scrollFunction() {
  if (document.body.scrollTop > 100 || document.documentElement.scrollTop > 100) {
    document.getElementById("up-arrow").style.display = "block";
  } else {
    document.getElementById("up-arrow").style.display = "none";
  }
}

// Scroll to the top
function topFunction() {
  document.body.scrollTop = 0; 
  document.documentElement.scrollTop = 0; 
}
