import psycopg2
import socket
import sys

#import os
#os.chdir("/home/landfried/gaming/trabajos/conquerClub/db/conquerSkill/")
#os.chdir("/home/landfried/gaming/trabajos/conquerClub/db/conquerSkill/")

def delete_match(c,con,argv):
    

    # sets
    # partake
    # match
    tables = ["sets", "partake", "play", "play_clay","play_carpet","play_hard","play_grass","match"]
    
    delete = ""
    for t in tables:
        delete = delete + """ 
        with rm as (
                select match_id
                from event e
                inner join match m
                on e.event_id = m.event_id
                where time_start >= '2019-01-01'
        )
        
        delete 
        FROM {0} 
        using rm
        where {0}.match_id = rm.match_id;""".format(t)
        
    
    c.execute(delete)
    #con.rollback()
    
    delete =""" 
        delete
        from event e
        where time_start >= '2019-01-01'"""
    c.execute(delete)    
    con.commit()
    
    delete = """
        with players as (
            select distinct player_id
            from play
        )
        
        delete 
        from player as d
        using player as p
        left join players ps
        on ps.player_id = p.player_id
        where ps.player_id is null
        and p.player_id <> '0000'
        and d.player_id = p.player_id;   
    """
    c.execute(delete)
    con.commit()
    #con.rollback()
    
def update_player(c,con):
    update=""
    tables = ["","_clay","_carpet","_hard","_grass"]
    for t in tables:#t=tables[0]
        update = update + """
            with all_play as (
                select p.player_id, p.skill, p.uncertainty, e.time_start, p.games_played
                ,row_number() over (partition by player_id order by time_start desc) as rn
                from play{0} p
                inner join match m
                on m.match_id = p.match_id
                inner join event e
                on e.event_id = m.event_id
            )
            , last_play as (
                select *
                from all_play
                where rn = 1
            )
            
            update player as p 
            set skill{0}=lp.skill,uncertainty{0}=lp.uncertainty
            ,last_play{0}=lp.time_start,games_played{0}=lp.games_played
            from last_play lp
            where lp.player_id = p.player_id;
        """.format(t)
    c.execute(update)
    con.commit()
    #con.rollback()
if __name__ == "__main__":
    if socket.gethostname() == "mininet-vm":		
        con = psycopg2.connect(database='tenis', user='glandfried', password="caimancito")
        c = con.cursor()
    else:
        con = psycopg2.connect(database='tenis', user='glandfried', password="caimancito", host='mininet.exp.dc.uba.ar', port='5432')
        c = con.cursor()            
    
    delete_match(c,con,sys.argv)