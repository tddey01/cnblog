$("#div_digg .action").click(function () {
    var is_up = $(this).hasClass("diggit");

    $obj = $(this).children("span");
    $.ajax(
        {
            url: "/digg/",
            type: "post",
            data: {
                "csrfmiddlewaretoken": $("[name = 'csrfmiddlewaretoken']").val(),
                'is_up': is_up,
                "article_id": "{{ article_obj.pk }}",

            },
            success: function (data) {
                console.log(data);

                if (data.state) {

                    var val = parseInt($obj.text());
                    $obj.text(val + 1);

                    // 局部刷新
                    //if(is_up){
                    //   var val = parseInt($("#digg_count").text());
                    //  $("#digg_count").text(val + 1);
                    //}else {
                    // var val = parseInt($("#bury_count").text());
                    // $("#bury_count").text(val + 1);
                    //}

                } else {
                    var val = data.handled ? "您已经推荐过" : "您已经反对过过";
                    $("#digg_tips").html(val);

                    //if (data.handled){
                    //    $("#digg_tips").html("您已经推荐过")
                    //}else {
                    //    $("#digg_tips").html("您已经反对过过")
                    //}
                    setTimeout(function () {
                        $("#digg_tips").html("")
                    }, 1000)
                }
            }
        }
    )
})
