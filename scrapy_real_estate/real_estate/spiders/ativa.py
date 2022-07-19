import scrapy
from ..items import RealEstateItem
from scrapy.loader import ItemLoader

class AtivaSpider(scrapy.Spider):
    name = 'ativa'
    allowed_domains = ['www.imobiliariaativa.com.br']
    page_number = 1
    start_urls = [
        'https://www.imobiliariaativa.com.br/pesquisa-de-imoveis/?locacao_venda=V&id_cidade%5B%5D=37&id_tipo_imovel%5B%5D=8&id_tipo_imovel%5B%5D=12&finalidade=residencial&dormitorio=0&garagem=0&vmi=&vma='
        ]

    def parse(self, response):

        links = response.css('.owl-carousel.owl-theme .item:nth-child(1) a::attr(href)').extract()

        for link in links:
            if link is not None:
                next_link = 'https://www.imobiliariaativa.com.br/'+link
                # response.follow(next_link, callback=self.extract_info)
                yield scrapy.Request(url=next_link, callback=self.extract_info)

        # page_number += 1
        # next_page = 'https://www.imobiliariaativa.com.br/pesquisa-de-imoveis/?locacao_venda=V&id_cidade%5B%5D=37&id_tipo_imovel%5B%5D=8&id_tipo_imovel%5B%5D=12&finalidade=residencial&dormitorio=0&garagem=0&vmi=&vma=&&pag='+page_number

        # yield scrapy.Request(url=next_page, callback=self.parse)
               

    def extract_info(self, response):
        
        loader = ItemLoader(item=RealEstateItem(), response=response)

        title = response.css('.property-title a::text').extract()
        type = title[0]
        neighborhood = title[2]
        
        rooms = response.xpath('//div[contains(.,"Dorm")]/br/following-sibling::text()').extract_first().strip()

        suites = response.xpath('//div[contains(.,"Suíte")]/br/following-sibling::text()').extract_first()
        if not suites:
            suites = 0
        else:
            suites = suites.strip()

        bathrooms = response.xpath('//div[contains(.,"Banheiros")]/br/following-sibling::text()').extract_first().strip()
        garages = response.xpath('//div[contains(.,"Garage")]/br/following-sibling::text()').extract_first().strip()

        total_area = response.xpath('//div[contains(.,"A. Terreno")]/br/following-sibling::text()').extract_first()
        if not total_area:
            total_area = response.xpath('//div[contains(.,"A. Total")]/br/following-sibling::text()').extract_first()
   
        total_area = total_area.strip()

        private_area = response.xpath('//div[contains(.,"A. Construída")]/br/following-sibling::text()').extract_first()
        if not private_area:
            private_area = response.xpath('//div[contains(.,"A. Útil")]/br/following-sibling::text()').extract_first()
        
        private_area = private_area.strip()

        loader.add_value('neighborhood', neighborhood)
        loader.add_value('type', type)
        loader.add_value('rooms', rooms)
        loader.add_value('suites', suites)
        loader.add_value('bathrooms', bathrooms)
        loader.add_value('garages', garages)
        loader.add_value('total_area', total_area)
        loader.add_value('private_area', private_area)

        yield loader.load_item()