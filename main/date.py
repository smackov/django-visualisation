"""Class Date.

The class can returns dates in vary formats."""


from datetime import date, timedelta
from dateutil.relativedelta import relativedelta


class Date:
    "Proccess date in needest format"

    __TODAY = date.today()
    __MONTH = __TODAY.month
    __YEAR = __TODAY.year
    
    @classmethod
    def first_day_of_current_week(cls):
        "Find first day of a current week."

        first_day = cls.__TODAY - timedelta(days=cls.__TODAY.weekday())
        return first_day

    @classmethod
    def current_week_dates(cls):
        "Find first and last dates of a current week."

        first_day = cls.__TODAY - timedelta(days=cls.__TODAY.weekday())
        last_day = first_day + timedelta(days=6)
        return first_day, last_day

    @classmethod
    def last_week_dates(cls):
        "Find first and last dates of a last week."

        first_day = cls.__TODAY - timedelta(days=cls.__TODAY.weekday() + 7)
        last_day = first_day + timedelta(days=6)
        return first_day, last_day

    @classmethod
    def current_month_dates(cls):
        "Find first and last dates of a current month."
        
        first_day = cls.__TODAY + relativedelta(day=1)
        print('\n\n Current month')
        print('First day: ', first_day)
        last_day = cls.__TODAY + relativedelta(day=1, months=+1, days=-1)
        print('Last day: ', first_day)
        
        return first_day, last_day

    @classmethod
    def last_month_dates(cls):
        "Find first and last dates of a last month."
        
        first_day = cls.__TODAY + relativedelta(day=1, months=-1)
        print('\n\n Last month')
        print('First day: ', first_day)
        last_day = cls.__TODAY + relativedelta(day=1, days=-1)
        print('Last day: ', first_day)
        
        return first_day, last_day
