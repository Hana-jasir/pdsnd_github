

import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new york.csv',
              'washington': 'washington.csv' }

months = ['january', 'february', 'march', 'april', 'may', 'june']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!\n')
    print('choose a city to filter : chicago or washington or new york')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Please enter the city name: ").lower()
    while city not in ['chicago','washington', 'new york']:
        city = input(
        "invalid city name, Please retype again: ").lower()

    # get user input for month (all, january, february, ... , june)
    print('choose between these months : january, february, march, april, may, june')
    month = input("Please enter the month name: ").lower()
    while month not in  ['january', 'february', 'march', 'april', 'may', 'june']:
        month = input(
        "invalid month name, Please retype again: ").lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Please enter the day of week: ").lower()
    while day not in  ['sunday', 'monday', 'tuesday', 'wednesay', 'thursday', 'friday','saturday']:
        day = input(
        "invalid day name, Please retype again: ").lower()

    print('-'*40)
    return city, month, day


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
    df=pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['start_hour'] = df['Start Time'].dt.hour
    df['month'] = df['Start Time'].apply(lambda x: x.month)
    df['day_of_week'] = df['Start Time'].apply(lambda x: x.strftime('%A').lower())
    #  most frequent combination of start station and end station trip
    df['routes'] = df['Start Station']+ " " + df['End Station']
    # trip duration
    df['duration'] = df['End Time'] - df['Start Time']

    # filter by month 
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month) + 1
        # create the new dataframe
        df = df.loc[df['month'] == month]

    # filter by day of week 
    if day != 'all':
        #  create the new dataframe
        df = df.loc[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\n--> Calculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # common month
    print("Most common month is: {}".format(
        str(df['month'].mode().values[0]))
    )

    # common day of week
    print("Most common day of the week is: {}".format(
        str(df['day_of_week'].mode().values[0]))
    )

    # common start hour
    print("Most common start hour is: {}".format(
        str(df['start_hour'].mode().values[0]))
    )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\n--> Calculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("Most common start station is: {} ".format(
        df['Start Station'].mode().values[0])
    )

    # display most commonly used end station
    print("Most common end station is: {}".format(
        df['End Station'].mode().values[0])
    )

    # display most frequent combination of start station and end station trip
    print("The most common start and end station combo is: {}".format(
        df['routes'].mode().values[0])
    )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\n--> Calculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['duration'].sum()
    print("Total travel time is: " + str(total_travel_time))

    # display mean travel time
    mean_travel_time = df['duration'].mean()
    print("Mean travel time is: " + str(mean_travel_time))
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\n--> Calculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("\nDisplay of various user types:")
    print(df['User Type'].value_counts())

    # Display counts of gender
    if city == 'chicago' or city == 'new york':
        print("\nDisplay of gender counts:")
        print(df['Gender'].value_counts())

        # Display earliest, most recent, and most common year of birth
        print('\nEarliest birth from the given fitered data is: {}\n'.format(int(df['Birth Year'].min())))
        print('Most recent birth from the given fitered data is: {}\n'.format(int(df['Birth Year'].max())))
        print('Most common birth from the given fitered data is: {}\n'.format(int(df['Birth Year'].mode()[0])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_raw_data(df):
    """
    Display contents of the CSV file to the display as requested by
    the user.
    """
    data_request  = input("Do you want to see 5 lines of raw data?: ").lower()

    index = 0

    while data_request == 'yes':
        print(df.iloc[index:index+5])
        data_request  = input("Do you want to see the next 5 lines of raw data?: ").lower()
        index = index + 5
        




def main():

    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
