$(function () {
  // Bootstrap select
  $('.selectmultiple').selectpicker({noneSelectedText: '---------'});
  $('.bootstrap-select button').addClass("form-control")

  // Star rating
  options = {
    min: 0,
    max: 5,
    step: 1,
    size: 'xs',
    showClear: false,
    showCaption: false,
    theme: 'krajee-uni',
  }
  $("#id_score").rating(options);

  options.displayOnly = true
  $(".score-display").rating(options);

  // Language picker
  var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
  $.ajaxSetup({
    beforeSend: function (xhr, settings) {
      if (!this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    }
  });

  $('.change-language').click(function (e) {
    $('#language').val($(this).attr('data-lang-code'));
    $('#change-language-form').submit();
  });
});
