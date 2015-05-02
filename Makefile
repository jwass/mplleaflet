# Command taken from mpld3's makefile to manager submodule's as packages
sync_current : mplexporter
	rsync -r mplexporter/mplexporter mplleaflet/
