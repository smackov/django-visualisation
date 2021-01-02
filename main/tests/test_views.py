import datetime
from dateutil.relativedelta import relativedelta

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models import Sum

from main.models import Rate, Task, Track


class IndexTest(TestCase):
    "The test of index view"

    @classmethod
    def setUpTestData(cls):
        pass

    def setUp(self):
        "Create 2 users"
        test_user_1 = User.objects.create_user(
            'Test_user_1', 'myemail@crazymail.com', 'password')
        test_user_2 = User.objects.create_user(
            'Test_user_2', 'myemail@crazymail.com', 'password')

        test_user_1.save()
        test_user_2.save()

        "Create Rate object"
        rate = Rate.objects.create(name="Good", rate=1)

        "Create tasks for test_user_1"
        task_1 = Task.objects.create(name='English', author=test_user_1)
        task_2 = Task.objects.create(name='German', author=test_user_1)
        task_3 = Task.objects.create(name='Programming', author=test_user_1)

        "Create tracks for test_user_1"
        today = datetime.date.today()
        # Monday and thursday of current week
        monday = today - datetime.timedelta(days=today.weekday())
        thursday = monday + datetime.timedelta(days=1)
        # Tracks of monday
        Track.objects.create(author=test_user_1, id_task=task_1, duration=5,
                             id_rate=rate, date=monday)
        Track.objects.create(author=test_user_1, id_task=task_1, duration=3,
                             id_rate=rate, date=monday)
        Track.objects.create(author=test_user_1, id_task=task_2, duration=10,
                             id_rate=rate, date=monday)
        # Tracks of thursday
        Track.objects.create(author=test_user_1, id_task=task_1, duration=5,
                             id_rate=rate, date=thursday)
        Track.objects.create(author=test_user_1, id_task=task_1, duration=3,
                             id_rate=rate, date=thursday)
        Track.objects.create(author=test_user_1, id_task=task_2, duration=10,
                             id_rate=rate, date=thursday)

        # Create the same tracks in the same days but in 1 week ago
        monday = monday - datetime.timedelta(days=6)
        thursday = thursday - datetime.timedelta(days=6)
        # Tracks of monday
        Track.objects.create(author=test_user_1, id_task=task_1, duration=5,
                             id_rate=rate, date=monday)
        Track.objects.create(author=test_user_1, id_task=task_1, duration=3,
                             id_rate=rate, date=monday)
        Track.objects.create(author=test_user_1, id_task=task_2, duration=10,
                             id_rate=rate, date=monday)
        # Tracks of thursday
        Track.objects.create(author=test_user_1, id_task=task_1, duration=5,
                             id_rate=rate, date=thursday)
        Track.objects.create(author=test_user_1, id_task=task_1, duration=3,
                             id_rate=rate, date=thursday)
        Track.objects.create(author=test_user_1, id_task=task_2, duration=10,
                             id_rate=rate, date=thursday)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/')
        self.assertAlmostEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, 'main/index.html')

    def test_view_with_logged_in_user_uses_correct_template(self):
        login = self.client.login(username='Test_user_1', password='password')
        response = self.client.get(reverse('index'))
        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'Test_user_1')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)
        # Check we used correct template
        self.assertTemplateUsed(response, 'main/index.html')

    def test_context_week_status_value(self):
        login = self.client.login(username='Test_user_1', password='password')
        response = self.client.get(reverse('index'))
        # Check that total worked time in the current week is 18 hours
        self.assertEqual(
            response.context['week_data']['worked_time']['hours'], 18)
        # Check status of completing the weed goal
        response_status_complete = response.context['week_data']['status_complete']
        self.assertEqual(str(response_status_complete),
                         '{:.0%}'.format(18/30).strip('%'))

    def test_context_last_4_weeks_status(self):
        login = self.client.login(username='Test_user_1', password='password')
        response = self.client.get(reverse('index'))
        # Only the first week has tracks with total worked time 18 hours
        for week in response.context['last_weeks'][:1]:
            # Check that total worked time in the week is 18 hours
            self.assertEqual(week['worked_time']['hours'], 18)
            # Check status of completing the weed goal
            self.assertEqual(str(week['status_complete']),
                             '{:.0%}'.format(18/30).strip('%'))
        # Others three weeks don't have any tracks
        for week in response.context['last_weeks'][-3:]:
            # Check that total worked time in the week is 18 hours
            self.assertEqual(week['worked_time']['hours'], 0)
            # Check status of completing the weed goal
            self.assertEqual(str(week['status_complete']), '0')

    def test_context_statistic(self):
        login = self.client.login(username='Test_user_1', password='password')
        response = self.client.get(reverse('index'))
        # First and last days of the current month
        first_day_of_current_month = datetime.date.today() + relativedelta(day=1)
        last_day_of_current_month = (datetime.date.today()
                                     + relativedelta(day=1, months=+1, days=-1))
        # Worked time for the current month
        worked_time_for_current_month = Track.objects.filter(
            author=response.context['user']
        ).filter(
            date__gte=first_day_of_current_month
        ).exclude(
            date__gt=last_day_of_current_month
        ).aggregate(
            Sum('duration')
        )
        
        if worked_time_for_current_month['duration__sum'] == None:
            # If there aren't any worked time for current month change
            # worked time value to '0'. Django ORM returns 'None' if 
            # there aren't anything
            worked_time_for_current_month['duration__sum'] = 0
        
        worked_time_for_last_month = 36 - \
            worked_time_for_current_month['duration__sum'] / 2

        # Check total worked time for current week
        self.assertEqual(response.context['statistic']['current_week'], 18)
        # Check total worked time for current month
        self.assertEqual(
            response.context['statistic']['current_month'],
            worked_time_for_current_month['duration__sum']/2)
        # Check total worked time for last month
        self.assertEqual(
            response.context['statistic']['last_month'],
            worked_time_for_last_month)
        # Check total worked time for ever time
        self.assertEqual(response.context['statistic']['for_ever'], 36)
