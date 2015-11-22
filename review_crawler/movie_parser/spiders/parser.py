## Run with Python2

from scrapy.spider   import BaseSpider
from scrapy.selector import Selector
from scrapy.item     import Item, Field

class MovieItem(Item):
	title  = Field()
	id     = Field()
	rating = Field()
	review = Field()


class MovieSpider(BaseSpider):
	name = "movie"
	allowed_domians = ['movie.naver.com'] 
	start_urls = ['http://movie.naver.com/movie/point/af/list.nhn?st=mcode&sword=106547&target=after&page=%d' % i for i in xrange(740)]

	def parse(self, response):
		sel = Selector(response)
		sites = sel.xpath("//table[@class='list_netizen']/tbody/tr")

		items = []

		item = MovieItem()
		item['title']  = sites.xpath("td[@class='title']/a[@class='movie']/text()").extract()
		item['rating'] = sites.xpath("td[@class='point']/text()").extract()
		
		text   = sites.xpath("td[@class='title']").extract()
		review = [ t.split('<br>')[1].split(' \r')[0] for t in text ]
		item['review'] = review
		items.append(item)

		return items
