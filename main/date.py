"""Class Date.

The class can returns dates in vary formats."""


from datetime import date, timedelta


class Date:
    "Proccess date in needest format"

    __TODAY = date.today()
    __MONTH = __TODAY.month
    __YEAR = __TODAY.year

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

        first_day = date(year=cls.__YEAR, month=cls.__MONTH, day=1)
        last_day = (date(year=cls.__YEAR, month=cls.__MONTH+1, day=1)
                    - timedelta(days=1))
        return first_day, last_day

    @classmethod
    def last_month_dates(cls):
        "Find first and last dates of a last month."

        first_day = date(year=cls.__YEAR, month=cls.__MONTH-1, day=1)
        last_day = (date(year=cls.__YEAR, month=cls.__MONTH, day=1)
                    - timedelta(days=1))
        return first_day, last_day
