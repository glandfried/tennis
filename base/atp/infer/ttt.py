import os
name = os.path.basename(__file__).split(".py")[0]
##################
#import time
import pandas as pd
import numpy as np
import sys
sys.path.append('../../../software/ttt/')
#import numpy as np
import src as th
from importlib import reload  # Python 3.4+ only.
reload(th)
env = th.TrueSkill(draw_probability=0,tau=(25/3)/(365),beta=4.33,epsilon=0.1)
import ipdb

# Data
df = pd.read_csv('history.csv')
df.sort_values(['time_start','time_end'], inplace=True)
df.reset_index(inplace=True)
fecha = [e  if pd.isna(s) else (s if pd.isna(e) else min(s,e))   for s, e in zip(df.time_start,df.time_end) ]
pd.to_datetime(fecha,format='%Y-%m-%d')

results = [[0,1]] * df.shape[0] 
composition = [[[w1,w2],[l1,l2]] if d else [[w1],[w2]] for w1, w2, l1, l2, d in zip(df.winner_player_1, df.winner_player_2, df.looser_player_1, df.looser_player_2, df.double) ]   
batch  =  (pd.to_datetime(fecha,format='%Y-%m-%d')- pd.to_datetime('1910-01-01',format='%Y-%m-%d')).dt.days

history= env.history(composition, results,batch)
history.through_time(online=False)
history.convergence()

ipdb.set_trace()
match_id = list(range(len(df.match_id)))
w1_mean = [ history.match_time[m].posteriors[w1].mu for m, w1 in zip(match_id, df.winner_player_1) ]
w1_std = [ history.match_time[m].posteriors[w1].sigma for m, w1 in zip(match_id, df.winner_player_1) ]
l1_mean = [ history.match_time[m].posteriors[l1].mu for m, l1 in zip(match_id, df.winner_looser_1) ]
l1_std = [ history.match_time[m].posteriors[l1].sigma for m, l1 in zip(match_id, df.winner_looser_1) ]
w2_mean = [ history.match_time[m].posteriors[w2].mu if d else None for m, w2, d in zip(match_id, df.winner_player_2, df.double) ]
w2_std = [ history.match_time[m].posteriors[w2].mu if d else None for m, w2, d in zip(match_id, df.winner_player_2, df.double) ]
l2_mean = [ history.match_time[m].posteriors[l2].mu if d else None for m, l2, d in zip(match_id, df.looser_player_2, df.double) ]
l2_std = [ history.match_time[m].posteriors[l2].mu if d else None for m, l2, d in zip(match_id, df.looser_player_2, df.double) ]
evidence = [ history.match_time[m].match_evidence[m] for m in df.match_id] 
last_evidence = [ history.match_time[m].match_last_evidence[m] for m in match_id] 

df["w1_mean"] = w1_mean
df["w1_std"] = w1_std
df["w2_mean"] = w2_mean
df["w2_std"] = w2_std
df["l1_mean"] = l1_mean
df["l1_std"] =l1_std
df["l2_mean"] = l2_mean
df["l2_std"] =l2_std
df["evidence"] = evidence
df["last_evidence"] = last_evidence

df.to_csv(name+".csv", index=False)
