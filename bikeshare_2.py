import time
import pandas as pd
import numpy as np

# Set display settings for Pandas
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTH_DATA = {'january': 1, 'feburary': 2, 'march': 3,
              'april': 4, 'may': 5, 'june': 6,
              'july': 7, 'august': 8, 'september': 9,
              'october': 10, 'november': 11, 'december': 12}

DAY_DATA = {'monday': 0, 'tuesday': 1, 'wednesday': 2,
            'thursday': 3, 'friday': 4, 'saturday': 5, 'sunday': 6}

def find_key(input_dict, value):
    """"Returns first key in a dictionary that has the specified value
        Solution from Stackoverflow:
        https://stackoverflow.com/questions/16588328/return-key-by-value-in-dictionary"""
    return next((k for k, v in input_dict.items() if v == value), None)


def time_string(x):
    """Takes in number of seconds and returns formatted string"""
    # Make sure x is a whole number
    x = int(np.round(x))

    # Pick units based on value of x
    if x < 60:
        # less than 1 min
        return('{} seconds'.format(x))
    elif x < 60*60:
        # less than 1 hour
        m, s = divmod(x, 60)
        return('{} minutes {} seconds'.format(m, s))
    elif x < 60*60*24:
        # less than 1 day
        h, r = divmod(x, 3600)
        m, s = divmod(r, 60)
        return('{} hours {} minutes {} seconds'.format(h,m,s))
    else:
        # greater than 1 day
        d, r1 = divmod(x, 86400)
        h, r2 = divmod(r1, 3600)
        m, s = divmod(r2, 60)
        return('{} days {} hours {} minutes {} seconds'.format(d,h,m,s))


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
    city = None
    while not city:
        print('\nWhat city would you like to summarize?\n'\
              '\tOptions:\n\tChicago,\n\tNew York City,\n\tWashington\n')
        foo = input('City:  ')

        # Check input
        if foo.lower() in ['chicago', 'chi']:
            city = 'chicago'
        elif foo.lower() in ['new york city', 'new york', 'nyc', 'ny']:
            city = 'new york city'
        elif foo.lower() in ['washington', 'washington dc', 'dc']:
            city = 'washington'
        else:
            print('\nInvailid Input. Please try again:\n')

    # get user input for month (all, january, february, ... , june)
    month = None
    while not month:
        print('\nIs there a particular month you would like to summarize?'\
              '\nIf not, enter: \'None\'\n')
        foo = input('Month:  ')
        month_error = '\nThis data set only has records from January to June.\nPlease make another selection.\n'

        # Check input
        if foo.lower() in ['january', 'jan']:
            month  = 'january'
        elif foo.lower() in ['february', 'feb']:
            month = 'february'
        elif foo.lower() in ['march', 'mar']:
            month = 'march'
        elif foo.lower() in ['april', 'apr']:
            month = 'april'
        elif foo.lower() in ['may']:
            month = 'may'
        elif foo.lower() in ['june', 'jun']:
            month = 'june'
        elif foo.lower() in ['july', 'jul']:
            print(month_error)
        elif foo.lower() in ['august', 'aug']:
            print(month_error)
        elif foo.lower() in ['september', 'sep']:
            print(month_error)
        elif foo.lower() in ['october', 'oct']:
            print(month_error)
        elif foo.lower() in ['november', 'nov']:
            print(month_error)
        elif foo.lower() in ['december', 'dec']:
            print(month_error)
        elif foo.lower() in ['none', 'all', 'no', 'n']:
            month = 'all'
        else:
            print('\nInvailid Input. Please try again:\n')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = None
    while not day:
        print('\nIs there a particular day of the week you would like to summarize?'\
              '\nIf not, enter: \'None\'\n')
        foo = input('Day of the Week:  ')

        # Check input
        if foo.lower() in ['sunday', 'sun', 'su']:
            day  = 'sunday'
        elif foo.lower() in ['monday', 'mon', 'mo']:
            day = 'monday'
        elif foo.lower() in ['tuesday', 'tue', 'tu']:
            day = 'tuesday'
        elif foo.lower() in ['wednesday', 'wed', 'we']:
            day = 'wednesday'
        elif foo.lower() in ['thursday', 'thu', 'th']:
            day = 'thursday'
        elif foo.lower() in ['friday', 'fri', 'fr']:
            day = 'friday'
        elif foo.lower() in ['saturday', 'sat', 'sa']:
            day = 'saturday'
        elif foo.lower() in ['none', 'all', 'no', 'n']:
            day = 'all'
        else:
            print('\nInvailid Input. Please try again:\n')

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
    # Read csv to datafram
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # Filter data based on month
    if month != 'all':
        df = df[df['Start Time'].dt.month == MONTH_DATA[month]]

    # Filter data based on day of the week
    if day != 'all':
        df = df[df['Start Time'].dt.weekday == DAY_DATA[day]]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    pop_month = df['Start Time'].dt.month.mode()
    for i in pop_month:
        pop_month_string = find_key(MONTH_DATA, i).title()
        print('Most Common Month: ', pop_month_string)

    # display the most common day of week
    pop_day = df['Start Time'].dt.weekday.mode()
    for i in pop_day:
        pop_day_string = find_key(DAY_DATA, i).title()
        print('Most Common Day: ', pop_day_string)

    # display the most common start hour
    pop_hour = df['Start Time'].dt.hour.mode()
    for i in pop_hour:
        if i == 0:
            disp_hour = 12
            tag = 'am'
        elif i <= 12:
            disp_hour = i
            tag = 'am'
        else:
            disp_hour = i - 12
            tag = 'pm'
        print('Most Common Hour: {}{}'.format(disp_hour,tag))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    pop_start = df['Start Station'].mode()
    for i in pop_start:
        print('Most popular Start Station: ',i)

    # display most commonly used end station
    pop_end = df['End Station'].mode()
    for i in pop_end:
        print('Most popular End Station: ',i)

    # display most frequent combination of start station and end station trip
    full_trip = df['Start Station'] + ' --> ' + df['End Station']
    pop_trip = full_trip.mode()
    for i in pop_trip:
        print('Most popular trip: ', i)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total = df['Trip Duration'].sum()
    print('Total travel time: ', time_string(total))

    # display mean travel time
    avg = df['Trip Duration'].mean()
    print('Average travel time: ', time_string(avg))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type = df.groupby('User Type')['User Type'].count()
    print('Count by user type:')
    for i in user_type.index:
        print('\t{} : {}'.format(i,user_type[i]))

    # skip this section if city is washington
    if city != 'washington':
        # Display counts of gender
        gender = df.groupby('Gender')['Gender'].count()
        print('Count by gender:')
        for i in gender.index:
            print('\t{} : {}'.format(i,gender[i]))

        # Display earliest, most recent, and most common year of birth
        print('Earliest birth year: ', int(df['Birth Year'].min()))
        print('Most recent birth year: ', int(df['Birth Year'].max()))
        print('Most common birth year: ', int(df['Birth Year'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def show_raw(df):
    """Display raw data if prompted by the user"""
    index = 0
    step = 5
    while True:
        foo = input('\nWould you like to see the raw data? (y/n)\n')
        if foo.lower() in ['n', 'no', 'nope']:
            return
        elif foo.lower() in ['y', 'yes', 'please']:
            data_flag = False
            while True:
                if index < len(df) - step:
                    d = step
                else:
                    data_flag = True
                    d = len(df) - index

                print(df.iloc[range(index, index + d)])
                index += step

                if data_flag:
                    print('\nEnd of dataframe reached.\n')
                    return
                else:
                    next_flag = False
                    while not next_flag:
                        bar = input('\nDisplay next set of rows? (y/n)\n')
                        if bar.lower() in ['y', 'yes', 'please']:
                            next_flag = True
                        elif bar.lower() in['n', 'no', 'nope']:
                            return
                        else:
                            print('\n Invaid input. Try again,\n')
        else:
            print('\n Invaid input. Try again,\n')


def main():
    end_flag = False
    while not end_flag:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        show_raw(df)

        choice = False
        while not choice:
            restart = input('\nWould you like to restart? (y/n)\n')
            if restart.lower() in ['y', 'yes']:
                choice = True
            elif restart.lower() in ['n', 'no']:
                end_flag = True
                choice = True
            else:
                print('\nInvailid Input. Please try again:\n')

if __name__ == "__main__":
	main()
