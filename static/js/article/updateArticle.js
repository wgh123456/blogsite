
// 获取图片预览地址函数
function getObjectURL(file) {  
    var url = null;   
    if (window.createObjectURL!=undefined) {  
        url = window.createObjectURL(file) ;  
    } else if (window.URL!=undefined) { // mozilla(firefox)  
        url = window.URL.createObjectURL(file) ;  
    } else if (window.webkitURL!=undefined) { // webkit or chrome  
        url = window.webkitURL.createObjectURL(file) ;  
    }  
    return url ;  
}
// 上传图片 
function uploader(e){
    var csrftoken = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    // 将图片信息通过getObjectURL函数处理出预览地址
    var s = getObjectURL(e[0]);
    // alert(s);
    // 获取img元素，label元素，div[上传按钮]元素
    var img=document.getElementById('o_photo_img');
    // 设置图片展示样式
    img.style.padding='3px';
    img.style.borderStyle='solid';
    img.style.borderColor='#eee';
    img.style.borderWidth='1px';
    img.style.display='block';
    // 设置img的src值实现图片预览
    // img.src=s;

    var formdata = new FormData();
    formdata.append('coverImage', e[0]);
    formdata.append('csrfmiddlewaretoken',csrftoken);

    $.ajax({
        method: 'POST',
        url: '/article/upload/cover/',
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


		

function myFunction1(e){
    e.parentNode.removeChild(e);
    var li = document.createElement("option");
    var textnode=document.createTextNode(e.innerText);
    li.appendChild(textnode);
    li.setAttribute("ondblclick","myFunction2(this)");
    var ul = document.getElementsByClassName('select-bei');
    document.getElementById('sel3').appendChild(li);
}

function myFunction2(e){
    e.parentNode.removeChild(e);
    var li = document.createElement("option");
    var textnode=document.createTextNode(e.innerText);
    li.appendChild(textnode);
    li.setAttribute("ondblclick","myFunction1(this)");
    var ul = document.getElementsByClassName('select-zhu');
    document.getElementById('sel2').appendChild(li);
}
