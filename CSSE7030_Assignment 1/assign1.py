
###################################################################
#
#   CSSE1001/7030 - Assignment 1
#
#   Student Number: 42377***
#
#   Student Name: Joyce Lau
#
###################################################################

#####################################
# Support given below - DO NOT CHANGE
#####################################

from assign1_support import *

#####################################
# End of support 
#####################################

# Add your code here

def load_dates(stations):
    """Return the list of dates in the data files

    load_dates() --> list(str)
    """
    
    list_dates = []
    for station in stations:
        file = open(station+'.txt', 'r')
        for line in file:        
            dates = line.strip()
            dates = line.split()
            list_dates.append(dates[0])
        break
        file.close()
    return list_dates

def load_station_data(station):
    """Return a list of temperatures as floats from a given station (e.g. "Brisbane")

    load_station_data() --> float(temperature)
    """
    
    list_temp = []
    data_file = open(station+'.txt','r')
    for line in data_file:
        temps = line.strip()
        temps = line.split()
        list_temp.append(float(temps[1]))
    data_file.close()
    return list_temp

    
def load_all_stations_data(stations):
    """Returns a ist of data for each station

    load_all_stations_data(str)-->list
    """
    
    list_data = []
    
    for station in stations:
        data = load_station_data(station)
        list_data.append(data)
        
    return list_data

def display_maxs(stations,dates,data,start_date,end_date):
    """Returns the maximum temperatures for given station within then given date range

    display_maxs(str,list,list,int,int) --> float
    """
    
    display_stations(stations,'Date')
    
    for n, date in enumerate(dates):
        if date >= start_date and date <=end_date:
            print(date, end='    ')
            for d, c in enumerate(data):
                display_temp(data[d][n])
            print()
                    
def temperature_diffs(data,dates,stations,station1,station2,start_date,end_date):
    """Returns a tuple containing the date and the temperatue difference between the two chosen stations

    temperature_diffs(list(list(float)),list(str), list(str),str,str,str,str) --> list(tup(str, float))
    """
    
    index1 = dates.index(start_date)
    index2 = dates.index(end_date)+1
    datelist = dates[index1:index2]
    s_index1 = stations.index(station1)
    s_index2 = stations.index(station2)
    
    for station in stations:
        if station == station1:
            s1_data = data[s_index1][index1:index2]
        if station == station2:
            s2_data = data[s_index2][index1:index2]

    resultlist = []
    
    for n,c in enumerate(s1_data):
        if s1_data[n] == 99999.9 or s2_data[n] == 99999.9:
            result = 99999.9
            resultlist.append(result)
        else:
            result = s1_data[n] - s2_data[n]
            result = float(result)
            resultlist.append(result)

    temp_diff = []
    m = 0

    for i, date in enumerate(datelist):
        temp_diff.append((datelist[i],resultlist[m]))
        m += 1

    return temp_diff


def display_diffs(diffs,station1,station2):
    """Display the temperature differences between the two specified stations

    display_diffs(float) --> None
    """
    
    print('Temperature differences between '+station1+' and '+station2+' \n')
    print('Date', end= '      ')
    print('Temperature Differences', end = '')
    print()

    for i,c in enumerate(diffs):
        date, temp = diffs[i]
        print(date, end = "  ")
        display_temp(temp)
        print()
    


def yearly_averages(dates,data,start_year,end_year):
    """Returns the pair of years and the yearly averages within the given range of years

    yearly_average(list(list(float)),list(str),str,str) ---> tuple(list(str),list(list(float)))
    """
    
    year_info = get_year_info(dates,start_year,end_year)
    year = year_info[0]
    averages = []
    list_averages = []
    emptylist = []

    for row in data:
        for i, c in enumerate(year_info[1][:-1]):
            temp = row[c:year_info[1][i+1]]
            total = 0
            for t in temp:
                if t != 99999.9:
                    total += t
            ave = total/len(temp)
            averages.append(ave)

    while averages != emptylist: #This is to create a tuple containing the list of years and list of averages
        list1 = averages[:len(year_info[0])]
        averages = averages[len(year_info[0]):]
        list_averages.append(list1)      

    result = (year,list_averages)

    return result
    
def display_yearly_averages(years, averages, stations):
    """Displays the yearly averages in the stations file

    display_yearly_averages(list(str),list(float),list(str)) --> None
    """
    
    print('Year', end="     ")
    for station in stations:
        print(station, end="      ")
    print()
    for i, c in enumerate(years):
        print(c, end="    ")
        for n, m in enumerate(averages):
            display_temp(m[i])
        print()
      
def interact():
    """Text-Based user-interface to allow users to enter a command

    The command will display the results
    """
    print("Welcome to BOM Data")
    
    inp_stations = input("Please enter the name of the Stations file: ")
    stations = load_stations(inp_stations)
    dates = load_dates(stations)
    data = load_all_stations_data(stations)
    
    print("Enter 'dm' and a date range to view the maximum temperatures")
    print("Enter 'dd', the two stations and the date range to view the temperature differences between the two stations in that date range")
    print("Enter 'ya' and the year range to view the yearly averages within that year range")
    print("To quit, enter 'q'")
    
    while True:
        command = input('Command: ')
        if command.startswith('dm'):
            command = command.split()
            if len(command) == 3:
                display_maxs(stations,dates,data,command[1],command[2])
                continue
            else:
                print("Unknown Command:",command)
                continue
        elif command.startswith('dd'):
            command = command.split()
            if len(command) == 5:
                diffs = temperature_diffs(data,dates,stations,command[1],command[2],command[3],command[4])
                display_diffs(diffs,command[1],command[2])
                continue
            else:
                print("Unknown Command:",command)
                continue
        elif command.startswith('ya'):
            command = command.split()
            if len(command) == 3:
                years, averages = yearly_averages(dates,data,command[1],command[2])
                display_yearly_averages(years, averages, stations)
            else:
                print("Unknown Command:",command)
                continue
        elif command == 'q':
            break
        else:
            print("Unknown Command:", command)


##################################################
# !!!!!! Do not change (or add to) the code below !!!!!
# 
# This code will run the interact function if
# you use Run -> Run Module  (F5)
# Because of this we have supplied a "stub" definition
# for interact above so that you won't get an undefined
# error when you are writing and testing your other functions.
# When you are ready please change the definition of interact above.
###################################################

if __name__ == '__main__':
    interact()
