all: inputs outputs

inputs: input/history_sorted.csv
input/history_sorted.csv:
	julia data.jl

outputs: output/trueskill.csv output/ttt.csv
output/trueskill.csv:
	julia trueskill.jl
output/ttt.csv:
	julia ttt.jl
output/online.csv:
	julia online.jl
