Each of the below is run using the command
> seaplan MYPARAMFILE.seaplan.yaml

GulfMexico
==========
The simplest example: just a paramter file
    - GulfMexico.seaplan.yaml : the parameter file

MayOBS
==========
Adds a CSV file for the stations
    - MayOBS.seaplan.yaml : the parameter file
    - MayOBS_stations.csv : the stations file (specified in the parameter file)

GEODEVA7
==========
Adds a bathymetry grid
    - GEODEVA7.seaplan.yaml : the parameter file
    - GEODEVA7.csv : the stations file (specified in the parameter file)
    - WCC_VAN.grd: a netcdf bathymetry file (specified in the parameter file)
