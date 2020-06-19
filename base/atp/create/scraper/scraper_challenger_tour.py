from lxml import html

import pandas as pd

import requests
import socket
import psycopg2
from time import sleep

#import os 
#os.chdir('/home/landfried/gaming/trabajos/tenis/db/atpworldtour/scraper')

png = open("/home/landfried/gaming/aux/k.png", "r") 
k = png.read()
if socket.gethostname() == "mininet-vm":		
    con = psycopg2.connect(database='tenis', user='glandfried', password=k[:-1])
    c = con.cursor()
else:
    con = psycopg2.connect(database='tenis', user='glandfried', password=k[:-1], host='mininet.exp.dc.uba.ar', port='5432')
    c = con.cursor()
    
query="""  
    select tournament_id, tournament_name
    from tournament
    """
c.execute(query) 
#con.rollback()    
t_id = c.fetchall()
atp = set(map(lambda x: x[0], t_id))

tournaments_id = set(); tour_id_name = set()
for year in range(1976,2018):
    url = "http://www.atpworldtour.com/en/scores/results-archive?year={}&tournamentType=ch".format(year) 
    page = requests.get(url)
    tree = html.fromstring(page.text)
    tournaments_url = tree.xpath("//td[@class='tourney-details']/a/@href")       
    tournaments_id.update(map(lambda x: int(x.split('/')[x.split('/').index('archive')+2]), tournaments_url ))
    tour_id_name.update(map(lambda x: (int(x.split('/')[x.split('/').index('archive')+2]), x.split('/')[x.split('/').index('archive')+1]), tournaments_url ))
    sleep(0.5)
#len(tournaments_id )


tournaments_id = set(); tour_atp = set()
for year in range(1915,2018):
    url = "http://www.atpworldtour.com/en/scores/results-archive?year={}&tournamentType=atp".format(year) 
    page = requests.get(url)
    tree = html.fromstring(page.text)
    tournaments_url = tree.xpath("//td[@class='tourney-details']/a/@href")       
    tournaments_id.update(map(lambda x: int(x.split('/')[x.split('/').index('archive')+2]), tournaments_url ))
    tour_atp.update(map(lambda x: (int(x.split('/')[x.split('/').index('archive')+2]), x.split('/')[x.split('/').index('archive')+1]), tournaments_url ))
    sleep(0.5)


interseccion = len(tour_atp.intersection(tour_id_name ))
print("La intersecci\'on en torneos challenger y atp es de {}".format(interseccion ))

tours = tour_atp.union(tour_id_name )
file = open('../html/tours.txt', 'w')
for id_, name_ in tours:
    file.write("{},{}\n".format(id_, name_ ))
file.close()

#pd.read_csv('../html/tours.txt')

event_challenger = set()
for year in range(1915,2019):
    url = "http://www.atpworldtour.com/en/scores/results-archive?year={}&tournamentType=ch".format(year)
    page = requests.get(url)
    tree = html.fromstring(page.text)
    tournaments_url = tree.xpath("//td[@class='tourney-details']/a/@href")       
    event_challenger.update(filter(lambda x: 'scores' in x.split("/") and  'archive' in x.split("/") and 'results' in x.split("/"),tournaments_url ))
    time.sleep(1)
len(event_challenger)
event_challenger_sorted = list(event_challenger)
#event_challenger_sorted .sort(key = lambda x: (x.split("/")[-2],x.split("/")[-4]) )
#event_challenger_sorted[0] 


file = open('../html/event_challenger.txt', 'w')
for url in event_challenger:
    file.write("{}\n".format(url))
file.close()

event= set()
for year in range(1915,2019):
    url = "http://www.atpworldtour.com/en/scores/results-archive?year={}".format(year)
    page = requests.get(url)
    tree = html.fromstring(page.text)
    tournaments_url = tree.xpath("//td[@class='tourney-details']/a/@href")       
    event.update(filter(lambda x: 'scores' in x.split("/") and  'archive' in x.split("/") and 'results' in x.split("/"),tournaments_url ))
    #event_challenger_doubles.update(filter(lambda x: 'scores' in x.split("/") and  'archive' in x.split("/") and 'results?matchType=doubles' in x.split("/"),tournaments_url ))    
    sleep(0.5)
len(event)
event_sorted = list(event)
event_sorted.sort(key = lambda x: (x.split("/")[-2],x.split("/")[-4]) )

file = open('../html/event_atp.txt', 'w')
for url in event_sorted :
    file.write("{}\n".format(url))
file.close()

apunte_selenium = """
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

os.environ['PATH'] = os.getenv('PATH') + ':/usr/lib/chromium-browser'
driver = webdriver.Chrome()

singles = set(); doubles = set()
for id_, name_ in tours:# id_, name_ = list(tours)[0]
    url = "http://www.atpworldtour.com/en/tournaments/{}/{}/overview".format(name_, id_)
    page = requests.get(url)
    if str(page) == '<Response [404]>':
        print(str(page))
        print(id_, name_, len(singles), len(doubles)) 
    else:
        driver.get(url) 
        delay = 20 # seconds
        try:
            myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'tourneyOverviewTabs')))
            # Singles        
            try:
                tree = html.fromstring(driver.find_element_by_id('pastResultsSinglesPlaceholder').get_attribute('innerHTML'))
                href_singles = tree.xpath("//a/@href")
                singles.update(filter(lambda x: 'scores' in x.split("/") and  'archive' in x.split("/") and 'results?matchType=singles' in x.split("/"),href_singles))
            except:
                pass
            # Doubles
            try:
                tree = html.fromstring(driver.find_element_by_id('pastResultsDoublesPlaceholder').get_attribute('innerHTML'))
                href_doubles = tree.xpath("//a/@href")
                doubles.update(filter(lambda x: 'scores' in x.split("/") and  'archive' in x.split("/") and 'results?matchType=doubles' in x.split("/"),href_doubles))
            except:
                pass
            print("Page is ready!")
        except TimeoutException:
            print("Loading took too much time!")
        print(id_, name_, len(singles), len(doubles)) 

"""

