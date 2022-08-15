function deleteArticle(id)
{
    const ans = confirm("确认要删除？");
	if (ans===true) {
		$.get(
            '/article/delete/',
            {
                id:id
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
    }else{
    	
    	return;
    }


    
}