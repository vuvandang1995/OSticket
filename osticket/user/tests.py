from django.test import TestCase, SimpleTestCase, Client
from .models import *
# Create your tests here.


class TestModels(TestCase):
    def setUp(self):
        from django.utils import timezone
        self.time_start = timezone.now()
        self.time_end = timezone.now() + timezone.timedelta(days=7)
        self.user = [Users.objects.create(fullname="Nguyen Viet K",
                                          email="v0@gmail.com",
                                          username="viet0",
                                          password="1",
                                          created=self.time_start,
                                          status=1),
                     Users.objects.create(fullname="Nguyen Viet M",
                                          email="v1@gmail.com",
                                          username="viet1",
                                          password="1",
                                          created=self.time_start)
                     ]
        self.topic = Topics.objects.create(name="django",
                                           description="django problem")
        self.ticket = [Tickets.objects.create(title="hi",
                                              content="how to play",
                                              topicid=self.topic,
                                              sender=self.user[0],
                                              datestart=self.time_start,
                                              dateend=self.time_end),
                       Tickets.objects.create(title="hello",
                                              content="play the game",
                                              topicid=self.topic,
                                              sender=self.user[0],
                                              datestart=self.time_start,
                                              dateend=self.time_end,
                                              status=1),
                       Tickets.objects.create(title="ciao",
                                              content="game",
                                              topicid=self.topic,
                                              sender=self.user[0],
                                              datestart=self.time_start,
                                              dateend=self.time_end,
                                              status=2),
                       Tickets.objects.create(title="ni hao",
                                              content="the game",
                                              topicid=self.topic,
                                              sender=self.user[0],
                                              datestart=self.time_start,
                                              dateend=self.time_end,
                                              status=3)]
        self.agent = [Agents.objects.create(fullname='Nguyen Dung K',
                                            email="d0@gmail.com",
                                            username="dung0",
                                            password="1"),
                      Agents.objects.create(fullname='Nguyen Dung M',
                                            email="d1@gmail.com",
                                            username="dung1",
                                            password="1"),
                      Agents.objects.create(fullname='Nguyen Dung H',
                                            email="d2@gmail.com",
                                            username="dung2",
                                            password="1"),
                      Agents.objects.create(fullname='Nguyen Dung B',
                                            email="d3@gmail.com",
                                            username="dung3",
                                            password="1",
                                            admin=1),
                      Agents.objects.create(fullname='Nguyen Dung F',
                                            email="d4@gmail.com",
                                            username="dung4",
                                            password="1",
                                            status=0)
                      ]
        TicketAgent.objects.create(agentid=self.agent[0], ticketid=self.ticket[1])
        TicketAgent.objects.create(agentid=self.agent[0], ticketid=self.ticket[3])
        TicketAgent.objects.create(agentid=self.agent[1], ticketid=self.ticket[2])
        TicketAgent.objects.create(agentid=self.agent[1], ticketid=self.ticket[3])
        TicketAgent.objects.create(agentid=self.agent[2], ticketid=self.ticket[3])

    def test_get_user(self):
        self.assertEqual(get_user("viet0"), self.user[0])
        self.assertEqual(get_user("dung2"), None)

    def test_count_tk(self):
        self.assertEqual(count_tk("dung0"), (1, 1))
        self.assertEqual(count_tk("dung2"), (1, 0))
        self.assertEqual(count_tk("hehe"), None)

    def test_list_hd(self):
        self.assertEqual(list_hd(self.ticket[0]), ["dung0", "dung1", "dung2", "dung3", "dung4"])
        self.assertEqual(list_hd(self.ticket[1]), ["dung1", "dung2", "dung3", "dung4"])
        self.assertEqual(list_hd(self.ticket[2]), ["dung0", "dung2", "dung3", "dung4"])
        self.assertEqual(list_hd(self.ticket[3]), ["dung3", "dung4"])

    def test_get_agent(self):
        self.assertEqual(get_agent("dung0"), self.agent[0])
        self.assertEqual(get_agent("dung1"), self.agent[1])
        self.assertEqual(get_agent("dungdung"), None)

    def test_get_user_email(self):
        self.assertEqual(get_user_email("v0@gmail.com"), self.user[0])
        self.assertEqual(get_user_email("hoho@gmail.com"), None)

    def test_active(self):
        self.assertEqual(active(self.user[0]), True)
        self.assertEqual(active(self.user[1]), False)

    def test_authenticate_user(self):
        self.assertEqual(authenticate_user("viet0", "1"), self.user[0])
        self.assertEqual(authenticate_user("viet0", "123"), None)
        self.assertEqual(authenticate_user("vietviet", "123"), None)
        self.assertEqual(authenticate_user("viet1", "1"), None)

    def test_authenticate_agent(self):
        self.assertEqual(authenticate_agent("dung0", "1"), 0)
        self.assertEqual(authenticate_agent("dung0", "123"), None)
        self.assertEqual(authenticate_agent("dung0000", "1"), None)
        self.assertEqual(authenticate_agent("dung3", "1"), 1)
        self.assertEqual(authenticate_agent("dung4", "1"), None)


class TestUrls(TestCase):
    def setUp(self):
        self.client = Client()
        self.time_start = timezone.now()
        self.user = [Users.objects.create(fullname="Nguyen Viet K",
                                          email="v0@gmail.com",
                                          username="viet0",
                                          password="1",
                                          created=self.time_start,
                                          status=1),
                     Users.objects.create(fullname="Nguyen Viet M",
                                          email="v1@gmail.com",
                                          username="viet1",
                                          password="1",
                                          created=self.time_start)
                     ]

    def test_login(self):
        response = self.client.post('/', {'username': 'viet0', 'password': '1'})
        self.assertEqual(response.status_code, 302)








