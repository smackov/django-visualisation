// Find current place in header where we are to highlight button
$(function() {

    var pathname_url = window.location.pathname;
    var href_url = window.location.href;

    $(".navbar-nav li").each(function () {

        var link = $(this).find("a").attr("href");

        if(pathname_url == link || href_url == link) {

            $(this).addClass("active");

        }

    });

});