$(function() {
  // Video fitting
  $("div").fitVids();

  // Selected Header
  function markHeader() {
    if(window.location.hash.length > 0) {
      $("h1, h2, h3, h4, h5, h6").removeClass("mark");
      $(window.location.hash).addClass("mark");
    }
  }

  window.onhashchange = markHeader;
  markHeader();

 // Allow linking to headers
  $(".page :header").hover(function() {
    var url = window.location.origin + window.location.pathname + "#" + $(this).attr('id');
    $( this ).append( $( "<a href='" + url + "' id='directlink' class='glyphicon glyphicon-link'></a>" ) );
  }, function() {
    $("#directlink").remove();
  });

  // LazyYT
  $('.lazyYT').lazyYT();
})
