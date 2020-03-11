import os

import scrapy
from common import url2html

TARGET_FILE_ROOT = './wenhui/'

FILE_PATH = TARGET_FILE_ROOT + '/module_urls.txt'


class BlogSpider(scrapy.Spider):

    custom_settings = {
        'LOG_LEVEL': 'WARNING',
        'DEFAULT_REQUEST_HEADERS': {
            "User-Agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
        }
    }

    name = 'wenhui_module'
    start_urls = ['http://gjzx.jschina.com.cn/20633/xjpwjsx/wh/']
    start_urls.extend(
        list(map(lambda i: 'http://gjzx.jschina.com.cn/20633/xjpwjsx/wh/index_%d.shtml' % (i), range(1, 6)))
    )

    # 文件夹初始化
    if not os.path.exists(TARGET_FILE_ROOT):
        os.makedirs(TARGET_FILE_ROOT)
    if os.path.exists(FILE_PATH):
        os.remove(FILE_PATH)

    def parse(self, response):
        titles = response.selector.xpath(
            '//div[@class="mleft"]//div[@class="biaot"]/a')

        file = open(FILE_PATH, 'a')
        for t_a in titles:
            url = t_a.attrib['href']
            print(url)
            file.write(url)
            file.write('\n')
        file.close()
