import time
import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
import osmnx as ox
import networkx as nx
import folium

CITY_DATA = { 'chicago': ('chicago.csv', 'chicago.json', 'Chicago, Illinois, United States'),
              'new york': ('new_york_city.csv', 'new_york_city.json', 'New York, New York, United States'),
              'washington': ('washington.csv', 'washington.json', 'Washinton, DC, United States') }

def get_city():
    #input the city name and if not in the list, popup will show up again to ask for retry
    city = input('\nWhich city of data would you like to see Chicago, New York or Washington?\n')
    while city.lower() not in ('chicago','new york','washington'):
        print("I'm sorry that looks like we don't have data for the city\n")
        city = input('\nWhich city of data would you like to see Chicago, New York or Washington?\n')
    return city.lower()

def date_check():
    '''input the date(month and day) and if not in the list, popup will show up again to ask for retry
       you can specify both(month and day) or day only or month only or nothing specified
    '''
    month_sp=0
    day_sp=0
    
    date_check = input('\nWould you like to filter the data by month, day, both or none? Type "none" for no filter\n').lower()
    while date_check not in ('both','month','day','none'):
        print("I'm sorry but would you please place the right values?\n")
        date_check = input('\nWould you like to filter the data by month, day, both or none? Type "none" for no filter\n')
    # get user input for day of week (all, monday, tuesday, ... sunday)
    if date_check.lower()=='both':
        month = get_month()
        month_sp=1

        day = get_day()
        day_sp=1
        
    elif date_check.lower() =='month':
        month = get_month()
        month_sp=1
        day='all'
    elif date_check.lower() =='day':
        day = get_day()
        day_sp=1
        month='all'
    elif date_check.lower()=='none':
        month='all'
        day='all'
    
    return month, day, month_sp, day_sp

def get_month():
    #input the month and if not in the list, popup will show up again to ask for retry
    month =input('Which month are you interested in? January, February, March, April, May or June?\n')
    while month.lower() not in ('january','february','march','april','may','june'):
        print("I'm sorry that we don't have the data for that\n")
        month =input('Which month are you interested in? January, February, March, April, May or June?\n')
    return month.lower()

def get_day():
    #input the day and if not in the list, popup will show up again to ask for retry
    day = int(input('\nWhich day of a week are you interested in? Type an integer please (eg.., 1=Sunday)\n'))
    while day not in range(1,8):
        print("I'm sorry that we don't have the data. Please place an integer between 1 and 7\n")    
        day = int(input('\nWhich day of a week are you interested in? Type an integer please (eg.., 1=Sunday)\n'))
    
    return day
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city=get_city()

    # get user input for month (all, january, february, ... , june)
    month, day, month_sp, day_sp=date_check()
    print('-'*40)
    return city, month, day, month_sp, day_sp


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city][0])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    
    # filter by month if applicable
    if month != 'all':
        print(month)
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1
        # filter by month to create the new dataframe
        #df = df[df['month']==month]
        df = df.query('month == @month')
    # filter by day of week if applicable
    if day != 'all':       
        # filter by day of week to create the new dataframe
        days=['sunday','monday','tuesday','wednesday','thursday','friday','saturday']
        day=days[day-1]
        df = df[df['day_of_week']==day.title()]
    
    return df


def time_stats(df,month_sp,day_sp):
    """Displays statistics on the most frequent times of travel.

    Args:
        (dataframe) df - containing bike share data
        (int) month_sp(0 or 1) - if month is specified, 1 is placed and no graph will be shown because there's only one month
        (int) day_sp(0 or 1) - if day is specified, 1 is placed and no graph will be shown because there's only one day
    Returns:
        showing most popular month/day
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month and day of week
    
    # only month is specified
    if month_sp==1:
        month_n=df['month'].unique()
        print(month_n)
        print('\nThe Most Common Month of Travel is\n')
        #just one month info so no graph
        draw_info(df,'month','max')
        print('\nThe Most Common day of week of Travel is\n')
        draw_info(df,'day_of_week','max',1)
    # only day is specified   
    elif day_sp==1:
        day_of_week=df['day_of_week'].unique()
        print(day_of_week)
        print('\nThe Most Common Month of Travel is\n')
        draw_info(df,'month','max',1)
        print('\nThe Most Common day of week of Travel is\n')
        #just one day info so no graph
        draw_info(df,'day_of_week','max')
    #otherwise
    else:
        print('\nThe Most Common Month of Travel is\n')
        draw_info(df,'month','max',1)
        print('\nThe Most Common day of week of Travel is\n')
        draw_info(df,'day_of_week','max',1)
    
    # display the most common start hour
    print('\nThe Most Common hour of Travel is\n')
    df['hour']=df['Start Time'].dt.hour
    draw_info(df,'hour','max',1)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df,city):
    """Displays statistics on the most popular stations and trip.

    Args:
        (dataframe) df - containing bike share data
        (str) city - the one you'd like to see
    Returns:
        showing most common start/end station and trip(start and end station combo)
        this also shows you the route between start/end if different, and point if the same
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('\nThe Most Common Start Station is\n')

    draw_info(df,'Start Station','max')

    # display most commonly used end station
    print('\nThe Most Common End Station is\n')

    draw_info(df,'End Station','max')
    # display most frequent combination of start station and end station trip
    print('\nThe Most frequent trip between start and end is\n')

    df['trip']=df['Start Station']+':'+ df['End Station']
    #preparing list of trip
    sst_est=[]
    draw_info(df,'trip','max')
    sst_est=df['trip'].mode().values[0]
    #diassemble trip to start and end
    s_station=sst_est.split(':')[0]
    e_station=sst_est.split(':')[1]
    #if latitude and longitide info are available, map will be drawn
    draw_map(city,s_station,e_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df,month_sp,day_sp):
    """Displays statistics on the total and average trip duration.

    Args:
        (dataframe) df - containing bike share data
        (int) month_sp(0 or 1) - if month is specified, 1 is placed and no graph will be shown because there's only one month
        (int) day_sp(0 or 1) - if day is specified, 1 is placed and no graph will be shown because there's only one day
    Returns:
        showing total trip duration and mean trip duration
    """
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    df['Trip Time']=df['End Time']-df['Start Time']

    # display total travel time
    print('\nTotal Trip Duration...\n')
    if month_sp==1:
        draw_info(df,'day_of_week','sum',1)
    elif day_sp==1:
        draw_info(df,'month','sum',1)
    else:
        draw_info(df,'month','sum',1)    
        draw_info(df,'day_of_week','sum',1)

    # display mean travel time
    print('\nMean Trip Duration...\n')
    if month_sp==1:
        draw_info(df,'day_of_week','mean',1)
    elif day_sp==1:
        draw_info(df,'month','mean',1)
    else:
        draw_info(df,'month','mean',1)
        draw_info(df,'day_of_week','mean',1)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users.

    Args:
        (dataframe) df - containing bike share data
        (str) city - the one you'd like to see
    Returns:
        the numbers by user type
    """
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('\nUser type counts\n')
    draw_info(df,'User Type','freq',1)

    if city !="washington": #because washinton doesn't have gender info
        # Display counts of gender
        print('\nGender type counts\n')
        draw_info(df,'Gender','freq',1)

        # Display earliest, most recent, and most common year of birth
        print('\nBirthday stats\n')
        print("Oldest year:",df['Birth Year'].min()," Youngest year:",df['Birth Year'].max()," Most common year:",df['Birth Year'].mode())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def draw_info(df,item,agg_type,graph_activate=0):
    """
    Drawing graph for the specified item if graph_activate flag is 1.

    Args:
        (dataframe) df - containing bike share data
        (str) item - trip(start/end station combo), month, day_of_week, gender, customer can be specified
        (str) aggregation type - sum, mean, count(frequency) can be specified.
        (int) graph acitivate flag(0 or 1) - if specified, graph will be drawn, otherwise, the text info is shown only.

    Returns:
        drawing graph and showing text info
    """
    mod_items=df[item].mode().values[0]
    mod_number=df[item].value_counts().max()
    frequency=df[item].value_counts()
    item_names = frequency.index
    item_counts = frequency.values
    item_cap=item.capitalize()
    #sorted by month and sum/mean for Trip Time
    if agg_type=='sum' or agg_type=='mean':
        group_month=df.groupby('month')
        group_day=df.groupby('day_of_week')
        
    if item=='month':
        if agg_type=='sum':
            sum_month=group_month['Trip Time'].sum()
            item_names = sum_month.index
            item_counts = sum_month.values/86400000000000
            print(sum_month)
        elif agg_type=='mean':
            mean_month=group_month['Trip Time'].mean()
            item_names = mean_month.index
            item_counts = mean_month.values/60000000000
            print(mean_month)
    #sorted by day and sum/mean for Trip Time
    if item=='day_of_week':
        item='day'
        if agg_type=='sum':
            sum_day=group_day['Trip Time'].sum()
            item_names = sum_day.index
            item_counts = sum_day.values/86400000000000
            print(sum_day)
        elif agg_type=='mean':
            mean_day=group_day['Trip Time'].mean()
            item_names = mean_day.index
            item_counts = mean_day.values/60000000000
            print(mean_day)
    if agg_type=='max':
        print("{0}: {1}, Number of rides: {2}".format(item_cap,mod_items,mod_number))
    if graph_activate==1:
        #showing info with sum or mean
        if  agg_type=='sum' or agg_type=='mean':
            title='The duration of rides for '+ item
            x_label=item.capitalize()
            y_label=agg_type.capitalize()+' Duration'
        #showing info by gender/user type
        elif item=='Gender' or item=='User Type':
            title='The number of users by '+ item
            x_label=item
            y_label='Number of users'
            
            for ty,val in zip(item_names,item_counts):
                print(ty,val)
        elif item=='month' or item=='day' or item=='hour':
            title='The number of rides by '+item
            x_label=item
            y_label='Number of rides'
        plt.bar(item_names,item_counts)
        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.show()
def draw_map(city,s_station,e_station):
    """
    Drawing map for the specified city and route between start station and end station.

    Args:
        (str) city - name of the city to analyze
        (str) start station - name of the start station
        (str) end station - name of the end station
    Returns:
        drawing map
    """
    start_time = time.time()

    #loading latitude and longitude file for the city 
    lat_lng_f=CITY_DATA[city][1]
    lat_lng_dict = open(lat_lng_f, "r", encoding="utf-8")
    with lat_lng_dict as ll:
        LAT_LANG_DIC = json.load(ll)

    orig_lat, orig_lng=LAT_LANG_DIC[s_station]
    dest_lat, dest_lng=LAT_LANG_DIC[e_station]
    origin=(orig_lat,orig_lng)
    destination=(dest_lat,dest_lng)
    print('Latitude and longitude for Start Station is: ',origin)
    print('Latitude and longitude for End Station is: ',destination)
    if orig_lat !='no data' or dest_lat !='no data':
        print('\nCalculating Routes... it would take a few mins..\n')
        # location where you want to find your route
        place     = CITY_DATA[city][2]
        # choose the mode of moving
        mode      = 'bike'        # 'drive', 'bike', 'walk'

        # find shortest path based on distance or time
        optimizer = 'time'        # 'length','time'

        #Start Station will be highlited in green
        start_marker = folium.Marker(
                    location = origin,
                    popup = s_station,
                    icon = folium.Icon(color='green'))
        
        #End Station will be highlited in red
        end_marker = folium.Marker(
                    location = destination,
                    popup = e_station,
                    icon = folium.Icon(color='red'))
        
        #  find the shortest path
        if origin != destination:
            # create graph from OSM within the boundaries of some geocodable place(s)
            graph = ox.graph_from_place(place, network_type = mode)

            # find the nearest node to the start location
            orig_node = ox.distance.nearest_nodes(graph, origin[1], origin[0])

            # find the nearest node to the end location
            dest_node = ox.distance.nearest_nodes(graph, destination[1],destination[0]) 
            shortest_route = nx.shortest_path(graph,orig_node,dest_node,weight=optimizer)
            shortest_route_map = ox.plot_route_folium(graph, shortest_route,tiles='openstreetmap')
            
            #adding start and end marker
            start_marker.add_to(shortest_route_map)
            end_marker.add_to(shortest_route_map)

            #display(shortest_route_map)
            shortest_route_map
        else: # if bike is rented and returned at the same place
            print("Bikes are rented/returned at the same place")
            folium_map = folium.Map(location=origin,zoom_start=15)

            # plot the single marker
            folium.Marker(location=origin).add_to(folium_map)
            #display(folium_map)
            folium_map
        
        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)

def main():
    while True:
        city, month, day, month_sp, day_sp= get_filters()
        df = load_data(city, month, day)
        time_stats(df, month_sp, day_sp)
        station_stats(df,city)
        trip_duration_stats(df,month_sp,day_sp)
        user_stats(df,city)
        line_no=0
        ind_data = input('\nWould you like to see some of the individual data? Enter yes or no.\n').lower()
        while ind_data =='yes':
            print(df[line_no:line_no+5])
            ind_data = input('\nWould you like to see some of the individual data? Enter yes or no.\n').lower()
            line_no +=5
        #prompt the message saying showing first rows
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
