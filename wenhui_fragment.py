import os

import scrapy
from common import url2html

TARGET_FILE_ROOT = './wenhui/'

TITLE_FILE_PATH = TARGET_FILE_ROOT + '/title_urls.txt'

FILE_PATH = TARGET_FILE_ROOT + '/fragment.txt'


class BlogSpider(scrapy.Spider):

    custom_settings = {
        'LOG_LEVEL': 'WARNING',
        'DEFAULT_REQUEST_HEADERS': {
            "User-Agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
        }
    }

    name = 'wenhui_fragment'

    # 文件夹初始化
    if not os.path.exists(TARGET_FILE_ROOT):
        os.makedirs(TARGET_FILE_ROOT)

    if not os.path.exists(TITLE_FILE_PATH):
        print("no title exists")
        quit()

    module_file = open(TITLE_FILE_PATH, 'r')
    start_urls = module_file.readlines()
    # start_urls = [
    #     'http://gjzx.jschina.com.cn/20633/xjpwjsx/wh/hlwxcgz/201907/t20190711_6258936.shtml']
    module_file.close()

    # 删除旧的url
    if os.path.exists(FILE_PATH):
        os.remove(FILE_PATH)

    def parse(self, response):
        print(response.url)
        fragments = response.selector.xpath(
            '//div[@class="mleft"]//div[@class="article"]//div[@class="TRS_Editor"]/p//text()').getall()

        move = dict.fromkeys((ord(c) for c in u"\xa0\n\t\u3000"))
        sentences = list(map(lambda f: f.translate(move), fragments))
        sentences = list(filter(lambda s: len(s) != 0, sentences))
        # 升维度
        digit_2 = []
        temp = []
        for sentence in sentences:
            if sentence.startswith('VW') and len(temp) > 0:
                digit_2.append(temp)
                temp = []
            temp.append(sentence)
        # print(digit_2)
        if len(temp) > 0:
            digit_2.append(temp)
        file = open(FILE_PATH, 'a')
        for group in digit_2:
            file.write(str(group))
            file.write('\n')
        file.close()
