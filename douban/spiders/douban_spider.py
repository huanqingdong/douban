# -*- coding: utf-8 -*-
import scrapy,threading
from douban.items import DoubanItem


class DoubanSpiderSpider(scrapy.Spider):
    # 爬虫名
    name = 'douban_spider'
    # 允许的域名
    allowed_domains = ['cdjdm.com']
    # 入口url
    # start_urls = ['https://movie.douban.com/top250']
    start_urls = ['http://www.cdjdm.com/html/part/index49.html']
    root = "D://python1//sw//"
    base_path = "http://www.cdjdm.com"

    def parse(self, response):
        url_list = response.xpath("//div[@class='box list channel']/ul/li/a/@href").extract()
        for i_url in url_list:
            # i_url = i_url[0]
            print(i_url)
            if i_url:
                yield scrapy.Request(self.base_path + i_url, callback=self.parsePics)
            # douban_item = DoubanItem();
            # douban_item['serial_number'] = i_item.xpath(".//div[@class='pic']/em").extract_first()
            # douban_item['movie_name'] = i_item.xpath(
            #     ".//div[@class='info']//div[@class='hd']/a/span[1]/text()").extract_first()
            # douban_item['movie_pic'] = i_item.xpath(".//div[@class='pic']//img/@src").extract_first()
            # # print(douban_item)
            # movie_pic = i_item.xpath(".//div[@class='pic']//img/@src").extract_first()
            #
            # path = DoubanSpiderSpider.root + movie_pic.split("/")[-1]
            # print(path)
            # self.urllib_download(movie_pic, path)
            # yield douban_item
        next_link = response.xpath(
            "//div[@class='box list channel']/div[@class='pagination']/a[contains(text(), '下一页')]/@href").extract()
        if next_link:
            next_link = next_link[0]
            yield scrapy.Request(self.base_path + next_link, callback=self.parse)

    def parsePics(self, response):
        # 解析标题,创建目录
        pic_title = response.xpath("//div[@class='box pic_text']/div[@class='page_title']/text()").extract_first()
        path = DoubanSpiderSpider.root + pic_title + "//"
        self.mkdir(path)

        # 解析图片,进行下载
        pic_list = response.xpath("//div[@class='content']/img/@src").extract()
        for i_pic in pic_list:
            pic_name = i_pic.split("/")[-1]
            #self.urllib_download(i_pic, path+ pic_name)
            threading.Thread(target=self.urllib_download, args=(i_pic,  path+ pic_name)).start()

    def urllib_download(self, url, path):
        from urllib.request import urlretrieve,build_opener,install_opener
        opener = build_opener()
        opener.addheaders = [('User-agent',
                              'Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10')]
        install_opener(opener)
        print('线程:', threading.current_thread().name, "下载文件:", url)
        urlretrieve(url, path)

    def mkdir(self, path):
        # 引入模块
        import os
        # 去除首位空格
        path = path.strip()
        # 去除尾部 \ 符号
        path = path.rstrip("\\")
        # 判断路径是否存在 存在     True 不存在   False
        isExists = os.path.exists(path)

        # 判断结果
        if not isExists:
            # 如果不存在则创建目录
            # 创建目录操作函数
            os.makedirs(path)
            print(path + ' 创建成功')
            return True
        else:
            # 如果目录存在则不创建，并提示目录已存在
            print(path + ' 目录已存在')
            return False

