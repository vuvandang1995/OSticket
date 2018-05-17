from django.test import TestCase, SimpleTestCase, Client
from .models import *
# Create your tests here.


class TestModels(TestCase):
    def setUp(self):
        self.time_start = timezone.now()
        self.time_end = timezone.now() + timezone.timedelta(days=7)
        self.user = Users.objects.create(fullname="Nguyen Dung",
                             email="NVD@gmail.com",
                             username="dung1",
                             password="1",
                             created=self.time_start)
        self.topic = Topics.objects.creats(name="django",
                                           description="django problem")
        self.ticket = Tickets.objects.create(title="hi",
                                             content="how to play",
                                             sender=self.user,
                                             datestart=self.time_start,
                                             dateend=self.time_end,
                                            )

    def test_get_user(self):
        self.assertEqual(get_user("dung1"), Users.objects.get(username="dung1"))
        self.assertEqual(get_user("dung2"), None)

    def test_countk(self):
        pass


