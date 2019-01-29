from assign1_support import *
from assign1 import *
stations = load_stations('stations2.txt')
dates = load_dates(stations)
data = load_all_stations_data(stations)
years, averages = yearly_averages(dates,data,'2000','2006')
a = get_year_info(dates,'2000','2001')
print(a)

