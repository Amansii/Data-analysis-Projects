import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

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
    city = input('Please enter the name of the city 1-chicago 2-new york city 3-washington : \n').lower()
    while city not in CITY_DATA:
        city = input('Wrong input, Please re-enter the name of the city 1-chicago 2-new york 3-washington \n').lower()

    # get user input for month (all, january, february, ... , june)
    month = input('Please enter a month from january to june to filter with and all for no filter\n(letters in lower cases): \n').lower()
    while month not in ['january','february','march','april','may','june','all']:
            month = input('Wrong input, Please enter a month from january to june to filter with and all for no filter\n(letters in lower cases): \n').lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Please enter a week day to filter and all for no filter\n(letters in lower cases): \n').lower()
    while day not in ['sunday','monday','tuesday','wednesday','thursday','friday','saturday','all']:
            day = input('Wrong input, Please enter a week day to filter and all for no filter\n(letters in lower cases): \n').lower()

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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1

        # filter by month to create the new dataframe
        df = df[df['month']==month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week']==day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    days = ['sunday','monday','tuesday','wednesday','thursday','friday','saturday']
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # display the most common month
    df['month'] = df['Start Time'].dt.month
    popular_month = df['month'].mode()[0]

    # display the most common day of week
    df['day'] = df['Start Time'].dt.day_name()
    popular_day = df['day'].mode()[0]

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print("The most common month is {}\nThe most common day is {}\nThe most common hour is {} ".format(months[popular_month-1].title(),popular_day,popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start = df['Start Station'].mode()[0]
    print('The most common Start Station is : ',popular_start)

    # display most commonly used end station
    popular_end = df['End Station'].mode()[0]
    print('The most common End Station is : ',popular_end)

    # display most frequent combination of start station and end station trip
    popular_comb = (df['Start Station']+" - "+df['End Station']).mode()[0]
    print('The most common Combination of start and stop stations is :\n',popular_comb)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum()

    # display mean travel time
    mean_time = df['Trip Duration'].mean()

    print('The total time of travel of all trips is {} s ({} hr) \nwith average of {} s ({} hr)'.format(total_time,total_time/3600,mean_time,mean_time/3600))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    types = df['User Type'].value_counts()
    print('Counts of user types:\n',types)

    # Display counts of gender
    if 'Gender' in df :
        gender = df['Gender'].value_counts()
        print('\nCounts of genders:\n',gender)
    else:
        print('No Gender data for this city')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df :
        earliest = int(df['Birth Year'].min())
        latest = int(df['Birth Year'].max())
        popular_year = int(df['Birth Year'].mode()[0])
        print('\nThe earliest year of birth for a user is {} and the latest is {}'.format(earliest,latest))
        print('The most common year of birth for users is ',popular_year)
    else:
        print('No Birth Year data for this city')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()
    start_loc = 0
    while (view_data == 'yes'):
        print(df.iloc[start_loc:start_loc+5])
        start_loc += 5
        view_data = input("Do you wish to continue?: ").lower()

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
