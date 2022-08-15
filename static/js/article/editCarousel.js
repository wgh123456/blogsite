function uploader(e)
{
    var csrftoken = document.getElementsByName('csrfmiddlewaretoken')[0].value;

    var img=document.getElementById('o_photo_img');
    img.style.padding='3px';
    img.style.borderStyle='solid';
    img.style.borderColor='#eee';
    img.style.borderWidth='1px';
    img.style.display='block';

    var formdata = new FormData();
    formdata.append('file', e[0]);
    formdata.append('filetype','image');
    formdata.append('source','carousel');
    formdata.append('csrfmiddlewaretoken',csrftoken);

    $.ajax({
        method: 'POST',
        url: '/utils/uploadfile/',
        data: formdata,
        contentType: false,
        processData: false,
        success: function(res) {
            if(res.status==100){
                alert(res.data);
            }else if(res.status==200){
                img.src=res.data[0];
            }
           
        }
   });
}

function SaveCarousel()
{
    var img=document.getElementById("o_photo_img");
    var carouselPath = img.getAttribute("src");
    var titleCarousel = document.getElementById('carousel-title').value;
    var description = document.getElementById("description").value;
    var csrftoken = document.getElementsByName('csrfmiddlewaretoken')[0].value;

    if(description.length>200)
    {
        alert("输入文字过长，请删减文字");
        return;
    }

    var myselect=document.getElementById("related-article");
    var index=myselect.selectedIndex ;
    var related = myselect.options[index].text;
   

    var selectStatus=document.getElementById("status");
    var status=selectStatus.selectedIndex ;
    
    $.post('/article/carouseledit/',
    {
        carouselPath:carouselPath,
        titleCarousel:titleCarousel,
        description:description,
        related:related,
        status:status,
        csrfmiddlewaretoken:csrftoken
    },
    function(data,status){
        if(status=="success")
        {
            if(data.status==100)
            {
                alert(data.data);
            }
            else if(data.status)
            {//保存文章成功
                alert(data.data);
                window.location.href='http://'+ window.location.host + '/myadmin/carousel/';

            }
            
        }else
        {
            alert("上传数据错误");
        }
        
    });

    
}