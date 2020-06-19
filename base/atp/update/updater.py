import re
import ipdb

ronda_dict = {'Final':0,'Finals':0, 'Semifinals':1 ,'Semi-Finals':1, 'Quarterfinals':2, 'Quarter-Finals':2, 'Round of 16': 3, 'Round of 32': 4, 'Round of 64': 5, 'Round of 128': 6, '3rd Round Qualifying':7, '2nd Round Qualifying':8, '1st Round Qualifying':9
              , 'Round Robin':10, '3rd/4th Place Match':11}

seed_dict = {'LL': "Lucky loser: a player who plays the qualifying round to enter an event, but loses in the final qualifying round , he then enters the main draw after the start of an event as a result of another player withdrawal due to illness or injury", 'Q': "Qualifier: is a player whose ranking is not high enough to permit direct entry in to a tournament and thus he has to play the qualifying round to enter the main draw.", 'WC': "Wild cards: allow direct entry in to events for players who are not ranked high enough to enter an event directly. The wild cards are given by the authorities mainly to 3 kind of players, as under.", 'AL': None, "S": None, 'PR': None, 'SE': None  }

score_dict = {
'(RET)': "layer's withdrawal during a match, causing the player to forfeit the tournament. Usually this happens due to injury.", '(W/O)': "Unopposed victory. A walkover is awarded when the opponent fails to start the match for any reason, such as injury.",
'(DEF)': None,'(ABD)':None,'(ABN)':None,'(NA)':None,'(WEA)':None,'(UNP)':None
}

def update(c, con, url, tree, double, challenger, db_active = False):    
    tour_name = url.split("/")[6]
    tour_id = url.split("/")[7]
    timestamp = tree.xpath("//span[@class='tourney-dates']/text()")[0].strip(' \r\n\t')    
    print(timestamp )
    year = int(timestamp.split(".")[0])    
    
    event_id = int(tour_id)*(10**5)+int(year)*(10)+int(double) 
    
    matchs_in_web = 0
    partidas_en_ronda = tree.xpath("//div[@id='scoresResultsContent']/div/table/tbody")    
    for penr in partidas_en_ronda:#penr=partidas_en_ronda[-1]
        matchs_in_web += len(penr.xpath("./tr") )
    
    query = """
    select count(match_id)
    from match
    where event_id = {}    
    """.format(event_id)
    c.execute(query)    
    #con.rollback()
    matchs_at_db= c.fetchall()[0][0]
    if matchs_at_db< matchs_in_web: 
        print("Faltan partidas!",  tour_name, tour_id, year)
        #####
        # Tour
        query = "select * from tournament where tour_id = {}".format(tour_id)        
        c.execute(query)#con.rollback
        in_db = len(c.fetchall())>0
        if not in_db:
            if db_active: c.execute("""insert into tournament (tour_id, tour_name) 
                values (%s, %s)""", (tour_id, tour_name) )
            print("Nuevo torneo!", tour_id, tour_name)
        #####
        # Event
        tour_details = tree.xpath(
        "//td[@class='tourney-details-table-wrapper']//td[@class='tourney-details']")
        for td in tour_details:#td=tour_details[0]
            if len(td.xpath("./div/div[@class='icon-court image-icon']"))>0:
                ground = td.xpath(
                "./div/div[@class='item-details']/span[@class='item-value']/text()")[0]
                ground = ground.strip(' \r\n\t')        
        timestamp = tree.xpath("//span[@class='tourney-dates']/text()")[0].strip(' \r\n\t')    
        if ' - ' in timestamp:
            time_start = timestamp.split(" - ")[0].replace('.', '-')
            time_end = timestamp.split(" - ")[1].replace('.', '-')
        else: 
            time_start = timestamp.replace('.', '-')
            time_end = None
        #
        query = "select * from event where event_id = {}".format(event_id)        
        c.execute(query)#con.rollback
        in_db = len(c.fetchall())>0
        if not in_db:
            if db_active: c.execute("""
            insert into event (event_id, tour_id, year, double, challenger, 
            time_start , time_end, ground) values (%s,%s,%s,%s, %s,%s,%s,%s)"""
            , (event_id, tour_id, year, double, challenger, time_start, time_end, ground) )
            print("Nuevo Evento!", tuple([tour_name, tour_id, year, double, ground]))        
        #####
        # Players    
        s = 'overview'
        players_url = set(filter(lambda x: (x[0:12]=='/en/players/' or x[0:12]=='/es/players/')
            and x[-9:] == '/overview', tree.xpath("//@href")))
        players = list(map(lambda x: tuple(re.split('en/players/|es/players/',x)[1].split("/overview")[0].split("/")) , players_url))
        #
        for player_name, player_id in players:#player_name, player_id = players[0]
            query = "select * from player where player_id = '{}'".format(player_id)        
            c.execute(query);#con.rollback
            in_db = len(c.fetchall())>0
            if not in_db:
                #print("New player")
                if db_active: c.execute("""insert into player 
                (player_id, player_name) values (%s, %s)""", (player_id, player_name))    
                
        if db_active: con.commit();#con.rollback()            
        
        ######    
        # Match - sets
        ronda = tree.xpath("//div[@id='scoresResultsContent']/div/table/thead")
        partidas_en_ronda = tree.xpath("//div[@id='scoresResultsContent']/div/table/tbody")
        winner_player_2=None; looser_player_2=None; looser_seed=None; winner_seed=None; end_type=None
        for r in range(len(ronda)):#r =0
            round_name = ronda[r].xpath("./tr/th")[0].text
            round_number = ronda_dict[round_name]
            matchs = partidas_en_ronda[r].xpath("./tr")        
            #cantidad_partidas_ronda = len(matchs)
            for m in matchs:#m=matchs[0]
            
                seeds_element = m.xpath("./td[@class='day-table-seed']")
                if len(seeds_element[0].xpath("./span"))==1: 
                    winner_seed =  seeds_element[0].xpath("./span")[0].text.strip(' \n\t').split("(")[1].split(")")[0]
                if len(seeds_element[1].xpath("./span"))==1: 
                    looser_seed =  seeds_element[1].xpath("./span")[0].text.strip(' \n\t').split("(")[1].split(")")[0]            
                players_element = m.xpath("./td[@class='day-table-name']"); players =[]            
                winner_team_element = players_element[0].xpath("./a")
                winner_player_1 = re.split('en/players/|es/players/',winner_team_element[0].xpath("./@href")[0])[1].split("/overview")[0].split("/")[1]
                if len(winner_team_element )==2:
                    winner_player_2 = re.split('en/players/|es/players/',winner_team_element[1].xpath("./@href")[0])[1].split("/overview")[0].split("/")[1]
                looser_team_element = players_element[1].xpath("./a")
                if len(looser_team_element)==0: 
                    looser_player_1 = '0000' # bye
                else: 
                    url = looser_team_element[0].xpath("./@href")[0]
                    if url != '#': looser_player_1 = re.split('en/players/|es/players/',url)[1].split("/overview")[0].split("/")[1]
                    else: looser_player_1 = '0000'
                if len(looser_team_element )==2: 
                    url = looser_team_element[1].xpath("./@href")[0]
                    if url != '#': looser_player_2 = re.split('en/players/|es/players/',url)[1].split("/overview")[0].split("/")[1]
    
    
                match_id=str(event_id)+str(round_number)+winner_player_1+looser_player_1 
                ## sets
                score_element = m.xpath("./td[@class='day-table-score']")[0]
                scores = []
                #score_element.xpath("./a/text()")
                #if len(score_element.xpath('./a'))==1 and len(score_element.xpath("./a")[0].text.strip(' \n\t'))>1:

                #sets_texts = list(filter(lambda x: x != '' , map(lambda x: x.replace('\r','').replace('\n','').replace('\t','').split(' ') ,score_element.xpath("./a/text()"))))
                list_of_lists = [x.replace('\r','').replace('\n','').replace('\t','').split(' ') for x in score_element.xpath("./a/text()")]
                sets_texts = [e for ls in list_of_lists for e in ls if e != '']  
                #sup =  score_element.xpath("./a/sup/text()")                                
                desarmar = list(map(lambda x: x.split(' '),  sets_texts))              
                sets = [e for l in desarmar for e in l]
                #win_alternative = sum(map(lambda x: x in score_dict.keys(), sets))>0
                end_type = "empty"
                for s in range(len(sets)):#s=0
                    end_type = "sets"
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
                
                query = "select * from match where match_id = '{}'".format(match_id)        
                c.execute(query)#con.rollback
                in_db = len(c.fetchall())>0
                if not in_db: print("Nuevo match!", match_id,round_number, round_name)               
                if not in_db and db_active:
                    # Match
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
                    # Partake
                    won = True
                    if winner_player_1 !='0000' and not winner_player_1 is None: 
                        c.execute("""insert into partake (player_id, match_id, won)
                        values (%s,%s,%s)""" , (winner_player_1, match_id, won))
                    if winner_player_2 !='0000' and not winner_player_2 is None: 
                        c.execute("""insert into partake (player_id, match_id, won) 
                        values (%s,%s,%s)""" , (winner_player_2, match_id, won))
                    won = False
                    if looser_player_1 !='0000' and not looser_player_1 is None:
                        c.execute("""insert into partake (player_id, match_id, won)
                        values (%s,%s,%s)""" , (looser_player_1, match_id, won))
                    if looser_player_2 !='0000' and not looser_player_2 is None: 
                        c.execute("""insert into partake (player_id, match_id, won) 
                        values (%s,%s,%s)""" , (looser_player_2, match_id, won))                    
                    # Sets
                    sets=len(scores)
                    for s in range(len(scores)):
                        if db_active: c.execute("""
                        INSERT into sets (match_id,set_number,winner,looser)
                        values (%s,%s,%s,%s)""",(match_id,s,scores[s][0],scores[s][1]))
                elif in_db and db_active:
                    c.execute("""
                    update match
                    set round_number = {}
                    where match_id = '{}'
                    """.format(round_number,match_id))
                    
        if db_active: 
            print(tour_name, tour_id, year, double, ground)            
            con.commit()
            print("commit")
    else:
        print("Partidas completas", tour_name, tour_id, year)
                    #con.rollback()            
                
delete = """ 
delete from set 
where match_id in (
    select m.match_id
    from match m 
    inner join event e
    on e.event_id = m.event_id
    left join play pm
    on pm.match_id = m.match_id
    where pm.player_id is null and looser_player_1 <> '0000'
)
"""
delete = """ 
delete from partake pk 
where match_id in (
    select m.match_id
    from match m 
    inner join event e
    on e.event_id = m.event_id
    left join play pm
    on pm.match_id = m.match_id
    where pm.player_id is null and looser_player_1 <> '0000'
)
"""

delete = """ 
delete from match 
where match_id in (
    select m.match_id
    from match m 
    inner join event e
    on e.event_id = m.event_id
    left join play pm
    on pm.match_id = m.match_id
    where pm.player_id is null and looser_player_1 <> '0000'
)
"""

