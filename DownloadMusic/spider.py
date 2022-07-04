import os
import requests
import re
from copy import deepcopy
from ffmpy3 import FFmpeg
from lxml import etree
from multiprocessing import Pool


def make_directory():
    # 生成视频存放路径
    if not os.path.exists("video"):
        os.makedirs("video")
    # 生成音乐存放路径
    if not os.path.exists("music"):
        os.makedirs("music")


def get_url_from_file():
    content = None
    with open('readme.md', 'r', encoding='UTF-8') as f:
        f.readline()
        content = f.read()
    return content.split()


# 判断文件是否存在
def is_exist(name):
    if os.path.exists(name):
        return True
    else:
        return False


# 下载
def download(url):

    try:
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,'
                      'image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'
        }

        headers1 = deepcopy(headers)
        headers1['Referer'] = url

        html = requests.get(url, headers=headers).text
        etree_html = etree.HTML(html)

        name = etree_html.xpath('//*[@id="viewbox_report"]/h1/span/text()')[0]

        # B站目前视频有两种格式：flv和m4s，如果是m4s则最后一个链接就是音乐链接，如果是flv则直接获取到视频的链接
        m4s_url_list = re.findall('"baseUrl":"(.+?)"', html)
        flv_url_list = re.findall('"url":"(.+?)"', html)

        print(name + "开始下载！")
        if len(m4s_url_list) > 0:
            music_url = m4s_url_list[-1]
            music_name = "music//"+name+".mp3"

            if is_exist(music_name):
                print(name + "已经存在")
                return

            with open(music_name, 'wb') as f:
                f.write(requests.get(music_url, headers=headers1).content)
            print(name + "下载完成！")
        else:
            video_url = flv_url_list[0]
            video_name = "video//"+name+".flv"
            music_name = "music//"+name+".mp3"

            if is_exist(music_name):
                print(name + "已经存在")
                return
            if not is_exist(video_name):
                # 下载flv格式的视频
                with open(video_name, 'wb') as f:
                    f.write(requests.get(video_url, headers=headers1).content)

            # 提取出flv格式的视频中音频保存为mp3文件
            ff = FFmpeg(inputs={video_name: None}, outputs={music_name: None})
            ff.run()

            print(name + "下载完成！")

    except TimeoutError as e:
        print(e)


def main():
    make_directory()  # 生成存放音频视频的文件夹
    url_list = get_url_from_file()  # 读取文件中视频的url
    # 使用多进程
    count = 5
    if len(url_list) < count:
        count = len(url_list)
    with Pool(processes=count) as pool:
        pool.map(download, url_list)


if __name__ == '__main__':
    main()