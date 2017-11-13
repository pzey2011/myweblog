
$( document ).ready(function() {

    $('.dropdown-menu li a').click(function() {
        $('.dropdown-toggle').html($(this).html());
        $("input[name='privacy']").val($(this).text().trim().toLowerCase())
    });

});