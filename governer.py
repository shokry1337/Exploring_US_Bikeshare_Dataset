import pandas as pd
import lists

class calculator:
    def __init__(self, df, filter) -> None:
        self.df = df.copy()
        self.filter = filter

        df.fillna(method='ffill', inplace=True)
        self.df['Start Time'] = pd.to_datetime(self.df['Start Time'])
        self.df['Month'] = self.df['Start Time'].dt.month_name()
        self.df['Day'] = self.df['Start Time'].dt.day_name()
        self.df['Hour'] = self.df['Start Time'].dt.hour
        pass

    def get_0(self) -> str:
        """Returns the most common month, day, and hour."""

        if self.filter[1] == 0:
            self.df = self.df[self.df['Month'] == lists.months[self.filter[2]]]
            s = f"    Most common day = '{self.df['Day'].mode()[0]}'\n"
        elif self.filter[1] == 1:
            self.df = self.df[self.df['Day'] == lists.days[self.filter[2]]]
            s = ''
        elif self.filter[1] == 2:
            s = f"    Most common month = '{self.df['Month'].mode()[0]}'\n    Most common day = '{self.df['Day'].mode()[0]}'\n"

        most_common_hour = self.df['Hour'].mode()[0]
        if most_common_hour > 12:
            s += f"    Most common hour = '{(most_common_hour - 12)} PM'"
        else:
            s += f"    Most common hour = '{most_common_hour} AM'"

        return s

    def get_1(self) -> str:
        """Returns the most common start station, end station, and trip."""

        self.df.loc[:, 'Combination'] = self.df['Start Station'] + ' -> ' + self.df['End Station']

        s = f"    Most common start station = '{self.df['Start Station'].mode()[0]}'\n" +\
            f"    Most common end station = '{self.df['End Station'].mode()[0]}'\n" +\
            f"    Most common trip = '{self.df['Combination'].mode()[0]}'"

        return s

    def get_2(self) -> str:
        """Retruns both total, and average travel durations."""

        s = f"    Average travel time = '{round(self.df['Trip Duration'].mean(), 2)}' seconds\n" +\
            f"    Total travel time = '{round((self.df['Trip Duration'].sum() / 60 / 60 / 24), 2)}' days"

        return s

    def get_3(self) -> str:
        """Returns counts of subscribers, customers, males/females, and the earliest/latest and most common birth year."""

        s = f"    Count of subscribers = '{(self.df['User Type'] == 'Subscriber').sum()}'\n" +\
            f"    Count of customers = '{(self.df['User Type'] == 'Customer').sum()}'"

        if self.filter[0] != 2:
            s += f"\n    Count of males = '{(self.df['Gender'] == 'Male').sum()}'\n" +\
                f"    Count of females = '{(self.df['Gender'] == 'Female').sum()}'\n" +\
                f"    Earliest birth year = '{round(self.df['Birth Year'].min())}'\n" +\
                f"    Latest birth year = '{round(self.df['Birth Year'].max())}'\n" +\
                f"    Most common birth year = '{round(self.df['Birth Year'].mode()[0])}'"

        return s
