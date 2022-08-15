var old_carousel_table_content="";
var carousel_id;
function myDbclick(e)
{
    var content = e.innerText;
    old_carousel_table_content = content;

    e.style.display="none";
    e.nextElementSibling.style.display="inline";
    
}

function changeModelInfo(e,updateid,type)
{
    carousel_id = updateid
    var content = e.getAttribute('title');
    if(type=='title')
    {
        document.getElementById('title-txt').value="";
        document.getElementById('title-txt').value=content;
    }
    else if(type == 'detail')
    {
        document.getElementById('detail-txt').value="";
        document.getElementById('detail-txt').value=content;
    }
    
    
}

function updateInfo(type)
{
    var csrftoken = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    var content;
    if(type=='title')
    {
        content = document.getElementById('title-txt').value;
    }
    else if(type == 'detail')
    {
        content = document.getElementById('detail-txt').value
    }

    $.post('/article/carouselupdate/',
        {
            content:content,
            update_id:carousel_id,
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

function inputonblur(e,updateid,type)
{
    var csrftoken = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    var content;
    if(type=="articleid")
    {
        var index = e.selectedIndex;
        content = e.options[index].value;
    }else if(type=="status")
    {
        var index = e.selectedIndex;
        content = e.options[index].value;  
    }

    if(old_carousel_table_content==content)
    {
        e.style.display="none";
        e.previousElementSibling.style.display="inline";
        return;
    }

    if(content=='发布')
    {
        content = "True";
    }else if(content=='禁用'){
        content = "False"; 
    }
    


    $.post('/article/carouselupdate/',
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

