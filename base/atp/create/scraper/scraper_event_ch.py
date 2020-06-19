from lxml import html 
import requests
import time
import os 
os.chdir('/home/landfried/gaming/trabajos/tenis/db/atpworldtour/scraper')

file = open('../html/event_challenger.txt', 'r')
htmls_names = file.read().splitlines()
htmls_names.sort(key = lambda x: (x.split("/")[-2],x.split("/")[-4]) )
len(htmls_names )

count_s=2796; count_d=1280
for url in htmls_names[2870:]:# url = htmls_names[2870]
    url_s = "http://www.atpworldtour.com/"+url+"?matchType=singles"
    page = requests.get(url_s)
    print(url.split("/")[4], url.split("/")[5], url.split("/")[6])
    if str(page)  != '<Response [404]>':
        tree = html.fromstring(page.text)
        results_table = tree.xpath("//div[@id='scoresResultsContent']")    
        if len(results_table) > 0:
            namefile = "../html/event_ch/{}_{}_{}_{}.html".format(url.split("/")[4], url.split("/")[5], url.split("/")[6], "singles")
            html_file = open(namefile, 'w')
            html_file.write(page.text)
            html_file.close()
            count_s+=1; print("singles", count_s)
    time.sleep(1.1)    
    url_d = "http://www.atpworldtour.com/"+url+"?matchType=doubles"
    page = requests.get(url_d)
    if str(page)  != '<Response [404]>':   
        tree = html.fromstring(page.text)
        results_table = tree.xpath("//div[@id='scoresResultsContent']")    
        if len(results_table) > 0:
            namefile = "../html/event_ch/{}_{}_{}_{}.html".format(url.split("/")[4], url.split("/")[5], url.split("/")[6], "doubles")
            html_file = open(namefile, 'w')
            html_file.write(page.text)
            html_file.close()
            count_d+=1;print("doubles", count_d) 
    time.sleep(1.1)
    
