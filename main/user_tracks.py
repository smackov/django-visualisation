from datetime import timedelta

from django.db.models import Sum

from .models import Track
from .date import Date


class UserTracks:
    "Class queries all tracks related with added user and processes it."

    def __init__(self, user):
        self.__user = user
        self.__tracks = Track.objects.filter(author=user)

    def __query_tracks_for_period(self, period):
        "Query the tracks from the starting day to the trailing day."
        starting_day = period[0]
        trailing_day = period[1]
        tracks = self.__tracks.filter(
            date__gte=starting_day
        ).exclude(
            date__gt=trailing_day
        )
        return tracks

    @staticmethod
    def __pomodoros_to_hours(work_time, with_fraction_part=False):
        """Transfer pomodoros to hours.

        1 hour = 2 pomodoros (2*30 min)
        """
        whole_part = work_time // 2
        if with_fraction_part:
            fraction_part = (work_time % 2) * 0.5
            if not fraction_part == 0:
                return whole_part + fraction_part
        return whole_part

    def __count_total_work_time(self, period=None, tracks=None,
                                with_fraction_part=False):
        "This func evaluates all work time for a given period"
        if tracks == None:
            if period:
                tracks = self.__query_tracks_for_period(period)
            else:
                tracks = self.__tracks
        work_time = tracks.aggregate(Sum('duration'))['duration__sum']
        if work_time == None:
            return 0
        work_time = self.__pomodoros_to_hours(work_time, with_fraction_part)
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

    def current_week_detail(self):
        "Return the dictionary with the days statistic"
        day = Date.first_day_of_current_week()
        context = []
        
        # Populate context by week days
        for number_day in range(1, 8):
            # Get tracks and order them by lowering duraton
            tracks = self.__query_tracks_for_period((day, day))
            tracks = tracks.order_by('-duration')
            # Count total worked time in hours
            total_work_time = self.__count_total_work_time(
                tracks=tracks, with_fraction_part=True)
            # Add day tracks and worked time to the context
            new_day = {'weekday': day.strftime('%A'),
                       'total_work_time': total_work_time,
                       'tracks': tracks}
            context.append(new_day)
            day += timedelta(days=1)

        return context
