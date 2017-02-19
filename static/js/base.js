 $(function () {
    $("#headerwords1").children().click(function(){
        $(this).addClass("xuanzhong").siblings().removeClass("xuanzhong");
        });
    $("#head3").mouseover(function(){
        $("#head2").removeClass("hide")
    });
    $("#head2").mouseover(function(){
        $("#head2").removeClass("hide")
    });
     $("#head3,#head2").mouseout(function(){
        $("#head2").addClass("hide")
    });    
});     