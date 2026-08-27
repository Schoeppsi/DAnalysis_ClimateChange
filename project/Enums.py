from enum import Enum

class Region(Enum):
    World = 0,
    Continents = 1,
    Countries = 2
    
class DisasterType(Enum):
    alldisasters = 0,
    excl_earthquakes = 1,
    excl_extrweather = 2,
    drought = 3,
    drymassmovement = 4,
    wetmassmovement = 5,
    earthquake = 6,
    extrtemperature = 7,
    extrweather = 8,
    flood = 9,
    volcanic = 10
    wildfire = 11