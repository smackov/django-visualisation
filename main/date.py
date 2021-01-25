"""Class Date.

The class can returns dates in vary formats."""


from datetime import date, timedelta
from dateutil.relativedelta import relativedelta


class Date:
    "Proccess date in needest format"
    
    @classmethod
    def first_day_of_current_week(cls):
        "Find first day of a current week."

        first_day = date.today() - timedelta(days=date.today().weekday())
        return first_day

    @classmethod
    def current_week_dates(cls):
        "Find first and last dates of a current week."

        first_day = date.today() - timedelta(days=date.today().weekday())
        last_day = first_day + timedelta(days=6)
        return first_day, last_day

    @classmethod
    def last_week_dates(cls):
        "Find first and last dates of a last week."

        first_day = date.today() - timedelta(days=date.today().weekday() + 7)
        last_day = first_day + timedelta(days=6)
        return first_day, last_day

    @classmethod
    def current_month_dates(cls):
        "Find first and last dates of a current month."
        
        first_day = date.today() + relativedelta(day=1)
        last_day = date.today() + relativedelta(day=1, months=+1, days=-1)
        
        return first_day, last_day

    @classmethod
    def last_month_dates(cls):
        "Find first and last dates of a last month."
        
        first_day = date.today() + relativedelta(day=1, months=-1)
        last_day = date.today() + relativedelta(day=1, days=-1)
        
        return first_day, last_day
