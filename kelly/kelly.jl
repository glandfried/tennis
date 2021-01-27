using CSV
#using Dates
#using DataFrames
using Plots
#using Distributions

function inverse_odd(odd)
    return 1.0 / (1.0 - (1.0/odd))
end
function kelly(odd_w,p_w)
    b = odd_w - 1
    return (b*p_w - (1-p_w))/b
end
function yllek(odd_w,p_w)
    b = inverse_odd(odd_w) - 1.0
    return (-p_w + b*(1-p_w))/b
end

function laverage(odd,p,f=1.0)
    bet = kelly(odd,p)
    if bet > 0.0
        return bet*f
    else
        teb = yllek(odd,p)
        return -teb*f
    end
end

function results(laverage, odds, wins)
    res = laverage
    res[wins] .=  res[wins] .* odds[wins]
    return res
end


ts = CSV.read("../infer/output/trueskill.csv")
ttt = CSV.read("../infer/output/ttt.csv")
odds_ttt = ts.odds
pred_ttt = 1.0./ttt.odds
ts = missing
ttt = missing
GC.gc()

wins = laverage.(odds_ttt,pred_ttt) .> 0.0
res = results(laverage.(odds_ttt,pred_ttt), odds_ttt, wins)
cumsum(log.(1. .+ res))

###################################

ts = CSV.read("../infer/output/trueskill.csv")
ttt = CSV.read("../infer/output/ttt.csv")
odds = ttt.odds
pred = 1.0./ts.odds
ts = missing
ttt = missing
GC.gc()

wins = laverage.(odds,pred) .> 0.0
res_ts = results(laverage.(odds,pred), odds, wins)
cumsum(log.(1. .+ res_ts))



###################################


predicciones = CSV.read("../infer/output/trueskill.csv")
oferta = CSV.read("../infer/output/trueskill_carreira.csv")
#ttt = CSV.read("../infer/output/ttt.csv")
oferta[ismissing.(oferta.winner_prior_2_mu), "winner_prior_2_mu"] = 0.0
oferta[ismissing.(oferta.winner_prior_2_sigma), "winner_prior_2_sigma"] = 0.0
oferta[ismissing.(oferta.loser_prior_2_mu), "loser_prior_2_mu"] = 0.0
oferta[ismissing.(oferta.loser_prior_2_sigma), "loser_prior_2_sigma"] = 0.0

d = oferta.winner_prior_1_mu .+ oferta.winner_prior_2_mu .- oferta.loser_prior_1_mu .- oferta.loser_prior_2_mu
v = sqrt.(oferta.winner_prior_1_sigma.^2 .+  oferta.winner_prior_2_sigma.^2 .+ oferta.loser_prior_1_sigma.^2 .+ oferta.loser_prior_2_sigma.^2 .+ 2. .+ 2.0*Float64.(oferta.winner_prior_2_sigma.!=0))

proba = cdf.(Normal(), d./v)
odds = 1.0./predicciones.odds

# SEGUIR

bet = kelly.(odds,proba) 
teb = yllek.(odds,proba) 
l = [ (bet[i] > 0.0) ? bet[i] : -teb[i] for i in 1:length(bet)]

fs = 0.05:0.05:1.0
wealth = []
for i in 1:length(fs)
    deltas = 1 .+ l*fs[i]
    push!(wealth,sum(log.(deltas)))
end

findmax(wealth)
plot(wealth)

deltas = 1 .+ [ (bet[i] > 0.0) ? 0.1 : -0.1 for i in 1:length(bet)]
cumsum(log.(deltas))

plot(cumprod(1 .+ l)[1:38])




