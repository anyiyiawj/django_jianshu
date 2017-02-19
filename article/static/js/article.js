$(function () {
  $(".like").click(function () {
    var $this =  $(this);
    var article = $(this).parent().attr("article-id");
    $.ajax({
      url: '/article/like/',
      data: {
        'article': article,//返回的值
      },
      type: 'post',
      success: function (data){
        if ($this.hasClass("unlike")) {
          $this.removeClass("unlike");
          $this.find('.text').text("赞");//this值的变化
        }
        else {
          $this.addClass("unlike");
          $this.find('.text').text("撤销");
        }
        $this.find('.like-count').text(data);
      }
    });
    return false;
  });   
});
 

