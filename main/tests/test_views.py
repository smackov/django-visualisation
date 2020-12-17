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

        "Create Rate object"
        Rate.objects.create(name="Good", rate=1)

        "Create 2 new tasks for each users"
        for user in (test_user_1, test_user_2):
            for i in range(1, 3):
                Task.objects.create(name='Task #{} belongs {}'.format(
                    i, user.username), author=user)

        "Create 5 tracks for current week for each user"
        for user in (test_user_1, test_user_2):
            factor = 1 if user == test_user_1 else 2
            user_tasks = list(Task.objects.filter(author=user))
            rate = Rate.objects.get(id=1)
            for n in range(1, 11):
                random_number = n % 2
                task = user_tasks[random_number]
                duration = factor
                date = datetime.date.today() - datetime.timedelta(days=n)
                Track.objects.create(
                    author=user, id_task=task, duration=duration, 
                    id_rate=rate, date=date
                )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/')
        self.assertAlmostEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, 'main/index.html')
