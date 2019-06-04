import scrapy

from imdbDataset.items import ImdbdatasetItem

class imdbspider(scrapy.Spider):
	name="imdbspider"

	start_urls=["https://www.imdb.com/search/title?genres=comedy&explore=title_type,genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=3396781f-d87f-4fac-8694-c56ce6f490fe&pf_rd_r=8ESMS9M0HMBQ5EWTM96M&pf_rd_s=center-1&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_pr1_i_1"]



	

	def target_page(self,response):


		items=ImdbdatasetItem()
		items['title']="".join(response.xpath('//div/div[@class="title_wrapper"]//h1//text()').extract()).replace("\xa0","")
		items['certification']="".join(response.xpath('//div/div[@class="title_wrapper"]//div[@class="subtext"]/text()').extract_first()).strip()
		items['duration']="".join(response.xpath('//div/div[@class="title_wrapper"]//time/text()').extract()).strip()
		items['genres']=",".join(response.xpath('//div/div[@class="title_wrapper"]//a[contains(@href,"genres=")]//text()').extract())
		items['releaseDate']="".join(response.xpath('//div/div[@class="title_wrapper"]//a[contains(@href,"releaseinfo")]//text()').extract()).strip() 
		items['summary']= "".join(response.xpath('//*[contains(concat(" ", @class, " "), " summary_text ")]//text()').extract()).strip()
		items['stars']=",".join(response.xpath('//div[contains(h4/text(),"Stars")]//a[starts-with(@href,"/name")]/text()').extract())
		items['primaryLanguage']=",".join(response.xpath('//div//a[contains(@href,"primary_language")]//text()').extract()) 
		  
		yield items 
		
	def parse(self,response):

		pageList=response.xpath('//div/div/h3/a/@href').extract()
		for i in pageList:
			yield scrapy.Request(response.urljoin(i), callback=self.target_page)

		nextpageLink= "".join(response.xpath('//div[@class="article"]/div[@class="desc"]/a[contains(text(),"Next")]/@href').extract()) 
		
		if nextpageLink:
		 	yield scrapy.Request(response.urljoin(nextpageLink), callback=self.parse)




    