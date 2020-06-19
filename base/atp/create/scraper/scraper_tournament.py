from lxml import html 
import requests
import time
#import os 
#os.chdir('/home/landfried/gaming/trabajos/tenis/db/atpworldtour/scraper')

url = "http://www.atpworldtour.com/en/tournaments" 
page = requests.get(url)
tree = html.fromstring(page.text)
tournaments_url = tree.xpath("//div[@id='filterHolder']/div/div/div/div/ul/li/a/@href")
file = open('../html/tournament/urls.txt', 'w')
for t_url in tournaments_url:
	file.write("%s\n" % t_url)
file.close()

for t_url in tournaments_url:#t_url = tournaments_url[0]   
	page = requests.get("http://www.atpworldtour.com/".format(t_url))
	lugar_numero = t_url.split("/en/tournaments/")[1].split("/overview")[0]
	lugar = lugar_numero.split("/")[0]
	numero = lugar_numero.split("/")[1]
	namefile = "../html/tournament/{}_{}.html".format(lugar,numero) 
	html_file = open(namefile, 'w')
	html_file.write(page.text)
	html_file.close()
	print(lugar,numero)
	time.sleep(2)
