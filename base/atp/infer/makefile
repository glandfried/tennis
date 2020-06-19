all: history, history_sets

history:
	psql -h mininet.exp.dc.uba.ar -U glandfried -d tenis -f history.sql -A -F "," -o history.csv --pset footer

history_sets:
	psql -h mininet.exp.dc.uba.ar -U glandfried -d tenis -f history_sets.sql -A -F "," -o history_sets.csv --pset footer

ttt:
	python3 ttt.py
