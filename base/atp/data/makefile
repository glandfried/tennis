all: release

release: history.csv

history.csv:
	wget https://github.com/glandfried/tennis/releases/download/atp/history.csv.zip
	unzip history.csv.zip

history:
	psql -h mininet.exp.dc.uba.ar -U glandfried -d tenis -f history.sql -A -F "," -o history.csv --pset footer

history_sets:
	psql -h mininet.exp.dc.uba.ar -U glandfried -d tenis -f history_sets.sql -A -F "," -o history_sets.csv --pset footer

ttt:
	python3 ttt.py
