import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTH_D = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
DAY_WEEK = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    try:
        city = input("Write a city name: Chicago, New York or Washington!").lower()
        while city not in CITY_DATA:
            print("\nIncorrect answer\n")
            city = input("Write a city name: Chicago, New York or Washington!").lower()
            
    # TO DO: get user input for month (all, january, february, ... , june)
        month = input("Which month? January, February, March, April, May, or June? Or all of them").lower()
        while month not in MONTH_D:
            print("\nIncorrect answer\n")
            month = input("Which month? January, February, March, April, May, or June? Or all of them?").lower()
        
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
        day = input("Which day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday? All of them?").lower()
        while day not in DAY_WEEK:
            print("\nIncorrect answer\n")
            day = input("Which day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday? All of them?").lower()
        
        print('ok')
 
    except: 
        print("\nPlease check your answer\n")
    return city, month, day
    print('-'*40)

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
        df - Pandas DataFrame containing city data filtered by month and day
    Returns:
    """
    
    # load data file into a dataframe
    try:
        df = pd.read_csv(CITY_DATA[city])
    
    # convert the Start Time column to datetime
        df['Start Time'] = pd.to_datetime(df['Start Time'])
        df['End Time'] = pd.to_datetime(df['End Time'])
    
    # extract month, day of week and hour from the Start Time column 
        df['month'] = df['Start Time'].dt.month
        df['day_of_week'] = df['Start Time'].dt.weekday_name
        df['hour'] = df['Start Time'].dt.hour
    
    # filter by month if applicable
        if month != 'all':
            months =  ['January', 'February', 'March', 'April', 'May', 'June']
            month = MONTH_D.index(month) + 1
            df = df[df['month'] == month]
        
    # filter by day of week if applicable
        if day != 'all':
            df = df[ df['day_of_week'] == day.title()]

        return df
    except: 
        print('There are something wrong')

def time_stats(df,city):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')    
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].value_counts().idxmax()
    print("The most common month in", city, 'is:', most_common_month)

    # display the most common day of week
    most_common_day_of_week = df['day_of_week'].value_counts().idxmax()
    print("The most popular day of week in", city, 'is:', most_common_day_of_week)

    # display the most common start hour
    most_common_start_hour = df['hour'].value_counts().idxmax()
    print("The most common start hour in",  city, 'is:', most_common_start_hour)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
  
def station_stats(df,city):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    try:
        common_start_station = df['Start Station'].mode()[0]
        common_start_station_quantity = df['Start Station'].value_counts()[0]
        print("\nThe most common start station in\n", city, 'is:', common_start_station, 'it was used', common_start_station_quantity, 'times.')  
    except: 
        print('An error ocurred calculating commonly used start station')

    # display most commonly used end station
    try:
        common_end_station = df['End Station'].mode()[0]
        common_end_station_quantity = df['End Station'].value_counts()[0]
        print('\nThe most common end station in\n', city, 'is:', common_end_station, 'it was used', common_end_station_quantity, 'times.')  
    except: 
        print('An error ocurred calculating commonly used end station')

    # display most frequent combination of start station and end station trip
    try:
        common_trip= df.loc[:,'Start Station':'End Station'].mode()[0]
        common_trip_quantity = df.groupby(['Start Station','End Station']).size().max()
        print('\nThe most common trip is:\n',  common_trip, 'with', common_trip_quantity, 'times.' )  
    except: 
        print('An error ocurred calculating most frequent combination of start station and end station trip')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    
    total_travel_time = df['Trip Duration'].sum()
    print("Total travel time :", total_travel_time)

    # display mean travel time
    
    mean_travel_time = df['Trip Duration'].mean()
    print("Mean travel time :", mean_travel_time)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
   
def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df.groupby(['User Type'])['User Type'].count()
    print(user_types, "\n")
    if city != 'washington':
        # Display counts of gender
        gen = df.groupby(['Gender'])['Gender'].count()
        print(gen)
        # Display earliest, most recent, and most common year of birth
        mryob = sorted(df.groupby(['Birth Year'])['Birth Year'], reverse=True)[0][0]
        eyob = sorted(df.groupby(['Birth Year'])['Birth Year'])[0][0]
        mcyob = df['Birth Year'].mode()[0]
        print("The earliest year of birth is ", eyob, "\n")
        print("The most recent year of birth is ", mryob, "\n")
        print("The most common year of birth is ", mcyob, "\n")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    x = 1
    while True:
        raw = input('\nWould you like to see some raw data? Enter yes or no.\n')
        if raw.lower() == 'yes':
            print(df[x:x+5])
            x = x+5
        else:
            break

def data(df):
    start_loc = 0
    while True:
            view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()
            if view_data not in ['no','yes']:
                print("Isn´t the correct answer, please write yes or no.")
            elif view_data == 'yes':
                start_loc += 5
                print(df.iloc[start_loc : start_loc +5])
            again = input('Would you like to see more? Yes or No').lower()
            if again == 'no':
                break
            elif view_data == 'no':
                return


def main():
    while True:
        city, month, day = get_filters()
        
        df = load_data(city, month, day)

        time_stats(df,city)
        station_stats(df,city)
        trip_duration_stats(df)
        user_stats(df,city)

        data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
    
##Reference links: https://github.com/ozlerhakan/bikeshare/blob/master/bikeshare.py  --  https://github.com/xhlow/udacity-bikeshare-project/blob/master/bikeshare.py