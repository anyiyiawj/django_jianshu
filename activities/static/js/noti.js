$(function () {
  $('#notifications').popover({html: true, content: 'Loading...', trigger: 'manual'});
  $("#notifications").click(function () {//点击
    if ($(".popover").is(":visible")) {
      $("#notifications").popover('hide');
    }
    else {
      $("#notifications").popover('show');
      $.ajax({
        url: '/notifications/last/',
        beforeSend: function () {//发送之前
          $(".popover-content").html("<div style='text-align:center'><img src='/static/img/load.gif'></div>");
          $("#notifications").css('color','gray');;//消除新消息类
        },
        success: function (data) {
          $(".popover-content").html(data);//设置内容
        }
      });
    }
    return false;
  });

  function check_notifications() {//检查消息，是否要有新消息通知，在加载完调用
    $.ajax({
      url: '/notifications/check/',
      cache: false,
      success: function (data) {
        if (data != "0") {
          $("#notifications").css('color','blue');
        }
        else {
          $("#notifications").css('color','gray');
        }
      },
      complete: function () {
        window.setTimeout(check_notifications, 30000);//重复检查
      }
    });
  };
  check_notifications();
});