var csrftoken = document.getElementsByName('csrfmiddlewaretoken')[0].value;
// 创建编辑窗口
var E = window.wangEditor;
var editor = new E('#editorContent');
editor.customConfig.uploadImgServer = "/utils/uploadfile/";
editor.customConfig.uploadImgParams = {
    source: 'contentImage',
    filetype:'image',
    csrfmiddlewaretoken:csrftoken

}
editor.customConfig.uploadFileName = 'file'; 
editor.customConfig.uploadImgMaxLength = 5;
editor.create();
$(".w-e-text-container").css("height", "500px");



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
    //var s = getObjectURL(e[0]);
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
    formdata.append('file', e[0]);
    formdata.append('filetype','image');
    formdata.append('source','cover');
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

function save() {
    var csrftoken = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    // 获取标题
    var titleArticle = document.getElementsByClassName('title-article')[0].value;

    // 获取正文
    var content = editor.txt.html();
    // alert(content);

    // 获取封面
    // var cover = $('#travelImgs')[0].files
    var img=document.getElementById("o_photo_img");
    var coverPath = img.getAttribute("src");
    // alert(coverPath);

    // 获取分类
    var myselect=document.getElementById("sel1");
    var index=myselect.selectedIndex ;
    var classification = myselect.options[index].text;
    // alert(classification);

    // 获取标签
    var tagArr = document.getElementById('sel3');
    var tagStr = '';
    for(var i = 0;i<tagArr.length;i++){
        tagStr = tagStr+tagArr[i].innerText+";";
    }
    // 获取状态
    var selectStatus=document.getElementById("sel4");
    var indexSel4=selectStatus.selectedIndex ;
    var statusArticle = selectStatus.options[indexSel4].text;
    // alert(statusArticle);
    // 获取排序序号
    var sort = document.getElementsByClassName('sort-input')[0].value;
    // alert(sort);

    // ajax post提交
    $.post('/article/write/',
    {
        arTitle:titleArticle,
        arContent:content,
        coverPath:coverPath,
        classification:classification,
        tag:tagStr,
        statusArticle:statusArticle,
        sort:sort,
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
                window.location.href='http://'+ window.location.host + '/myadmin/article/';

            }
            
        }else
        {
            alert("上传数据错误");
        }
        
    });

}