
from django.db.models import Sum

from .models import Track
from .date import Date


class UserTracks:
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
    
    @staticmethod
    def __pomodoros_to_hours(work_time, with_fraction_part=False):
        """Transfer pomodoros to hours.
        
        1 hour = 2 pomodoros (2*30 min)"""
        
        whole_part = work_time // 2
        
        if with_fraction_part:
            fraction_part = (work_time % 2) * 0.5        
            if not fraction_part == 0:
                return whole_part + fraction_part
            
        return whole_part

    def __count_total_work_time(self, period=None):
        "This func evaluates all work time for a given period"

        if period:
            tracks = self.__query_tracks_for_period(period)
        else:
            tracks = self.__tracks
            
        work_time = tracks.aggregate(Sum('duration'))['duration__sum']
        print('__count_total_work_time')

        if work_time == None:
            return 0
        
        work_time = self.__pomodoros_to_hours(work_time)
        
        return work_time

    def work_time_current_week(self):
        "Return total work time for current week."

        period = Date.current_week_dates()
        return self.__count_total_work_time(period)

    def work_time_current_month(self):
        "Return total work time for current month."

        period = Date.current_month_dates()
        return self.__count_total_work_time(period)

    def work_time_last_month(self):
        "Return total work time for last month."

        period = Date.last_month_dates()
        return self.__count_total_work_time(period)

    def work_time_for_ever(self):
        "Return total work time for last month."
        
        return self.__count_total_work_time()
