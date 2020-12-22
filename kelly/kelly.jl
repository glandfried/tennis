include("../software/TrueSkill.jl/src/TrueSkill.jl")
#include("../../TrueSkill.jl/src/TrueSkill.jl")
using .TrueSkill
global ttt = TrueSkill
using CSV
using Dates
using DataFrames
#using JLD2


data = CSV.read("../base/atp/history.csv")

#Carreira
#10^(-101100/(length(data.double) - sum(data.double .== "t")))

times = Dates.value.(data[:,"time_start"] .- Date("1900-1-1")) .- data.round_number
insert!(data, 10, times, :day)
data = sort!(data, [:day], rev=(false))

times = Vector{Int64}()
results = [[0, 1] for row in eachrow(data) ]
events = [ r.double == "t" ? [[r.winner_player_1,r.winner_player_2],[r.looser_player_1,r.looser_player_2]] : [[r.winner_player_1],[r.looser_player_1]] for r in eachrow(data) ]   
prior_dict = Dict{String,ttt.Rating}()
GC.gc()

# Optimization TrueSkill
# m = Array{Float64,2}(undef, 3, 3)
# i = 0; j = 0
# for s in [0.5,0.75,1.]
#     i = i + 1 
#     j = 0
#     for g in [0.06,0.07,0.08]
#         j = j + 1 
#         GC.gc()
#         h = ttt.History(events, results, times , prior_dict, ttt.Environment(mu=0.0,sigma=s,beta=1.,gamma=g,iter=3,epsilon=0.1))
#         m[i,j] = ttt.log_evidence(h)
#         println("sigma: ", s,", gamma: ",g,", value: ",exp(m[i,j]/h.size))
#     end
# end
# # sigma: 0.75, gamma: 0.07, value: 0.535938169030606
# 
# GC.gc()
# 
# m = Array{Float64,2}(undef, 3, 3)
# i = 0; j = 0
# for s in [0.9,0.8,0.7]
#     i = i + 1 
#     j = 0
#     for g in [0.02,0.025,0.03]
#         j = j + 1 
#         GC.gc()
#         h = ttt.History(events, results, data.day , prior_dict, ttt.Environment(mu=0.0,sigma=s,beta=1.,gamma=g,iter=3,epsilon=0.1))
#         m[i,j] = ttt.log_evidence(h)
#         println("sigma: ", s,", gamma: ",g,", value: ",exp(m[i,j]/h.size))
#     end
# end
# #sigma: 0.8, gamma: 0.025, value: 0.5383314035052896

h = ttt.History(events, results, data.day , prior_dict, ttt.Environment(mu=0.0,sigma=0.8,beta=1.,gamma=0.025,iter=3,epsilon=0.1))

w1 = [e.teams[1].items[1].agent for b in h.batches for e in b.events]
w1 == data.winner_player_1

m_w1 = [b.skills[e.teams[1].items[1].agent].forward.mu for b in h.batches for e in b.events]
s_w1 = [b.skills[e.teams[1].items[1].agent].forward.sigma for b in h.batches for e in b.events]

m_w2 = [ (length(e.teams[1].items) == 2) ? b.skills[e.teams[1].items[2].agent].forward.mu : missing for b in h.batches for e in b.events]
s_w2 = [ (length(e.teams[1].items) == 2) ? b.skills[e.teams[1].items[2].agent].forward.sigma : missing for b in h.batches for e in b.events]

m_l1 = [b.skills[e.teams[2].items[1].agent].forward.mu for b in h.batches for e in b.events]
s_l1 = [b.skills[e.teams[2].items[1].agent].forward.sigma for b in h.batches for e in b.events]

m_l2 = [ (length(e.teams[1].items) == 2) ? b.skills[e.teams[2].items[2].agent].forward.mu : missing for b in h.batches for e in b.events]
s_l2 = [ (length(e.teams[1].items) == 2) ? b.skills[e.teams[2].items[2].agent].forward.sigma : missing for b in h.batches for e in b.events]

prior_prediction = [e.evidence for b in h.batches for e in b.events ]

df = DataFrame(
    id = data.match_id
    ,w1 = data.winner_player_1
    ,w2 = data.winner_player_2
    ,l1 = data.looser_player_1
    ,l2 = data.looser_player_2
    ,m_w1 = m_w1
    ,s_w1 = s_w1
    ,m_w2 = m_w2
    ,s_w2 = s_w2
    ,m_l1 = m_l1
    ,s_l1 = s_l1
    ,m_l2 = m_l2
    ,s_l2 = s_l2
    ,odds = 1.0./prior_prediction )
CSV.write("output/optimum_trueskill_estimation.csv", df; header=true)

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

df = DataFrame(
    id = data.match_id
    ,double = data.double
    ,w1 = data.winner_player_1
    ,w2 = data.winner_player_2
    ,l1 = data.looser_player_1
    ,l2 = data.looser_player_2
    ,m_w1 = m_w1
    ,s_w1 = s_w1
    ,m_w2 = m_w2
    ,s_w2 = s_w2
    ,m_l1 = m_l1
    ,s_l1 = s_l1
    ,m_l2 = m_l2
    ,s_l2 = s_l2)
CSV.write("output/ttt_2_0.04_online_estimation.csv", df; header=true)
