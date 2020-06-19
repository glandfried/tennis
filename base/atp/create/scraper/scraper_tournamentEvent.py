from lxml import html 
import requests
import time

file = open('../html/tournament/info.txt', 'r')
htmls_names = file.read().splitlines()

for html_name in htmls_names:
	for year in list(range(2017, 1914, -1)):#year=2017
		tournament_name = html_name.split("_")[0]
		tournament_number = html_name.split("_")[1].split(".html")[0]
		url_s = "http://www.atpworldtour.com/en/scores/archive/{}/{}/{}/results?matchType=singles".format(tournament_name ,tournament_number,year)
		url_d = "http://www.atpworldtour.com/en/scores/archive/{}/{}/{}/results?matchType=doubles".format(tournament_name ,tournament_number,year)
		
		page = requests.get(url_s)
		tree = html.fromstring(page.text)
		title_404 = len(tree.xpath("//div[@class='title-box-404']"))>0
		if not title_404:
			namefile = "../html/tournamentEvent/{}_{}_{}_singles.html".format(tournament_name,tournament_number,year) 
			html_file = open(namefile, 'w')
			html_file.write(page.text)
			html_file.close()
			print(tournament_name,tournament_number,year,"single")
		
		time.sleep(1.1)
		
		page = requests.get(url_d)
		tree = html.fromstring(page.text)
		title_404 = len(tree.xpath("//div[@class='title-box-404']"))>0
		if not title_404:	
			namefile = "../html/tournamentEvent/{}_{}_{}_doubles.html".format(tournament_name,tournament_number,year) 
			html_file = open(namefile, 'w')
			html_file.write(page.text)
			html_file.close()
			print(tournament_name,tournament_number,year,"double")
		
		time.sleep(1.1)