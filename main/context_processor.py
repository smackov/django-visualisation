from datetime import date

from .models import Quote


def date_day_quote(request):
    """
    The context for all app pages.
    
    Get 3 variables:
     - date in format: 'Saturday 14 November'
     - number day of year (year has 365 days): 234
     - random quote from Quote.objects.
     """
    context = {
        'date': date_today(),
        'number_day': number_day(),
        'quote': Quote.objects.random(),
    }
    return(context)


def date_today():
    """It return a date in accurate for pages format

    date_today() --> 'Saturday 14 November'
    """
    return date.today().strftime('%A %d %B')


def number_day():
    """The number day of year

    if today 01.01.2020 (the first day of year)
    number_day() --> 1

    if today 05.07.2020 (the arbitrary day of year)
    number_day() --> 187

    if today 31.12.2020 (the last day of year)
    number_day() --> 366 (leap year)
    """
    return (date.today().toordinal() -
            date(date.today().year, 1, 1).toordinal() + 1)
