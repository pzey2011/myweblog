
$( document ).ready(function() {
    $('.dropdown-toggle').text();
    $('.dropdown-menu li a').click(function() {
        $('.dropdown-toggle').html($(this).html());
        $("input[name='privacy']").val($(this).text().trim().toLowerCase());
    });
    $("#comment").submit(function() {
        $("input[name='title']").val($)
    });
});