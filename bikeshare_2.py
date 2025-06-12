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
    print('Hello! Let\'s explore some US bikeshare data!🚲 🚀')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    cities = {'chicago': 'chicago', 'new york': 'new york city', 'nyc': 'new york city', 'new york city': 'new york city', 'newyorkcity': 'new york city',
                    'washington': 'washington', 'dc': 'washington'}
    while True:
        city_input = input ('Please choose a city (Chicago, Washington or New York City)🏙️🌉: ').strip().lower()
        if city_input in cities:
            city = cities[city_input]
            break
        print('Please enter a City from Chicago, Washington or New York City 🏙️🌉:')

    # get user input for month (all, january, february, ... , june)
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    while True:
        month = input ('Please choose a month from January to June or select all! 🗓️: ').strip().lower()
        if month in months:
            break
        print('Please choose a month from January to June or select all! 🗓️:')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    while True:
        day = input ('Please choose a day from Monday to Sunday or select all! 📆: ').strip().lower()
        if day in days:
            break
        print('Please enter Monday to Sunday or select all! 📆: ')

    print('='*80)
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
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month_name().str.lower()
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()

    if month != 'all':
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day]


    return df


def show_raw_data(df):
    """Displays raw data upon user request, 5 rows at a time."""
    
    if df.empty:
        print("\n❌ No data available to display.")
        return
    
    start_row = 0
    while True:
        show_data = input("\nWould you like to see 5 lines of raw data? Enter yes or no. 📜\n").strip().lower()
        if show_data != 'yes':
            break
        print(df.iloc[start_row:start_row+5])
        start_row += 5
        if start_row >= len(df):
            print("\n❌ No more data available! ❌")
            break  


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\n⏳🚲  Calculating The Most Frequent Times of Travel...⏳🚲 \n')
    start_time = time.time()

    # display the most common month
    if month == 'all':
        most_common_month = df['month'].mode()[0].capitalize()
        print(f'📆 The most common month is: {most_common_month}!')
    
    elif month != 'all':
        print(f'🔍 Month is already filtered to {month.capitalize()}!')

    # display the most common day of week
    if day == 'all':
        most_common_day = df['day_of_week'].mode()[0].capitalize()
        print(f'📆 The most common day is: {most_common_day}!')

    elif day != 'all':
        print(f'🔍 Day is already filtered to {day.capitalize()}!')

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_common_hour = df['hour'].mode()[0]
    print(f'🕚 The most common start hour is: {most_common_hour}!')

    print("\n⏳ This took %s seconds." % (time.time() - start_time))
    print('='*60)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\n🚲 🚉 Calculating The Most Popular Stations and Trip...🚲 🚉 \n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print(f'📍 The most commonly used START STATION is:\n➡️  {most_common_start_station}!\n')

    print("🔝 Top 5 Start Stations:")
    print(df['Start Station'].value_counts().head(5))

    print('-'*40)

    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print(f'🏁 The most commonly used END STATION is:\n➡️  {most_common_end_station}!\n')

    print("\n🔝 Top 5 End Stations:")
    print(df['End Station'].value_counts().head(5))

    print('-'*40)

    # display most frequent combination of start station and end station trip
    df['Trip Combination'] = df['Start Station'] + ' ➡️ ' + df['End Station']
    most_common_trip = df['Trip Combination'].mode()[0]
    print(f'🔄 The most FREQUENT TRIP COMBINATION is:\n🚲 {most_common_trip}!')

    print("\n⏳ This took %s seconds." % (time.time() - start_time))
    print('='*60)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\n⏳ Calculating Trip Duration...⏳ \n')
    start_time = time.time()

    # display total travel time
    total_travel_time = int(df['Trip Duration'].sum())
    days = total_travel_time // 86400
    hours = (total_travel_time % 86400) // 3600
    minutes = (total_travel_time % 3600) // 60
    seconds = total_travel_time % 60
    print('📊 Total Travel Time:')
    print(f'➡️  {days} day(s), {hours} hour(s), {minutes} minute(s), {seconds} second(s)')

    # display mean travel time
    mean_travel_time = int(df['Trip Duration'].mean())
    mean_hours = mean_travel_time // 3600
    mean_minutes = (mean_travel_time % 3600) // 60
    mean_seconds = mean_travel_time % 60
    print('📈 Mean Travel Time:') 
    print(f'➡️  {mean_hours} hour(s), {mean_minutes} minute(s), {mean_seconds} second(s)')

    print("\n⏳ This took %s seconds." % (time.time() - start_time))
    print('='*60)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\n👤 Calculating User Stats...👤 \n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('📊 Counts of user types:')
    print(user_types)
    print('-'*40)

    # Display counts of gender
    if 'Gender' in df.columns: 
        gender_counts = df['Gender'].value_counts()
        print('\n👨 Counts of Gender 👩')
        print(gender_counts)
        print('-'*40)
    else:
        print('\n❌ No gender data available.')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_birth_year = int(df['Birth Year'].min())
        most_recent_birth_year = int(df['Birth Year'].max())
        most_common_birth_year = int(df['Birth Year'].mode()[0])

        print(f'\n🎂 Earliest year of birth: {earliest_birth_year}')
        print(f'📅 Most recent year of birth: {most_recent_birth_year}')
        print(f'📈 Most common year of birth: {most_common_birth_year}')
    else:
        print('\n❌ No birth year available.')

    print("\n⏳ This took %s seconds." % (time.time() - start_time))
    print('='*60)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        show_raw_data(df)
        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.🔄 \n').strip().lower()
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()


# Sources:
# 1. pandas.pydata.org  - [Pandas Cheat Sheet]              Link: https://pandas.pydata.org/Pandas_Cheat_Sheet.pdf
# 2. reddit             - [Python beginners cheat sheet]    Link: https://www.reddit.com/r/learnpython/comments/11eg5af/beginners_python_cheat_sheets_updated/?rdt=62024
# 3. ChatGPT (OpenAI)
# 4. Datacamp.com       - [NumPy Cheat Sheet]               Link: https://www.datacamp.com/cheat-sheet/numpy-cheat-sheet-data-analysis-in-python