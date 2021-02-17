$('.status-toggle').change(function (e) {
    let url = $(this).attr('data-ajax-target');
    let accepted = $(this).prop("checked")

    $.post({
        url: url,
        data: { accepted: accepted },
        success: function (data) {
            console.log(data);
        }
    });
});
