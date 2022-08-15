var old_value;

function myDbclick(e)
{
    var content = e.innerText;
    old_value = content;

    e.style.display="none";
    e.nextElementSibling.style.display="inline";
}

function selectonblur(e,updateid,type)
{
    var csrftoken = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    var content;
    if(type=='permission' || type=='isactive')
    {
        var index = e.selectedIndex;
        content = e.options[index].value;
    }
    else
    {
        return;
    }

    if(old_value==content)
    {
        e.style.display="none";
        e.previousElementSibling.style.display="inline";
        return;
    }

    if(content=='启用' || content=='管理员')
    {
        content = 1;
    }else if(content=='禁用' || content=='普通用户'){
        content = 0; 
    }


    $.post(
        '/user/update/',
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