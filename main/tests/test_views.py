import datetime

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

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
        
        self.assertEqual(response.context['week_data']['worked_time']['hours'], 18)
        response_status_complete = response.context['week_data']['status_complete'] 
        self.assertEqual(str(response_status_complete), '{:.0%}'.format(18/30).strip('%'))
        