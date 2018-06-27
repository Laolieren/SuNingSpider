# -*- coding: utf-8 -*-
import scrapy
from SuningSpider.items import SuningspiderItem
import re


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["suning.com"]
    start_urls = ['http://snbook.suning.com/web/trd-fl/999999/0.htm']

    def parse(self, response):
        type_list = response.xpath("//ul[@class='ulwrap']/li")
        for type in type_list:
            item = SuningspiderItem()
            item['title'] = type.xpath("./div[1]/a/text()").extract_first()
            type_detail_list = type.xpath("./div[2]/a")
            for type_detail in type_detail_list:
                item['detail_title'] = type_detail.xpath("./text()").extract_first()
                item['detail_title_url'] = type_detail.xpath("./@href").extract_first()
                if item["detail_title_url"] is not None:
                    item["detail_title_url"] = "http://snbook.suning.com/" + item["detail_title_url"]
                yield scrapy.Request(
                    item['detail_title_url'],
                    callback=self.book_list,
                    meta={'item': item}
                )


    def book_list(self, response):
        item = response.meta['item']
        book_detail_list = response.xpath("//div[@class='filtrate-books list-filtrate-books']/ul/li")
        for book_detail in book_detail_list:
            item['book_name'] = book_detail.xpath(".//div[@class='book-title']/a/@title").extract_first()
            item['book_info'] = book_detail.xpath(".//div[@class='book-descrip c6']/text()").extract_first()
            item['book_image'] = book_detail.xpath(".//div[@class='book-img']//img/@src").extract_first()
            item['book_author'] = book_detail.xpath(".//div[@class='book-author']/a/text()").extract_first()
            item['book_url'] = book_detail.xpath(".//div[@class='book-title']/a/@href").extract_first()
            yield scrapy.Request(
                item['book_url'],
                callback=self.book_detail,
                meta={'item': item}
            )
        pagecount = re.findall(r'var pagecount=(.*?);', response.body.decode()[0])
        current_page = re.findall(r'var currentPage=(.*?);', response.body.decode()[0])
        if current_page < pagecount:
            next_url = item['detail_title_url'] + '?pageNumber={}&sort=0'.format(current_page + 1)
            yield scrapy.Request(
                next_url,
                callback=self.book_list
            )

    def book_detail(self, response):
        item = response.meta['item']
        item["book_price"] = re.findall("\"bp\":'(.*?)',", response.body.decode())
        item["book_price"] = item["book_price"][0] if len(item["book_price"]) > 0 else None
        yield item
