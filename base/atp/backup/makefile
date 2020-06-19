all: dump zip release

dump:
	ssh postgres@mininet.exp.dc.uba.ar 'pg_dump tenis' > `date +'%y-%m-%d'`.dump

zip:
	zip `date +'%y-%m-%d'`.zip `date +'%y-%m-%d'`.dump

release:
	hub release edit -a `date +'%y-%m-%d'`.zip atp

#local:
#	psql tennis  < `date +'%y-%m-%d'`.dump 
