import os
import time
import pandas as pd
from governer import calculator
import lists

filter, filter_settings, df, d_line = [], None, None, ('-' * 25)

def clear():
    """Clears the terminal."""
   
    os.system('clear')

def parse_input(i, limit) -> int:
    """Validates that the user input is within the 'selection' range, and returns it as an integer."""
   
    if i.isnumeric() and (int(i) >= 0) and (int(i) <= limit): return int(i)    
    return -1

def choose_filter():
    """The backbone of the program; allows the user to choose filters."""
   
    clear()
    global filter
    if len(filter) == 0:

        print("Which city would you like to explore its data?\nType '0' for Chicago, '1' for New York, or '2' for Washington.")
        i = parse_input(input(), 2)
        if i != -1: filter.append(i)
        choose_filter()

    elif len(filter) == 1:

        print("How would you like to filter the data?\nType '0' for month, '1' for day, or '2' for no filters.")
        i = parse_input(input(), 2)
        if i != -1: filter.append(i)
        choose_filter()

    elif len(filter) == 2:

        if filter[1] == 0:

            print("Which month?\nType '0' for January, '1' for February, '2' for March, '3' for April, '4' for May, or '5' for June.")
            i = parse_input(input(), 5)
            if i != -1: filter.append(i)
            else: choose_filter()

        elif filter[1] == 1:

            print("Which day?\nType '0' for 'Sunday', '1' for Monday, '2' for Tuesday, '3' for Wednesday, '4' for Thursday, '5' for Friday, or '6' for Saturday.")
            i = parse_input(input(), 6)
            if i != -1: filter.append(i)
            else: choose_filter()

def confirm_filter():
    """Allows the user to confirm the chosen filters, or reset the program to start over."""

    clear()
    global filter, filter_settings
    filter_settings = "Filter settings:\n    City = '{}'".format(lists.cities[filter[0]])
    if filter[1] == 0:
        filter_settings += "\n    Month = '{}'".format(lists.months[filter[2]])
    elif filter[1] == 1:
        filter_settings += "\n    Day = '{}'".format(lists.days[filter[2]])
    
    print(filter_settings)
    print("Type '0' to confirm, or '1' to reset.")
    
    i = parse_input(input(), 1)
    if i == -1: confirm_filter()
    elif i == 0:
        get_and_print()
        print(d_line)
        finale(0)
    elif i == 1:
        filter = []
        main()

def get_and_print():
    clear()
    print(f'{filter_settings}\n' + d_line + '\nLoading data...')
    
    global df, _c
    df = pd.read_csv(lists.filenames[filter[0]])
    _c = calculator(df, filter)

    for i in range(0, 4):
        start_time = time.time()

        if i != 0: print(d_line)
        print(lists.phrases[i])

        print(eval(f'_c.get_{i}()') + f"\nThis took '{round(time.time() - start_time, 2)}' seconds.")

def finale(index):
    """Enables the user to browse raw data 5 rows a time."""
    
    global filter
    if index == 0:
        print("Would you like to see 5 rows of raw data?\nType '0' to confirm, '1' to reset, or '2' to quit.")
    else:
        print("Would you like to see 5 /more/ rows of raw data?\nType '0' to confirm, '1' to reset, or '2' to quit.")

    i = parse_input(input(), 2)
    if i == -1:
        clear()
        finale(index)
    elif i == 0:
        print(df.iloc[index: index + 5, :])
        finale(index + 5)
    elif i == 1:
        filter = []
        main()
    elif i == 2: clear()

def main():
    """The main function."""

    choose_filter()
    confirm_filter()

if __name__ == '__main__':
    main()
