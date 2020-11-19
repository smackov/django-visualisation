from django.test import TestCase
from django.contrib.auth.models import User

from main.models import Task

class TaskModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Set up non-modified objects used by all test methods."""
        
        "Create 2 users"
        test_user_1 = User.objects.create_user('Test_user_1', 'myemail@crazymail.com',
                                 'password')
        test_user_2 = User.objects.create_user('Test_user_2', 'myemail@crazymail.com',
                                 'password')
        
        "Create the first task"
        Task.objects.create(name='English', author=test_user_1)

        "Create 5 new tasks"
        for i in range(5):
            if i % 2 == 0:
                user = test_user_1
            else:
                user = test_user_2
            
            Task.objects.create(name='Task #{}'.format(i), author=user)
        
    def test_name_label(self):
        task = Task.objects.get(id=1)
        field_label = task._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')
        
    def test_author_label(self):
        task = Task.objects.get(id=1)
        field_label = task._meta.get_field('author').verbose_name
        self.assertEquals(field_label, 'author')

    def test_name_max_length(self):
        task = Task.objects.get(id=1)
        max_length = task._meta.get_field('name').max_length
        self.assertEquals(max_length, 40)

    def test_object_name(self):
        task = Task.objects.get(id=1)
        expected_object_name = task.name
        self.assertEquals(expected_object_name, str(task))
        
    def test_ordering(self):
        "Test the task ordering: ordering = ['author', 'name']"
        
        tasks = Task.objects.all()
        list_of_tasks = list(tasks)
        
        list_of_tasks_sorted = sorted(list_of_tasks, 
                                      key=lambda task: task.name)
        
        list_of_tasks_sorted = sorted(list_of_tasks_sorted, 
                                      key=lambda task: task.author.__str__())
        
        self.assertEquals(list_of_tasks, list_of_tasks_sorted)

