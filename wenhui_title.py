import os

import scrapy
from common import url2html

TARGET_FILE_ROOT = './wenhui/'

MODULE_FILE_PATH = TARGET_FILE_ROOT + '/module_urls.txt'

FILE_PATH = TARGET_FILE_ROOT + '/title_urls.txt'


class BlogSpider(scrapy.Spider):

    custom_settings = {
        'LOG_LEVEL': 'WARNING',
        'DEFAULT_REQUEST_HEADERS': {
            "User-Agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
        }
    }

    name = 'wenhui_title'

    # 文件夹初始化
    if not os.path.exists(TARGET_FILE_ROOT):
        os.makedirs(TARGET_FILE_ROOT)

    if not os.path.exists(MODULE_FILE_PATH):
        print("no module exists")
        quit()

    module_file = open(MODULE_FILE_PATH, 'r')
    start_urls = module_file.readlines()
    module_file.close()

    # 删除旧的url
    if os.path.exists(FILE_PATH):
        os.remove(FILE_PATH)

    def parse(self, response):
        url = response.url
        titles = response.selector.xpath(
            '//div[@class="mleft"]//div[@class="biaot"]/a')
        file = open(FILE_PATH, 'a')
        for t_a in titles:
            target_url = url + t_a.attrib['href'][2:]
            print(target_url)
            file.write(target_url)
            file.write('\n')
        file.close()
