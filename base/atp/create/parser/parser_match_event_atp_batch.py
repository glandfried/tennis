from lxml import html 
import os
import socket
import psycopg2
#import numpy as np
os.chdir('/home/landfried/gaming/trabajos/tenis/db/atpworldtour/parser')

event_ch_html = list(filter(lambda x: x.endswith(".html"), os.listdir("../html/event_atp/")))
event_ch_html.sort(key=lambda x: (x.split("_")[2], x.split("_")[0])) 

ronda_dict = {'Finals':1, 'Semi-Finals':2, 'Quarter-Finals':4, 'Round of 16': None, 'Round of 32': None, 'Round of 64': None, 'Round of 128': None, '1st Round Qualifying':None, '2nd Round Qualifying':None,'3rd Round Qualifying':None, 'Round Robin':None}

seed_dict = {'LL': "Lucky loser: a player who plays the qualifying round to enter an event, but loses in the final qualifying round , he then enters the main draw after the start of an event as a result of another player withdrawal due to illness or injury", 'Q': "Qualifier: is a player whose ranking is not high enough to permit direct entry in to a tournament and thus he has to play the qualifying round to enter the main draw.", 'WC': "Wild cards: allow direct entry in to events for players who are not ranked high enough to enter an event directly. The wild cards are given by the authorities mainly to 3 kind of players, as under.", 'AL': None, "S": None, 'PR': None, 'SE': None  }

score_dict = {
'(RET)': "layer's withdrawal during a match, causing the player to forfeit the tournament. Usually this happens due to injury.", '(W/O)': "Unopposed victory. A walkover is awarded when the opponent fails to start the match for any reason, such as injury.",
'(DEF)': None,'(ABD)':None,'(ABN)':None,'(NA)':None,'(WEA)':None,'(UNP)':None
}

db_active = True
if db_active:                      
    png = open("/home/landfried/gaming/aux/k.png", "r") 
    k = png.read().strip("\n")
    if socket.gethostname() == "mininet-vm":		
        con = psycopg2.connect(database='tenis', user='glandfried', password=k)
        c = con.cursor()
    else:
        con = psycopg2.connect(database='tenis', user='glandfried', password=k, host='mininet.exp.dc.uba.ar', port='5432')
        c = con.cursor()                            

#singles=4202; #doubles=2686
challenger = False
event_count=0; match_count=0
for te_html in event_ch_html:# te_html  = event_ch_html[4150]
    
    #####
    # Tour
    tour_name = te_html.split("_")[0]
    tour_id = te_html.split("_")[1]
    #    
    query = "select * from tournament where tour_id = {}".format(tour_id)        
    c.execute(query);#con.rollback
    in_db = len(c.fetchall())>0
    if not in_db and db_active:
        c.execute("""insert into tournament (tour_id, tour_name) 
            values (%s, %s)""", (tour_id, tour_name) )
     
    #####
    # Read file
    file = open("../html/event_atp/{}".format(te_html), "r") 
    string = file.read()
    tree = html.fromstring(string)      

    #####
    # Event
    year = te_html.split("_")[2]
    double =  te_html.split(".html")[0].split('_')[-1] == 'doubles'      
    event_id = int(tour_id)*(10**5)+int(year)*(10)+(double)    
    timestamp = tree.xpath("//span[@class='tourney-dates']/text()")[0].strip(' \n\t')    
    if ' - ' in timestamp:
        time_start = timestamp.split(" - ")[0].replace('.', '-')
        time_end = timestamp.split(" - ")[1].replace('.', '-')
    else: 
        time_start = timestamp.replace('.', '-')
        time_end = None
    tour_details = tree.xpath("//td[@class='tourney-details']") 
    for td in tour_details:#td=tour_details[1]
        if len(td.xpath("./div/div[@class='icon-court image-icon']"))>0:
            ground = td.xpath("./div/div[@class='item-details']/span[@class='item-value']/text()")[0].strip(' \n\t')    
    # 
    query = "select * from event where event_id = {}".format(event_id)        
    c.execute(query);#con.rollback
    in_db = len(c.fetchall())>0
    if not in_db and db_active:
        c.execute("insert into event (event_id, tour_id, year, double, challenger, time_start , time_end, ground) values (%s,%s,%s,%s, %s,%s,%s,%s)", (event_id, tour_id, year, double, challenger, time_start, time_end, ground) )
        event_count+=1; print(event_count, te_html)    
        
        print(tuple([event_id, tour_id, year, double, ground]))

    #####
    # Players    
    s = 'overview'
    len(s[-7:])
    players_url = set(filter(lambda x: x[0:12]=='/en/players/' 
        and x[-9:] == '/overview', tree.xpath("//@href")))
    players = list(map(lambda x: tuple(x.split('en/players/')[1].split("/overview")[0].split("/")) , players_url))
    #
    for player_name, player_id in players:#player_name, player_id = players[0]
        query = "select * from player where player_id = '{}'".format(player_id)        
        c.execute(query);#con.rollback
        in_db = len(c.fetchall())>0
        if not in_db and db_active:
            c.execute("insert into player (player_id, player_name) values (%s, %s)", (player_id, player_name))    

    if db_active: con.commit();#con.rollback()            

    ######    
    # Match - sets
    ronda = tree.xpath("//div[@id='scoresResultsContent']/div/table/thead")
    partidas_en_ronda = tree.xpath("//div[@id='scoresResultsContent']/div/table/tbody")
    winner_player_2=None; looser_player_2=None; looser_seed=None; winner_seed=None; end_type=None
    for r in range(len(ronda)):#r=5
        round_number = r    
        round_name = ronda[r].xpath("./tr/th")[0].text
        matchs = partidas_en_ronda[r].xpath("./tr")        
        cantidad_partidas_ronda = len(matchs)
        for m in matchs:#m=matchs[0]
            seeds_element = m.xpath("./td[@class='day-table-seed']")
            if len(seeds_element[0].xpath("./span"))==1: 
                winner_seed =  seeds_element[0].xpath("./span")[0].text.strip(' \n\t').split("(")[1].split(")")[0]
            if len(seeds_element[1].xpath("./span"))==1: 
                looser_seed =  seeds_element[1].xpath("./span")[0].text.strip(' \n\t').split("(")[1].split(")")[0]            
            players_element = m.xpath("./td[@class='day-table-name']"); players =[]            
            winner_team_element = players_element[0].xpath("./a")
            winner_player_1 = winner_team_element[0].xpath("./@href")[0].split('en/players/')[1].split("/overview")[0].split("/")[1]
            if len(winner_team_element )==2:
                winner_player_2 = winner_team_element[1].xpath("./@href")[0].split('en/players/')[1].split("/overview")[0].split("/")[1]
            looser_team_element = players_element[1].xpath("./a")
            if len(looser_team_element)==0: 
                looser_player_1 = '0000' # bye
            else: 
                url = looser_team_element[0].xpath("./@href")[0]
                if url != '#': looser_player_1 = url.split('en/players/')[1].split("/overview")[0].split("/")[1]
                else: looser_player_1 = '0000'
            if len(looser_team_element )==2: 
                url = looser_team_element[1].xpath("./@href")[0]
                if url != '#': looser_player_2 = url.split('en/players/')[1].split("/overview")[0].split("/")[1]


            match_id=str(event_id)+str(round_number)+winner_player_1+looser_player_1 
            ## sets
            score_element = m.xpath("./td[@class='day-table-score']")[0]
            scores = []
            if len(score_element.xpath('./a'))==1 and len(score_element.xpath("./a")[0].text.strip(' \n\t'))>1:
                sets_texts = list(filter(lambda x: x != '' , map(lambda x: x.strip(' \n\t') ,score_element.xpath("./a/text()"))))
                #sup =  score_element.xpath("./a/sup/text()")                                
                desarmar = map(lambda x: x.split(' '),  sets_texts)              
                sets = [e for l in desarmar for e in l]
                win_alternative = sum(map(lambda x: x in score_dict.keys(), sets))>0
                end_type = "sets"
                for s in range(len(sets)):#s=0
                    if not sets[s] in score_dict.keys():
                        if '-' in sets[s]:
                            score_1 = int(sets[s].split('-')[0]); score_2 = int(sets[s].split('-')[1])
                            scores.append((score_1,score_2)); 
                        elif len(sets[s])%2==0:
                            score_1 = int(sets[s][0:len(sets[s])//2 ])
                            score_2 = int(sets[s][len(sets[s])//2 : len(sets[s])])
                            scores.append((score_1,score_2)); 
                        if len(sets[s])==3:
                            score_1_a = int(sets[s][0:1]); score_2_a = int(sets[s][1:3])
                            score_1_b = int(sets[s][0:2]); score_2_b = int(sets[s][2:3])
                            if abs(score_1_a-score_2_a)<abs(score_1_b-score_2_b):
                                scores.append((score_1_a,score_2_a))
                            else:
                                scores.append((score_1_b,score_2_b))
                    else: 
                        end_type = sets[s]    
                #if match['end_type'] == '(W/O)': wo +=1:
            # 
            if db_active:
                 query = "select * from match where match_id = '{}'".format(match_id)        
                 c.execute(query);#con.rollback
                 in_db = len(c.fetchall())>0
                 if not in_db and db_active:     
                    c.execute("""insert into match (
                        match_id, event_id, round_number, round_name,
                        winner_player_1, looser_player_1,
                        winner_player_2, looser_player_2,
                        winner_seed, looser_seed, end_type) 
                        values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", 
                        (match_id,event_id, round_number, round_name, 
                        winner_player_1, looser_player_1,
                        winner_player_2, looser_player_2,
                        winner_seed, looser_seed, end_type) )
                    match_count+=1
                    if winner_player_1 !='0000' and not winner_player_1 is None: c.execute("""insert into partake (player_id, match_id, won) values (%s,%s,%s)""" , (winner_player_1, match_id, True))
                    if looser_player_1 !='0000' and not looser_player_1  is None: c.execute("""insert into partake (player_id, match_id, won) values (%s,%s,%s)""" , (looser_player_1, match_id, True))
                    if winner_player_2 !='0000' and not winner_player_2 is None: c.execute("""insert into partake (player_id, match_id, won) values (%s,%s,%s)""" , (winner_player_2, match_id, True))
                    if looser_player_2 !='0000' and not looser_player_2  is None: c.execute("""insert into partake (player_id, match_id, won) values (%s,%s,%s)""" , (looser_player_2, match_id, True))                    
                    sets=len(scores)
                    for s in range(len(scores)):
                        c.execute("""INSERT into sets (match_id,set_number,winner,looser)
                        values (%s,%s,%s,%s)""",(match_id,s,scores[s][0],scores[s][1]))
                    con.commit()
    print(match_count)
                #con.rollback()            
            

    
                
