$(document).ready(function () {

  $(".answer").each(function (i, item) {
    $(item).click(function () {
      var aid = $(item).data('id')
      var qid = $("#question").data('id');
      console.log(qid + " => " + aid);


      $.ajax({
        type: 'GET',
        url: '/answer/' + qid + '/' + aid,
        success: function (data) {
          if (data.correct) alert('Correct answer');

          window.location.href = '/game/' + (qid + 1)
        }
      });
    });
  });
});
