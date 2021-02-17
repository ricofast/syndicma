$("#join").click(function () {
    let form = $("#join-request-form")
    let url = form.attr('action');
    let button = $(this)

    $.post({
        url: url,
        data: form.serialize(), // serializes the form's elements.
        success: function (data) {
            console.log(data); // show response from the php script.
            $("#join-request-sent-alert").removeClass("d-none");
            button.hide();
        }
    });
})
