# OpenTransport Belgium

OpenTransport Belgium is a project to extract data from transport corporations all over Belgium.

It's goals are to scrape (or to get by ourselves) :

* routes
* stops
* timetables
* real-time

And then provide a nice, unified API fot thoses.
We would also like to store all thoses data over time to provide historical data

##Usecases
Usecases would/could be :

* Nice websites to replace often old one from the corporations
* a Raildar.be (see Raildar.fr)
* predict timetables (eg: show somehow that train 1234 if *always* 5 min late (or early))
* bind with OSM to provide multimodal, realtime nice routing (for eg with http://navitia.io/)
* push back stations and routes to OSM
* GTFS and GTFS realtime exports
* ?


## Steps

I think it should be done that way : (for each corp)

1. Gather stops and routes and provide a nice API
2. Gather static timetables and provide a nice API
3. Provide GTFS with both of the above
4. Get realtime data(=last known position and if provided, lateness) (often only the last station is provided), store it and provide an API
5. Make something that extrapolates the last position to the current position and that fires events whith positions (with, if possible, (arrival) predictions from the coorp) (note: if we have realtime gps position, this step is trivial)

We should try to make abstractions so that each "layer" could be usable with another coorp if applicable


##Available datasets :
None of thoses are yet standadized or stored
Maybe we could find some more at http://data.irail.be/

### STIB/MIVB:
Static:

* stations
* lines
* timetables

Dynamic:

* realtime (=last stop) python lib

### SNCB/NMBS
Static :

* GTFS (http://data.openov.nl/belgie/nmbs.zip)

Dynamic:

* Last stop for every current train

Maybe :

* Every 6 min, the actual past arrival/departure time for past stops + theorical arrival/departure time and planned lateness for future stops for every train (http://archive.irail.be/)


### DeLijn
Static:

* GTFS (http://gtfs.ovapi.nl/archive/delijn/)

### TEC
Static:

* GTFS (http://gtfs.ovapi.nl/tec/)
* http://datahub.io/dataset/tec

## Available APIs
None


## Bonus goal

Make this data very accessible and well documented because it was a real pain in the ass all thoses sources
