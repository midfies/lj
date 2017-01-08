var RUNNING_COUNT = 0;
$(document).ready(function(){
    var submit_button = $('#create');
    submit_button.on("click", function(e){
        $.ajax({
            url: 'journal/new-entry',
            data: {
                'csrf_token': $("[name='csrf_token']").val(),
                'title': $("[name='title']").val(),
                'category': $("[name='category']").val(),
                'tags': $("[name='tags']").val(),
                'body': $("[name='body']").val()
            },
            method: 'POST',
            success: function(){
                console.log("added");
                console.log(RUNNING_COUNT)
                if (RUNNING_COUNT !== 0){
                    id = RUNNING_COUNT;
                }
                else{
                    var id = $("#count").attr('data-id');
                }
                id = parseInt(id) + 1;
                console.log(id)
                var top = $("#count");
                var title = $("[name='title']").val();
                var category = $("[name='category']").val();
                var body = $("[name='body']").val();
                var tags = $("[name='tags']").val();
                var temp1 = "<article><h2><a href='journal/";
                var temp2 = "'>";
                var temp3 = " </a></h2><span id='time' class='glyphicon glyphicon-time'>Today</span><br><br><div class='row'><div class='col-sm-6 col-md-6'><span class='glyphicon glyphicon-folder-open'></span> &nbsp;<a href='journal/category/";
                var temp4 = "'>"
                var temp5 = "</a>&nbsp;&nbsp;";
                var temp6 = "</div><div class='col-sm-6 col-md-6'>&nbsp;<span class='glyphicon glyphicon-pencil'></span> <a href='#'>Comments</a></div></div><hr><img src='http://placehold.it/900x300' class='img-responsive'><br /><p class='lead'>";
                var temp7 = "</p><p class='text-right'><a href='journal/";
                var temp8 = ">Go to Post</a><span class='glyphicon glyphicon-chevron-right'></span></p><p class='text-right'><a class ='delete' href='journal/"
                var temp9 = "/delete'' data = ";
                var temp10 = ">Delete</a><span class='glyphicon glyphicon-trash'></span></p><hr><hr></article>";
                template_complete = temp1 + id + temp2 + title + temp3 + category + temp4 + category + temp5 + temp6 + body + temp7 + id + temp8 + id + temp9 + id + temp10;
                top.after(template_complete);
                RUNNING_COUNT = id

                $("[name='title']").val('')
                $("[name='body']").val('')
                $("[name='title']").val('')
                $("[name='body']").val('')
                $("[name='title']").val('')
                $("[name='body']").val('')
            }
        });        
    e.preventDefault();   
    });
});

