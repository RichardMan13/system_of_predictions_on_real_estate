import scrapy
from ..items import RealEstateItem
from scrapy.loader import ItemLoader

class AtivaSpider(scrapy.Spider):
    name = 'ativa'
    allowed_domains = ['www.imobiliariaativa.com.br']
    page_number = 1
    start_urls = [
        'https://www.imobiliariaativa.com.br/pesquisa-de-imoveis/?locacao_venda=V&id_cidade%5B%5D=37&id_tipo_imovel%5B%5D=8&id_tipo_imovel%5B%5D=12&finalidade=residencial&dormitorio=0&garagem=0&vmi=&vma=&&pag='
        ]

    def parse(self, response):

        links = response.css('.owl-carousel.owl-theme .item:nth-child(1) a::attr(href)').extract()

        for link in links:
            if link is not None:
                next_link = 'https://www.imobiliariaativa.com.br/'+link
                # response.follow(next_link, callback=self.extract_info)
                yield scrapy.Request(url=next_link, callback=self.extract_info)

        AtivaSpider.page_number += 1
        next_page = AtivaSpider.start_urls[0]+str(AtivaSpider.page_number)
        
        if AtivaSpider.page_number <= 71:
            yield scrapy.Request(url=next_page, callback=self.parse)
               

    def extract_info(self, response):
        
        loader = ItemLoader(item=RealEstateItem(), response=response)
        
        price = response.css('.col-lg-6.col-sm-6.text-right strong::text').extract()
        # price = response.css('.row:nth-child(10) strong::text').extract_first()

        #If there is no price none should be scrap!
        if price:
            price = float(price[-1].split(',')[0].replace('.', ''))
        else:
            return
    
        title = response.css('.property-title a::text').extract()
        type = title[0]
        neighborhood = title[2]
        
        rooms = self.get_item_with_xpath(response=response, xpath='//div[contains(.,"Dorm")]/br/following-sibling::text()', cast='int')
        suites = self.get_item_with_xpath(response=response, xpath='//div[contains(.,"Suíte")]/br/following-sibling::text()', cast='int')
        bathrooms = self.get_item_with_xpath(response=response, xpath='//div[contains(.,"Banhei")]/br/following-sibling::text()', cast='int')
        garages = self.get_item_with_xpath(response=response, xpath='//div[contains(.,"Garage")]/br/following-sibling::text()', cast='int')

        total_area = self.get_item_with_xpath(response=response, xpath='//div[contains(.,"A. Terreno")]/br/following-sibling::text()', cast='float')
        if total_area == 0:
            total_area = self.get_item_with_xpath(response=response, xpath='//div[contains(.,"A. Total")]/br/following-sibling::text()', cast='float')

        private_area = self.get_item_with_xpath(response=response, xpath='//div[contains(.,"A. Construída")]/br/following-sibling::text()', cast='float')
        if private_area == 0:
            private_area = self.get_item_with_xpath(response=response, xpath='//div[contains(.,"A. Útil")]/br/following-sibling::text()', cast='float')

        loader.add_value('price', price)
        loader.add_value('neighborhood', neighborhood)
        loader.add_value('type', type)
        loader.add_value('rooms', rooms)
        loader.add_value('suites', suites)
        loader.add_value('bathrooms', bathrooms)
        loader.add_value('garages', garages)
        loader.add_value('total_area', total_area)
        loader.add_value('private_area', private_area)

        yield loader.load_item()
    
    def get_item_with_xpath(self, response, xpath, cast):

        item = response.xpath(xpath).extract_first()

        if not item:
            item = 0

        else:
            item = item.strip()

            if item and cast=='int':
                item = int(item)

            elif item and cast=='float':
                item = float(item[:-3])

            else:
                item = 0

        return item