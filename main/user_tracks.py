
from django.db.models import Sum

from .models import Track
from .date import Date


class UserTracks(Date):
    "Class queries all tracks related with added user and processes it."

    def __init__(self, user):
        self.__user = user
        self.__tracks = Track.objects.filter(author=user)
        print('UserTracks class')

    def __query_tracks_for_period(self, period):
        "Query the tracks from the starting day to the trailing day."

        starting_day = period[0]
        trailing_day = period[1]

        tracks = self.__tracks.filter(
            date__gte=starting_day
        ).exclude(
            date__gt=trailing_day
        )
        print('__query_tracks_for_period')
        return tracks

    def __count_total_work_time(self, period):
        "This func evaluates all work time for a given period"

        tracks = self.__query_tracks_for_period(period)
        work_time = tracks.aggregate(Sum('duration'))['duration__sum']
        print('__count_total_work_time')

        if work_time == None:
            return 0

        return work_time

    def work_time_current_week(self):
        "Return total work time for current week."

        period = self.current_week_dates()
        return self.__count_total_work_time(period)

    def work_time_current_month(self):
        "Return total work time for current month."

        period = self.current_month_dates()
        return self.__count_total_work_time(period)
