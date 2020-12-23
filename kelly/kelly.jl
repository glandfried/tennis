using CSV
using Dates
using DataFrames
using Plots


ts = CSV.read("../infer/output/trueskill.csv")
ttt = CSV.read("../infer/output/ttt.csv")

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
        return teb*f
    end
end

bet = kelly.(ts.odds,1.0./ttt.odds) 
teb = yllek.(ts.odds,1.0./ttt.odds) 
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




