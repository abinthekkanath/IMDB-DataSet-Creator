import requests
from lxml import html
from w3lib.html import remove_tags
import json

head="https://www.imdb.com"
count=0
pageCount=0

def targetPage(url):
	global count
	count=count+1
	print(182*'*') 
	print("Page URL:",url)
	print("Movie Count:",count)

	response=requests.get(url) 
	tree = html.fromstring(response.content)  

	title="".join(tree.xpath('//div/div[@class="title_wrapper"]//h1//text()')).replace("\xa0","") 
	certification=((("".join(tree.xpath('//div/div[@class="title_wrapper"]//div[@class="subtext"]/text()'))).replace("\n","")).replace("  ","")).replace(",","")   
	duration="".join(tree.xpath('//div/div[@class="title_wrapper"]//time/text()')).strip()
	genres=",".join(tree.xpath('//div/div[@class="title_wrapper"]//a[contains(@href,"genres=")]//text()')).strip() 
	releaseDate= ",".join(tree.xpath('//div/div[@class="title_wrapper"]//a[contains(@href,"releaseinfo")]//text()')).strip()   
	summary="".join(tree.xpath('//*[contains(concat(" ", @class, " "), " summary_text ")]/text()')).strip()
	stars= ",".join(tree.xpath('//div[contains(h4/text(),"Stars")]//a[starts-with(@href,"/name")]/text()')).strip().replace("\n","") 
	primaryLanguage=(",".join(tree.xpath('//div//a[contains(@href,"primary_language")]/text()')))

	print("Title:",title,"Certification:",certification,"Duration:",duration,"Genres:",genres,"Release Date:",releaseDate,"Summary:",summary,"Stars:",stars,"Primary Language:",primaryLanguage, sep="\n")
	print(182*'*') 

	imdbcomedy={"Title":title,"Certification":certification,"Duration":duration,"Genres":genres,"Release Date":releaseDate,"Summary":summary,"Stars":stars,"Primary Language":primaryLanguage}
	with open('imdb-dataset.json', 'a+') as f:
		json.dump(imdbcomedy, f, indent=2, ensure_ascii=False)

def nextPage(url):

	global pageCount
	pageCount=pageCount+1
	print(46*'/**/')  
	print("Block URL:",url)
	print("Block Count:",pageCount)

	response=requests.get(url) 
	tree = html.fromstring(response.content)

	pageList=tree.xpath('//div/div/h3/a/@href')
	for i in pageList:
		par=head+i
		print(par)
		targetPage(par)


	print(46*'/**/')

	nexturl="".join(tree.xpath('//div[@class="article"]/div[@class="desc"]/a[contains(text(),"Next")]/@href'))
	if nexturl :
		par=head+nexturl
		print(par)
		nextPage(par)


print("Welcome to IMDB DataSet Creator\n Choose the Genres:\n")
response=requests.get('https://www.imdb.com/feature/genre/?ref_=nv_ch_gr')
tree = html.fromstring(response.content)
generList=tree.xpath('//img/@title')
generListurls=tree.xpath('//div[@class="image"]/a/@href') 
for i in generList:
	print(generList.index(i),i)

ch=int(input()) 
nextPage(generListurls[ch])
