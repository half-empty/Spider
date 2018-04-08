# 遍历json，下载文件id从start到end，开多进程
import os
import linecache
import json
import requests
# from PIL import Image

filepath = '/home/sunweifeng/Picture/pexels'

def getListFiles(path, start, end):
    ret = []
    for id in range(start, end + 1):
        src = os.path.join(path, str(id) + '.jpeg')
        if not os.path.exists(src) or os.path.getsize(src) == 0:
            ret.append(id)
        #else: # bad image
        #    try:
        #        img = Image.open(src) # open the image file
        #        #img.verify() # verify that it is, in fact an image
        #except (IOError, SyntaxError) as e:
        #        ret.append(id)
        #except:
        #    pass
    return ret

ret = getListFiles(os.path.join(filepath, 'image'), 20000, 22000)
print(ret)

file_path = os.path.join(filepath, 'pexels.json')
for i in ret:
    print(i)
    # 获取自定行json
    temp_num = int(i)
    temp_json = linecache.getline(file_path, int(i))
    temp_dict = json.loads(temp_json)
    image_url = temp_dict['image_url']
    image_file = '/home/sunweifeng/Picture/pexels/image'
    if not os.path.exists(image_file):
        os.makedirs(image_file)
    with open(os.path.join(image_file, str(i) + '.jpeg'), 'wb') as handle:
        status = 0
        # 图片爬挂重连
        while status != 200:
                try:
                    response = requests.get(image_url, timeout=30)
                    status = response.status_code
                    for block in response.iter_content():
                        if not block:
                            print('!!!')
                            break
                        handle.write(block)
                except:
                    break
