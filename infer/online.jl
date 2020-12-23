include("../software/TrueSkill.jl/src/TrueSkill.jl")
using .TrueSkill
global ttt = TrueSkill
using CSV
using Dates
using DataFrames

data = CSV.read("input/history_sorted.csv")

results = [[0, 1] for row in eachrow(data) ]
events = [ r.double == "t" ? [[r.winner_player_1,r.winner_player_2],[r.looser_player_1,r.looser_player_2]] : [[r.winner_player_1],[r.looser_player_1]] for r in eachrow(data) ]   
prior_dict = Dict{String,ttt.Rating}()

# m = Array{Float64,2}(undef, 3, 3)
# i = 0; j = 0
# for s in [2.,1.75,1.5,]
#     i = i + 1 
#     j = 0
#     for g in [0.03,0.04,0.05]
#         j = j + 1 
#         GC.gc()
#         h = ttt.History(events, results, data.day , prior_dict, ttt.Environment(mu=0.0,sigma=s,beta=1.,gamma=g,iter=4,epsilon=0.1))
#         ttt.convergence(h,true)
#         m[i,j] = ttt.log_evidence(h)
#         println("sigma: ", s,", gamma: ",g,", value: ",exp(m[i,j]/h.size))
#     end
# end
# #sigma: 1.75, gamma: 0.04, value: 0.5517622092161408
# #sigma: 1.5, gamma: 0.04, value: 0.551752018092088
# #sigma: 2.0, gamma: 0.04, value: 0.5517303232229469
# 

GC.gc()
h = ttt.History(events, results, data.day, prior_dict, ttt.Environment(mu=0.0,sigma=2.,beta=1.,gamma=0.04,iter=1,epsilon=0.1), true)

#h = ttt.History(events[1:2000], results[1:2000], data.day[1:2000], prior_dict, ttt.Environment(mu=0.0,sigma=2.,beta=1.,gamma=0.04,iter=1,epsilon=0.1), true)

m_w1 = [b.skills[e.teams[1].items[1].agent].online.mu for b in h.batches for e in b.events]
s_w1 = [b.skills[e.teams[1].items[1].agent].online.sigma for b in h.batches for e in b.events]

m_w2 = [ (length(e.teams[1].items) == 2) ? b.skills[e.teams[1].items[2].agent].online.mu : missing for b in h.batches for e in b.events]
s_w2 = [ (length(e.teams[1].items) == 2) ? b.skills[e.teams[1].items[2].agent].online.sigma : missing for b in h.batches for e in b.events]

m_l1 = [b.skills[e.teams[2].items[1].agent].online.mu for b in h.batches for e in b.events]
s_l1 = [b.skills[e.teams[2].items[1].agent].online.sigma for b in h.batches for e in b.events]

m_l2 = [ (length(e.teams[1].items) == 2) ? b.skills[e.teams[2].items[2].agent].online.mu : missing for b in h.batches for e in b.events]
s_l2 = [ (length(e.teams[1].items) == 2) ? b.skills[e.teams[2].items[2].agent].online.sigma : missing for b in h.batches for e in b.events]

evidence = [ (length(b.events[e].teams[1].items) == 2) ? ttt.Game([[ttt.Rating(m_w1[e],s_w1[e],1.0), ttt.Rating(m_w2[e],s_w2[e],1.0)],[ttt.Rating(m_l1[e],s_l1[e],1.0), ttt.Rating(m_l2[e],s_l2[e],1.0)]],[0,1],0.0).evidence : ttt.Game([[ttt.Rating(m_w1[e],s_w1[e],1.0)],[ttt.Rating(m_l1[e],s_l1[e],1.0)]],[0,1],0.0).evidence for b in h.batches for e in 1:length(b.events)]

df = DataFrame(
    id = data.match_id
    ,double = data.double
    ,w1 = data.winner_player_1
    ,w2 = data.winner_player_2
    ,l1 = data.looser_player_1
    ,l2 = data.looser_player_2
    ,odds = 1.0 ./ evidence 
    ,m_w1 = m_w1
    ,s_w1 = s_w1
    ,m_w2 = m_w2
    ,s_w2 = s_w2
    ,m_l1 = m_l1
    ,s_l1 = s_l1
    ,m_l2 = m_l2
    ,s_l2 = s_l2)
CSV.write("output/online.csv", df; header=true)
