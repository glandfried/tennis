all:
	make -C update
	make -C backup

release: history.csv

history.csv:
	wget https://github.com/glandfried/tennis/releases/download/atp/history.csv.zip
	unzip history.csv.zip
	
