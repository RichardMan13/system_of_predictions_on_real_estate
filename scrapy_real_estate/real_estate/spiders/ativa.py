import scrapy
from ..items import RealEstateItem

class AtivaSpider(scrapy.Spider):
    name = 'ativa'
    allowed_domains = ['www.imobiliariaativa.com.br']
    start_urls = [
        'https://www.imobiliariaativa.com.br/pesquisa-de-imoveis/?locacao_venda=V&id_cidade%5B%5D=37&id_tipo_imovel%5B%5D=8&id_tipo_imovel%5B%5D=12&finalidade=residencial&dormitorio=0&garagem=0&vmi=&vma='
        ]

    def parse(self, response):
        
        items = RealEstateItem()

        #caixa com o link -#property-listing .col-lg-3
        # a href link para o imovel
        # .owl-item:nth-child(1) a::attr(href)
        #property-listing .col-lg-3 a::attr(href)
        #property-listing .col-lg-3:nth-child(1) a::attr(href)
        # '.col-lg-3 .item a::attr(href)' funciona com o set <<<<<
        # '.col-lg-3 .imagem-imovel .owl-wrapper .item a::attr(href)'

        

