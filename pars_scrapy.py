import scrapy


class IMDbSpyder(scrapy.Spider):
    name = 'imdb_spyder'
    start_urls = ['https://www.imdb.com/search/title/?country_of_origin=ru&page=1&ref_=adv_prv']

    def parse(self, response):
        SET_SELECTOR = '//div[@class="lister-item mode-advanced"]'
        for i in response.xpath(SET_SELECTOR):
            yield {
                'title': i.xpath('.//h3/a/text()').extract_first(),
                'year': i.xpath('.//h3/span[@class="lister-item-year text-muted unbold"]/text()').extract_first(),
                'rating': i.xpath('.//div[@class="inline-block ratings-imdb-rating"]/strong/text()').extract_first(),
                'length_of_film': i.css('div.lister-item-content p.text-muted span.runtime::text').extract_first(),
                'genre': i.css('div.lister-item-content p.text-muted span.genre::text').extract_first(),
                'gross': i.css('div.lister-item-content p.sort-num_votes-visible span.ghost+span.text-muted+span::text').extract_first(),
            }
        NEXT_PAGE = 'div#main div.article div.sub-list div.nav div.desc a.next-page::attr(href)'
        next_page = response.css(NEXT_PAGE).extract_first()
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page), callback=self.parse
            )
