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

GC.gc()
h = ttt.History(events, results, data.day, prior_dict, ttt.Environment(mu=0.0,sigma=2.,beta=1.,gamma=0.04,iter=16,epsilon=0.01))
ttt.convergence(h,true)

# m_w1 = [b.skills[e.teams[1].items[1].agent].online.mu for b in h.batches for e in b.events]
# s_w1 = [b.skills[e.teams[1].items[1].agent].online.sigma for b in h.batches for e in b.events]
# 
# m_w2 = [ (length(e.teams[1].items) == 2) ? b.skills[e.teams[1].items[2].agent].online.mu : missing for b in h.batches for e in b.events]
# s_w2 = [ (length(e.teams[1].items) == 2) ? b.skills[e.teams[1].items[2].agent].online.sigma : missing for b in h.batches for e in b.events]
# 
# m_l1 = [b.skills[e.teams[2].items[1].agent].online.mu for b in h.batches for e in b.events]
# s_l1 = [b.skills[e.teams[2].items[1].agent].online.sigma for b in h.batches for e in b.events]
# 
# m_l2 = [ (length(e.teams[1].items) == 2) ? b.skills[e.teams[2].items[2].agent].online.mu : missing for b in h.batches for e in b.events]
# s_l2 = [ (length(e.teams[1].items) == 2) ? b.skills[e.teams[2].items[2].agent].online.sigma : missing for b in h.batches for e in b.events]

evidences = [e.evidence for b in h.batches for e in b.events]

df = DataFrame(
    id = data.match_id
    ,double = data.double
    ,w1 = data.winner_player_1
    ,w2 = data.winner_player_2
    ,l1 = data.looser_player_1
    ,l2 = data.looser_player_2
    ,odds = 1.0./evidences)
CSV.write("output/ttt.csv", df; header=true)
