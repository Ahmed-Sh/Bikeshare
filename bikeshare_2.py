import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def ask_for_input(item, output, items):
    """
    Asks user to Choose a city, month, and day to analyze.

    Args:
        (str) item - define the variable we are going to get from the user
        (str) output - empty string as initial input
        items - Criteria to check the user input validity
    Returns:
        (str) output - city or month or day
    """
    while output not in items:
        if item == "city":
            output = input("Please select a city to see its Data: Chicago, New york city  or Washington: ").lower()
        elif item == "month":
            output = input("Please select a month from January to June to filter by it, "
                           "or choose 'all' for no month filter: ").lower()
        elif item == "day":
            output = input("Please select a day name to filter by it, or choose 'all' for no day filter: ").lower()
        if output not in items:
            print("Invalid input")
    return output


def get_filters():
    """
    Collects the user inputs for city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    output = ""
    city = ask_for_input("city", output, CITY_DATA.keys())

    # get user input for month (all, january, february, ... , june)
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    month = ask_for_input("month", output, months)

    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day = ask_for_input("day", output, days)

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
    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # filter by month to create the new dataframe
        df = df[df["month"].isin([month.title()])]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'].isin([day.title()])]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print("The most Common month is: ", df['month'].mode()[0])

    # display the most common day of week
    print("The most Common day is: ", df['day_of_week'].mode()[0])

    # display the most common start hour
    print("The most Common hour is: ", df['hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("The most used Start Station is: ", df['Start Station'].mode()[0])

    # display most commonly used end station
    print("The most used End Station is: ", df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    grouped_start_stop = df.groupby(['Start Station', 'End Station']).size().sort_values(ascending=False).index[0]
    print("The most frequent Start, Stop combination is: ", grouped_start_stop)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    # print(f"The total travel time is: {df['Trip Duration'].sum()} Seconds")
    print(f"The total travel time is: {np.sum(df['Trip Duration'])} Seconds")

    # display mean travel time
    # print(f"The Average travel time is: {df['Trip Duration'].mean()} Seconds")
    print(f"The Average travel time is: {np.mean(df['Trip Duration'])} Seconds")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print(f"The User Types count is: \n{df['User Type'].value_counts()}")

    # Display counts of gender
    try:
        print(f"The Gender count is: \n{df['Gender'].value_counts()}")
    except KeyError:
        print("Gender Count is not available for this city")
        
    # Display earliest, most recent, and most common year of birth
    try:
        print(f"The oldest biker year of birth is: \n{df['Birth Year'].min()}")
        print(f"The youngest biker year of birth is: \n{df['Birth Year'].max()}")
        print(f"The most common year of birth is: \n{df['Birth Year'].mode()}")
    except KeyError:
        print("Year of Birth is not available for this city")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        answer = input(f"Would you like to check the Raw data of {city.title()}.\n"
                       f"Type 'yes' to check or press any key to move on: ").lower()
        n = 0
        m = 5
        for i in range(len(df)):
            if answer == 'yes':
                if m >= len(df):
                    print(df[n: len(df)])
                    break
                else:
                    print(df[n: m])
            else:
                break
            answer = input("Do u want to see the next 5 Rows? \n "
                           "Type 'yes' to continue or press any key to move on: ").lower()
            n += 5
            m += 5

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        restart = input("\nWould you like to restart? Type 'yes' to continue or press any key to exit.\n")
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
