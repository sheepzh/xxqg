import requests


def url2html(url):
    """
      获取url地址的html内容，并以字符串返回
    """
    html = requests.get(url)
    html.encoding = 'utf-8'
    return html.text
