
$( document ).ready(function() {
    $('.dropdown-toggle').text();
    $('.dropdown-menu li a').click(function() {
        $('.dropdown-toggle').html($(this).html());
        $("input[type='hidden']").val($(this).text().trim().toLowerCase());
    });

});