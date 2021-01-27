using CSV
using Dates
using DataFrames

data = CSV.read("../base/atp/data/history.csv")

#times = Dates.value.(data[:,"time_start"] .- Date("1900-1-1")) .- data.round_number
times = Dates.value.(data[:,"time_start"] .- Date("1900-1-1"))
insert!(data, 10, times, :day)
data = sort!(data, [:day, :round_number], rev=(false, true))
#data = sort!(data, [:day, :round_number], rev=(false, false)) # mal ordenado
#data = sort!(data, [:day], rev=(false))
CSV.write("input/history_sorted.csv", data; header=true)

