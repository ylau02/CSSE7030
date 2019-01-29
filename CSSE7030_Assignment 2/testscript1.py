#testscript
from assign2_support import *
from assign2 import *
data = TemperatureData()
data.load_data("Brisbane.txt")
data.get_ranges()
data.load_data("Adelaide.txt")
data.get_ranges()
data.load_data("Canberra.txt")
data.get_ranges()
data.get_stations()
