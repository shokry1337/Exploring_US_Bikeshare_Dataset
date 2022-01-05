# The program could still use alot of optimization to improve performance and code readability.
import os
import time
import pandas as pd

# A group of variables that are used throughout the program.
filter = []
filter_settings, df, unmodified_df = None, None, None
list_of_filenames = [f'chicago.csv', f'new_york_city.csv', f'washington.csv']
list_of_cities = ['Chicago', 'New York', 'Washington']
list_of_months = ['January', 'February', 'March', 'April', 'May', 'June']
list_of_days = ['Sunday', 'Monday', 'Tuesday',
                'Wednesday', 'Thursday', 'Friday', 'Saturday']

def clear():
    """Clears the terminal as a mean to improve output readability."""
    os.system('clear')

def parse_input(i, r):
    """Validates that the user input is within the 'selection' range, and returns it as an integer."""
    if i.isnumeric():
        if int(i) in r:
            return int(i)
        else:
            return -1
    else:
        return -1

def choose_filter():
    """The backbone of the program; allows for a bug-less user interaction to choose filters."""
    clear()
    
    # Sets the scope of the variable 'filter' to 'global'.
    global filter

    if len(filter) == 0:
        print("Which city would you like to explore its data?\nType '1' for Chicago, '2' for New York, or '3' for Washington.")
        i = parse_input(input(), range(1, 4))
        if i != -1:
            filter.append(i)
        choose_filter()
    elif len(filter) == 1:
        print("How would you like to filter the data?\nType '1' for month, '2' for day, or '3' for no filters.")
        i = parse_input(input(), range(1, 4))
        if i != -1:
            filter.append(i)
        choose_filter()
    elif len(filter) == 2:
        if filter[1] == 1:
            print("Which month?\nType '1' for January, '2' for February, '3' for March, '4' for April, '5' for May, or '6' for June.")
            i = parse_input(input(), range(1, 7))
            if i != -1:
                filter.append(i)
            else:
                choose_filter()
        elif filter[1] == 2:
            print("Which day?\nType '1' for 'Sunday', '2' for Monday, '3' for Tuesday, '4' for Wednesday, '5' for Thursday, '6' for Friday, or '7' for Saturday.")
            i = parse_input(input(), range(1, 8))
            if i != -1:
                filter.append(i)
            else:
                choose_filter()

def confirm_filter():
    """Allows the user to confirm the chosen filters, or reset the program to start over."""
    clear()
   
    global filter, filter_settings, df
   
    filter_settings = "Filter settings:\n    City = '{}'".format(
        list_of_cities[filter[0] - 1])
    if filter[1] == 1:
        filter_settings += "\n    Month = '{}'".format(
            list_of_months[filter[2] - 1])
    elif filter[1] == 2:
        filter_settings += "\n    Day = '{}'".format(
            list_of_days[filter[2] - 1])
    
    print(filter_settings)
    print("Type '1' to confirm, or '2' to reset.")
    
    i = parse_input(input(), range(1, 3))
    if i == -1:
        confirm_filter()
    elif i == 1:
        clear()
        cal_1()
        cal_2()
        cal_3()
        cal_4()
        print('-' * 25)
        finale(0)
    elif i == 2:
        filter = []
        main()

def cal_1():
    """Calculates the most common month, day, and hour."""
    global filter_settings, df, unmodified_df
  
    print(filter_settings)
    print('-' * 25)
    print('Calculating popular times of travel...')

    start_time = time.time()
    df = pd.read_csv(list_of_filenames[filter[0] - 1])
    unmodified_df = df.copy()
    df.fillna(method='ffill', inplace=True)
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month_name()
    df['Day'] = df['Start Time'].dt.day_name()
    df['Hour'] = df['Start Time'].dt.hour

    if filter[1] == 1:
        df = df[df['Month'] == list_of_months[filter[2] - 1]]
        s = "    Most common day = '{}'\n".format(df['Day'].mode()[0])
    elif filter[1] == 2:
        df = df[df['Day'] == list_of_days[filter[2] - 1]]
        s = ''
    elif filter[1] == 3:
        s = "    Most common month = '{}'\n    Most common day = '{}'\n".format(
            df['Month'].mode()[0], df['Day'].mode()[0])

    most_common_hour = df['Hour'].mode()[0]
    if most_common_hour > 12:
        s += "    Most common hour = '{} PM'".format(most_common_hour - 12)
    else:
        s += "    Most common hour = '{} AM'".format(most_common_hour)

    print(s)
    print("This took '{}' seconds.".format(round(time.time() - start_time, 2)))

def cal_2():
    """Calculates the most common start station, end station, and trip."""
    global df
    
    print('-' * 25)
    print('Calculating popular stations and trip...')

    start_time = time.time()
    df['Combination'] = df['Start Station'] + ' -> ' + df['End Station']

    print("    Most common start station = '{}'".format(
        df['Start Station'].mode()[0]))
    print("    Most common end station = '{}'".format(
        df['End Station'].mode()[0]))
    print("    Most common trip = '{}'".format(df['Combination'].mode()[0]))
    print("This took '{}' seconds.".format(round(time.time() - start_time, 2)))

def cal_3():
    """Calculates both total, and average travel durations."""
    global df

    print('-' * 25)
    print('Calculating trip duration...')

    start_time = time.time()

    print("    Total travel time = '{:.2f}' days".format(
        df['Trip Duration'].sum() / 60 / 60 / 24))
    print("    Average travel time = '{:.2f}' seconds".format(
        df['Trip Duration'].mean()))
    print("This took '{}' seconds.".format(round(time.time() - start_time, 2)))

def cal_4():
    """Calculates the count of subscribers, customers, males, females, and the earliest / latest / most common birth year."""
    global df, filter

    print('-' * 25)
    print('Calculating user information...')

    start_time = time.time()

    print("    Count of subscribers = '{}'".format(
        (df['User Type'] == 'Subscriber').sum()))
    print("    Count of customers = '{}'".format(
        (df['User Type'] == 'Customer').sum()))

    if filter[0] == 1 or filter[0] == 2:
        print("    Count of males = '{}'".format(
            (df['Gender'] == 'Male').sum()))
        print("    Count of females = '{}'".format(
            (df['Gender'] == 'Female').sum()))
        print("    Earliest birth year = '{}'".format(
            int(df['Birth Year'].min())))
        print("    Latest birth year = '{}'".format(
            int(df['Birth Year'].max())))
        print("    Most common birth year = '{}'".format(
            int(df['Birth Year'].mode()[0])))

    print("This took '{:.2f}' seconds.".format(time.time() - start_time))

def finale(index):
    """Enables the user browse raw data 5 rows a time."""
    global filter

    if index == 0:
        print("Would you like to see 5 rows of raw data?\nType '1' to confirm, '2' to reset, or '3' to quit.")
    else:
        print("Would you like to see 5 /more/ rows of raw data?\nType '1' to confirm, '2' to reset, or '3' to quit.")

    i = parse_input(input(), range(1, 4))
    if i == -1:
        clear()
        finale(index)
    elif i == 1:
        print(unmodified_df.iloc[index: index + 5, :])
        finale(index + 5)
    elif i == 2:
        filter = []
        main()
    elif i == 3:
        clear()

def main():
    """The main function."""
    choose_filter()
    confirm_filter()

# Incase I decided to move the calculation functions to a separate .py model.
if __name__ == '__main__':
    main()
    