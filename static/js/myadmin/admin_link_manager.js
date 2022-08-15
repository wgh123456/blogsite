var old_value="";

function addlink()
{
    var linkname = document.getElementById('linkname').value;
    // var parentlinkname = document.getElementById('parentlinkname').value;
    var myselect=document.getElementById("parentlink");
    var index=myselect.selectedIndex ;
    var parentlinkname = myselect.options[index].text;
    var csrftoken = document.getElementsByName('csrfmiddlewaretoken')[0].value;

    if(linkname==''){
        alert("导航不能为空")
    }else{
        $.post('/link/add/',
            {
                linkname:linkname,
                parentlinkname:parentlinkname,
                csrfmiddlewaretoken:csrftoken
            },
            function(data,status){
                if(status=="success")
                {
                    if(data.status==100)
                    {
                        alert("导航添加失败");
                    }
                    else if(data.status)
                    {
                        alert("导航添加成功");
                        location.reload();
                    }
                    
                }else
                {
                    alert("导航上传数据错误");
                }
            }
        );
    }
    
    
}

function inputonblur(e,updateid,type)
{
    var csrftoken = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    var content;
    if(type=="linkname")
    {
        content = e.innerText;
    }else if(type=="isactive")
    {
        var index = e.selectedIndex;
        content = e.options[index].value;
        
    }else if(type=="parentLink")
    {
        var index = e.selectedIndex;
        content = e.options[index].value;
    }

    if(old_value==content)
    {
        e.style.display="none";
        e.previousElementSibling.style.display="inline";
        return;
    }

    if(content=='激活')
    {
        content = "True";
    }else if(content=='禁用'){
        content = "False"; 
    }


    $.post('/link/update/',
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

function activeStatusDbclick(e)
{
    var content = e.innerText;
    old_value = content;

    e.style.display="none";
    e.nextElementSibling.style.display="inline";
    
}