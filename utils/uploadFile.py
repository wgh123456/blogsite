import json
import time
import os,uuid

#文件名hash化
def _hash_filename(filename):
    _, suffix = os.path.splitext(filename)
    return '%s%s' % (uuid.uuid4().hex, suffix) 


def generateUrl(filetype,source,file):
    if filetype=='image' and source=='cover':
        local_save_path = "static/images/cover/"
    elif filetype=='image' and source=='carousel':
        local_save_path = "static/images/carousel/"
    elif filetype=='image' and source=='contentImage':
        local_save_path = "static/images/detail/" + time.strftime("%Y%m%d", time.localtime()) + '/'
    
    isExists = os.path.exists(local_save_path)
    if not isExists:
        os.makedirs(local_save_path) 
    hash_file_name = _hash_filename(file.name)

    local_save_file = local_save_path + hash_file_name
    # 图片拷贝
    with open(local_save_file, 'wb') as f:
        for line in file.chunks():
            f.write(line)
        f.close()

    url = 'http://www.memcpy.top/' + local_save_file

    return url

def uploadfile(source,filetype,filelist):
   
    
    if filelist == None:
        resp = {'status': 100, 'data': '请选择图片'}
        return resp

    imageUrl = []
    for file in filelist:
        url = generateUrl(filetype,source,file)
        imageUrl.append(url)

    if source=='contentImage':
        resp = {'errno': 0, 'data': imageUrl}
    else:
        resp = {'status': 200, 'data': imageUrl}
    return resp