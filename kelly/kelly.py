import sys
sys.path.append('../software/ttt/')
import src as ttt
from importlib import reload  # Python 3.4+ only.
reload(ttt)

import math
import pandas as pd
import time
import datetime

df = pd.read_csv('../base/atp/history.csv')
df = df.sort_values(by=['time_start', 'round_number'])
results = [[0,1] for _ in range(df.shape[0])]
composition = [[[w1, w2],[l1, l2]] if d == "t" else [[w1],[l1]] for d, w1, w2, l1, l2 in zip(df.double, df.winner_player_1, df.winner_player_2, df.looser_player_1, df.looser_player_2)]   
times = []
prior_dict = dict()

#import trueskill as ts
#env = ts.TrueSkill(draw_probability=0.0,tau=0.09, beta=1)
#forward = dict()
#for c in composition:
    #if not (c[0][0] in forward):
        #forward[c[0][0]] = [env.Rating(0.0,6.0)]
    #w1 = forward[c[0][0]][-1]
    #if not (c[1][0] in forward):
        #forward[c[1][0]] = [env.Rating(0.0,6.0)]
    #l1 = forward[c[1][0]][-1]
    
    #teams = [[w1],[l1]]
    
    #if len(c[0]) == 2:
        #if not (c[0][1] in forward):
            #forward[c[0][1]] = [env.Rating(0.0,6.0)]
        #w2 = forward[c[0][1]][-1]
        #if not (c[1][1] in forward):
            #forward[c[1][1]] = [env.Rating(0.0,6.0)]
        #l2 = forward[c[1][1]][-1]
        
        #teams[0].append(w2) 
        #teams[1].append(l2)
    
        #[w1, w2], [l1, l2] = env.rate(teams,[0,1])
        
        #forward[c[0][1]].append(w2)
        #forward[c[1][1]].append(l2)
    #else:
        #[w1], [l1] = env.rate(teams,[0,1])
    
    #forward[c[0][0]].append(w1)
    #forward[c[1][0]].append(l1)

# forward["t012"][1:7] 
# [trueskill.Rating(mu=3.339, sigma=4.986), trueskill.Rating(mu=5.066, sigma=4.428), trueskill.Rating(mu=6.169, sigma=4.061), trueskill.Rating(mu=6.957, sigma=3.796), trueskill.Rating(mu=7.559, sigma=3.592), trueskill.Rating(mu=8.040, sigma=3.429)]

df.time_start

h = ttt.History(composition , results, times , prior_dict, ttt.Environment(mu=0.0,sigma=6.,beta=1.,gamma=0.09,iterations=1))
ts_log_evidence = h.log_evidence()

math.exp(ts_log_evidence/df.shape[0]) < 0.508

h.batches[-1].events
h.batches[-1].skills['sd46'].forward
#N(mu=2.554, sigma=0.509)
h.batches[-1].forward_prior_out('sd46')
#N(mu=2.499, sigma=0.502)

for a in h.batches[-1].skills:
    

