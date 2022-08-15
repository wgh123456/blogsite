var time = 60;

function TestCheckCodeFormat(email)
{
    var pattern = /\w[-\w.+]*@([A-Za-z0-9][-A-Za-z0-9]+\.)+[A-Za-z]{2,14}/;
    if(!pattern.test(email))
    {
        return false;
    }
    return true;
}

function matchStr(str)
{
    var pattern = /[\/\.\?\=]/;
    if(pattern.test(str))
    {
        return true;
    }
    return false;
}

function CheckPhone(phone)
{
    var pattern = /0?(13|14|15|17|18|19)[0-9]{9}/;
    if(pattern.test(phone))
    {
        return true;
    }
    return false;
}

$(document).ready(function(){
    $('.login-enter').click(function(){
       var email = $('#login-email').val();
       var password = $('#login-pwd').val();
       var verify = $('#login-verify').val();
       var remember = $('#remember:checked').is(':checked');
       var csrftoken = document.getElementsByName('csrfmiddlewaretoken')[0].value;

       if(email==""||password==""||verify=="")
       {
            alert("用户信息不能为空");
            return;
       }
       
        if(!TestCheckCodeFormat(email))
        {
            alert('邮箱格式错误');
            return;
        }


       $.post(
        "/user/login/",
        {
            email:email,
            password:password,
            verify:verify,
            remember:remember,
            csrfmiddlewaretoken:csrftoken
        },
        function(data,status){
            if(status=="success"){
                if(data.status==100){
                    alert(data.data);
                }else if(data.status==200){
                    // alert("登录成功");
                    window.location.href='http://'+ window.location.host;
                }
                
            }
            else
            {
                alert("failed");
            }
        });
    });


    // 注册
    $('.register-enter').click(function(){
        var email = $('#register-email').val();
        var checkcode = $('#email-code').val()
        var password = $('#register-pwd').val();
        var ack_password = $('#register-ack-pwd').val();
        var verify = $('#register-verify').val();
        var csrftoken = document.getElementsByName('csrfmiddlewaretoken')[0].value;

        if(email==""||checkcode==""||password==""||ack_password==""||verify=="")
        {
            alert('输入项不能为空');
            return;
        }
        
        if(!TestCheckCodeFormat(email))
        {
            alert('邮箱格式错误');
            return;
        }

        if(password!=ack_password)
        {
            alert("两次密码不一致");
            return;
        }

        $.post(
            "/user/register/",
            {
                email:email,
                checkcode:checkcode,
                password:password,
                ack_password:ack_password,
                verify:verify,
                csrfmiddlewaretoken:csrftoken
            },
            function(data,status){
                if(status=="success"){
                    if(data.status==100){
                        alert(data.data);
                    }else if(data.status==200){
                        alert("注册成功，请返回界面登录");
                        window.location.href='http://'+ window.location.host;
                    }
                    
                }
                else
                {
                    alert("failed");
                }
            });

        
       
    });

    // 获取邮箱校验码
   
    $('.btn-email-code').click(function(){
        var email = $('#register-email').val();
        var csrftoken = document.getElementsByName('csrfmiddlewaretoken')[0].value;
        if(email=="")
        {
            alert("请填写邮箱");
            return;
        }

        $.post(
            "/utils/emailcheckcode/",
            {
                email:email,
                csrfmiddlewaretoken:csrftoken
            },
            function(data,status){
                if(status=="success"){
                    if(data.status==100){
                        alert(data.data);
                    }else if(data.status==200){
                        alert(data.data);
                        var timer = setInterval(function(){
                            time--;
                            $('.btn-email-code').text(time + "秒");
                            $('.btn-email-code').addClass('disabled');
                            if (time==0) {
                              time = 60;
                              clearInterval(timer);
                              $('.btn-email-code').text("获取校验码");
                              $('.btn-email-code').removeClass('disabled');
                            }
                          },1000);
                    }
                    
                }
                else
                {
                    alert("failed");
                }
            });


        
    });
});


function search()
{
    var search_content = document.getElementById('search-input').value;
    var csrftoken = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    if(search_content=='')
    {
        alert('不能为空');
        return;
    }
    
    if(matchStr(search_content))
    {
        alert("不能含有特殊字符");
        return;
    }

    path = '/index/search/'+search_content+'/';
    $.get(
        path,
        {
            content:search_content,
            csrfmiddlewaretoken:csrftoken
        },
        function(data,status){
            if(status=="success"){
                window.location.href='http://'+ window.location.host + path;
            }
            else{
                window.location.href='http://'+ window.location.host;
            }
        }
    );
}

function uploader(e,updateid,type)
{
    var img=document.getElementsByClassName('headshot-show')[0];
    var csrftoken = document.getElementsByName('csrfmiddlewaretoken')[0].value;


    var formdata = new FormData();
    formdata.append('content', e[0]);
    formdata.append('type',type);
    formdata.append('update_id',updateid);
    formdata.append('csrfmiddlewaretoken',csrftoken);
   

    $.ajax({
        method: 'POST',
        url: '/user/update/',
        data: formdata,
        contentType: false,
        processData: false,
        success: function(res) {
            if(res.status==100){
                alert(res.data);
            }else if(res.status==200){
                img.src=res.data;
            }
           
        }
   });
}

var old_value;
function pondblclick(e)
{
    old_value = e.innerText;
    e.setAttribute('contenteditable','true');
    // e.innerText = '';

}

function ponblur(e,updateid,type)
{
    var csrftoken = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    var content;
    if(type=='username'||type == 'sex'||type == 'phone')
    {
        content = e.innerText;
    }

    // if(content=='')
    // {
    //     e.innerText = old_value;
    //     return;
    // }

    if(content == old_value)
    {
        return;
    }
    
    if(type == 'sex')
    {
        if(content == '男'|| content == '男\n')
        {
            content = 1;
        }else if(content == '女' || content == '女\n')
        {
            content = 0;
        }else
        {
            alert('性别只能填写男或者女');
            e.innerText = old_value;
            return;
        }
    }

    if(type == 'phone')
    {
        if(!CheckPhone(content))
        {
            alert('手机号不符合');
            e.innerText = old_value;
            return;
        }
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
                    e.setAttribute('contenteditable','false');
                    alert("修改成功");
                    
                }
            }
            else
            {
                alert("修改失败");
            }
        }  

    );

}