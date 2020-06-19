from lxml import html
#import pandas as pd
#import numpy as np
import requests
import updater as up
#from importlib import reload  # Python 3.4+ only.
#reload(up)
from time import sleep
#import os
#os.chdir('/home/landfried/gaming/trabajos/tenis/db/atpworldtour/scraper')
#os.chdir('/home/amaya-botello/gaming/bases/tenis/create/atpworldtour/scraper')
import socket
import psycopg2
import sys
last_events = 0
if len(sys.argv)>1: last_events = int(sys.argv[1])

db_active = True
if socket.gethostname() == "mininet-vm":		
    con = psycopg2.connect(database='tenis', user='glandfried', password="caimancito")
    c = con.cursor()
else:
    con = psycopg2.connect(database='tenis', user='glandfried', password="caimancito", 
    host='mininet.exp.dc.uba.ar', port='5432')
    c = con.cursor()

###########################
##### Challenger###########
challenger = True

url = "http://www.atpworldtour.com/en/scores/results-archive?year=2020&tournamentType=ch"
page = requests.get(url)
tree = html.fromstring(page.text)
tournaments_url = tree.xpath("//td[@class='tourney-details']/a/@href")

for tour_url in tournaments_url[-last_events:]:#tour_url = tournaments_url[45]; len(tournaments_url)
        double = False
        url = "http://www.atpworldtour.com"+'/'.join(tour_url.split("/")[:-1])+'/results'
        page = requests.get(url); tree = html.fromstring(page.text)
        up.update(c, con, url, tree, double, challenger, db_active)        
        #
        sleep(0.1)
        double = True
        url = url + '?matchType=doubles' 
        page = requests.get(url); tree = html.fromstring(page.text)
        if len(tree.xpath("//div[@class='title-box-404']"))==0: 
            up.update(c, con, url, tree, double, challenger, db_active)        
        sleep(0.1)
            
###########################
##### ATP #################
challenger = False

url = "http://www.atpworldtour.com/en/scores/results-archive?year=2020"
page = requests.get(url)
tree = html.fromstring(page.text)
tournaments_url = tree.xpath("//td[@class='tourney-details']/a/@href")

for tour_url in tournaments_url[-last_events:]:#tour_url = tournaments_url[-1]
        double = False       
        url = "http://www.atpworldtour.com"+'/'.join(tour_url.split("/")[:-1])+'/results'
        page = requests.get(url); tree = html.fromstring(page.text)
        up.update(c, con, url, tree, double, challenger, db_active)        
        #        
        sleep(0.1)
        double = True
        url = url + '?matchType=doubles' 
        page = requests.get(url);  tree = html.fromstring(page.text)
        if len(tree.xpath("//div[@class='title-box-404']"))==0: 
            up.update(c, con, url, tree, double, challenger, db_active)        
        sleep(0.1)
            