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
    while True:
        city = input("Which city's data would you like to see? (Chicago, Washington, New York City) ")
        city = city.lower()
        if city == 'chicago' or city == 'washington' or city == 'new york city':
            break
        else:
            print("That's not a valid city!")

    while True:
        month = input("Which month's data would you like to see? (All, January, February, March, April, May, June) ")
        month = month.lower()
        if month == 'all' or month == 'january' or month == 'february' or month == 'march' or month == 'april' or month == 'may' or month == 'june':
            break
        else:
            print("That's not a valid month!")

    while True:
        day = input("Which day of the week's data would you like to see? (All, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday) ")
        day = day.lower()
        if day == 'all' or day == 'monday' or day == 'tuesday' or day == 'wednesday' or day == 'thursday' or day == 'friday' or day == 'saturday' or day == 'sunday':
            break
        else:
            print("That's not a valid day of the week!")

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
        df - pandas DataFrame containing city data filtered by month and day
    """

    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name


    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        df = df[df['month'] == month]


    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    df["Start Time"] = pd.to_datetime(df["Start Time"])
    df["month"] = df["Start Time"].dt.month
    popular_month = df["month"].mode()[0]
    MONTH_DICT = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June"}
    print("The most popular month to travel is {}.".format(MONTH_DICT[popular_month]))

    df["day"] = df["Start Time"].dt.dayofweek
    popular_day = df["day"].mode()[0]
    DAY_DICT = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"}
    print("The most popular day of the week to travel is {}.".format(DAY_DICT[popular_day]))

    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print("The most frequent start hour is {}.".format(popular_hour))

    print("\nThis took %.4f seconds." % (time.time() - start_time))
    print('-'*25)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    start_station = df["Start Station"].mode()[0]
    print("The most commonly used start station is {}.".format(start_station))

    end_station = df["End Station"].mode()[0]
    print("The most commonly used end station is {}.".format(end_station))

    df["Round Trip"] = df["Start Station"] + ' to ' + df["End Station"]
    round_trip = df["Round Trip"].mode()[0]
    pd.set_option('display.max_colwidth',1000)
    print("The most frequent combination of start and end station is {}.".format(round_trip))


    print("\nThis took %.4f seconds." % (time.time() - start_time))
    print('-'*25)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_travel_min = df["Trip Duration"].sum()
    total_travel_hour = int(round(total_travel_min / 60))
    total_travel_day = int(round(total_travel_hour / 24))
    print("The total travel duration was {:,} minutes, or about {:,} hours or {:,} days.".format(total_travel_min, total_travel_hour, total_travel_day))


    mean_travel_min = df["Trip Duration"].mean()
    mean_travel_hour = int(round(mean_travel_min / 60))

    print("The mean travel time was {:.4f} minutes, or about {:,} hours.".format(mean_travel_min, mean_travel_hour))

    print("\nThis took %.4f seconds." % (time.time() - start_time))
    print('-'*25)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_types = df["User Type"].value_counts()
    print("There are {:,} subscribers, and {:,} customers.".format(user_types[0], user_types[1]))

    try:
        gender = df["Gender"].value_counts()
        print("There are {:,} male and {:,} female bike riders.".format(gender[0], gender[1]))
    except KeyError:
        print("Gender statistics are not available for this data.")

    try:
        oldest = int(df["Birth Year"].min())
        youngest = int(df["Birth Year"].max())
        avg = df["Birth Year"].mode()[0]
        print("The earliest birth year of a rider is {}, the most recent is {}, and the most common is {}.".format(oldest, youngest, int(avg)))
    except KeyError:
        print("Age statistics are not available for this data.")

    print("\nThis took %.4f seconds." % (time.time() - start_time))
    print('-'*25)

def display_data(df):
    df = df.copy().iloc[:, 1 :-5]
    view_data = input('\nWould you like to view 5 rows of individual data? Enter yes or no\n')
    start_loc = 0
    end_loc = 5
    while view_data.startswith('y'):
        df_indiv = df.iloc[start_loc:end_loc]
        df_list = df_indiv.values.tolist()
        for item in df_list:
            print(item)
        start_loc += 5
        end_loc += 5
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
