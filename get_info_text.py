# 导包
import requests
from lxml import etree
import time


def get_info():
    # 目标url
    url = 'http://www.tsxsw.net/html/109/109706/'
    # 请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
        'Cookie': 'Hm_lvt_fc84acdc886053f94471501138a7e02a=1622958066; Hm_lpvt_fc84acdc886053f94471501138a7e02a=1622958123'
    }
    # 获取反应
    res = requests.get(url, headers=headers)
    # print(res.content.decode('gbk'))
    # 在使用utf-8编码时出错，同时查看网页乱码，发现需要用到gbk编码

    # 把类型转换为element类型数据
    html = etree.HTML(res.content.decode('gbk'))

    # 提取书名
    title = html.xpath('/html/body/div[2]/div[2]/div[2]/div[1]/div/h1/text()')[0]
    # print(title)

    # 提取作者名称
    author = html.xpath('/html/body/div[2]/div[2]/div[2]/div[1]/div/span/text()')[0]
    # print(author)

    # # 提取正文章节名称
    # Chapter_name = html.xpath('/html/body/div[2]/div[4]/ul/li[*]/a/text()')
    # print(Chapter_name)

    # 获取正文章节网址并存储在列表中
    Chapter_html1 = html.xpath('/html/body/div[2]/div[4]/ul/li[*]/a/@href')
    Chapter_html = []
    # 发现网址不全，补全网址
    for i in Chapter_html1:
        html1 = 'http://www.tsxsw.net' + str(i)
        Chapter_html.append(html1)
    # print(Chapter_html)

    for i in Chapter_html:
        # 每获取完一个章节内容后休息0.5秒
        time.sleep(0.5)
        # 不同章节的url
        url_i = i
        # 请求反应
        res = requests.get(url_i, headers=headers)
        # 把类型转换为element类型数据
        html = etree.HTML(res.content.decode('gbk'))
        # 获取每个章节标题
        chapter_title = html.xpath('//*[@id="c1"]/h1/text()')
        # print(chapter_title)
        text = html.xpath('//*[@id="content"]/p/text()')
        # print(text)
        # a+ 文件存在则在文件后面追加，不存在则创建文件并追加。若不想重复获取，需保证此文件夹中没有该文件
        with open(title + '+' + author + '.txt', 'a+', encoding='gbk') as f:
            # 将类型转换为字符串类型写入
            chapter_title = str(chapter_title[0])
            # 把每个章节的标题写入
            f.write(chapter_title + '\n')
            # 写入正文
            for character in text:
                # 将类型转换为字符串类型写入
                j = str(character)
                f.write(j + '\n')                   # '\n'换行处理
            f.write('\n')
            # 每个章节之间空一行

    # 结果获取完后输出获取完成
    print('获取完成，已经获取全部的章节内容')

    # 每获得一本小说就将小说名称和url写入文本中
    with open('不同小说的url.txt', 'a+', encoding='utf-8') as f:
        f.write(title + '+' + author + '         ' + url)
        f.write('\n')


if __name__ == '__main__':
    start_time = time.time()
    get_info()
    end_time = time.time()
    total_time = end_time - start_time
    print('获取内容共耗时%.2f秒' % total_time)
