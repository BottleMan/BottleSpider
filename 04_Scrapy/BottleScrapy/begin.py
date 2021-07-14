import os

from scrapy import cmdline


def start_spider(debug):
    # 设置启动参数
    # cmd = 'scrapy crawl news163 '
    cmd = 'scrapy crawl epaper_rmrb '
    # 启动爬虫
    if debug:
        cmdline.execute(cmd.split())
    else:
        os.system(cmd)


if __name__ == '__main__':
    start_spider(debug=True)
