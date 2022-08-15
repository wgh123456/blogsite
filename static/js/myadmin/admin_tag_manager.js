function addtag()
{
    var tagname = document.getElementById('tagname').value;
    var csrftoken = document.getElementsByName('csrfmiddlewaretoken')[0].value;

    if(tagname==''){
        alert("标签不能为空")
    }else{
        $.post('/tag/add/',
            {
                tagname:tagname,
                csrfmiddlewaretoken:csrftoken
            },
            function(data,status){
                if(status=="success")
                {
                    if(data.status==100)
                    {
                        alert("标签添加失败");
                    }
                    else if(data.status)
                    {
                        alert("标签添加成功");
                        location.reload();
                    }
                    
                }else
                {
                    alert("上传数据错误");
                }
            }
        );
    }
    
    
}


var old_tag_table_content="";
function inputonblur(e,updateid,type)
{
    var csrftoken = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    var content;
    if(type=="tagname")
    {
        content = e.innerText;
    }

    if(old_tag_table_content==content)
    {
        
        return;
    }

    $.post('/tag/update/',
        {
            content:content,
            update_id:updateid,
            type:type,
            csrfmiddlewaretoken:csrftoken
        },
        function(data,status){
            if(status=="success")
            {
                if(data.status==100)
                {
                    alert(data.data);
                    location.reload();
                }
                else if(data.status)
                {
                    // alert("修改成功");
                    location.reload();
                }
            }
            else
            {
                alert("修改失败");
            }
        }  

    );
}