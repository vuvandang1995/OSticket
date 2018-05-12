# chat/consumers.py
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from user.models import *
from channels.layers import get_channel_layer

dict_chat = {}
list_mess = []
class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        print(self.room_group_name)
        
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

        try:
            list_message = dict_chat[self.room_group_name]
            for listmess in list_message:
                self.send(text_data=json.dumps({
                'message': listmess['message'],
                'who': listmess['who']
            }))
        except:
            print('ok')

    def disconnect(self, close_code):
        try:
            list_mess_check = dict_chat[self.room_group_name]
            check = True
        except:
            check = False

        if check == True:
            list_mess_ = []
            list_mess_ = dict_chat[self.room_group_name]
            if list_mess not in list_mess_:
                print('true')
            #     list_mess_ = list_mess_ + list_mess
            #     dict_chat[self.room_group_name] = list_mess_
            #     print('co roi')
            #     print(list_mess_)
            print(list_mess)
            print(list_mess_)
        else:
            dict_chat[self.room_group_name] = list_mess
            print('chua co')
            print(list_mess)
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )



    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        who = text_data_json['who']

        list_mess.append(text_data_json)
        print(list_mess)

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'who' : who
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        who = event['who']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'who': who
        }))



# class UserConsumer(WebsocketConsumer):
#     def connect(self):
#         self.user_name = self.scope['url_route']['kwargs']['username']
#         self.accept()
#         u = Users.objects.get(username=self.user_name)
#         tk = Tickets.objects.filter(sender=u)
#         dem = 0
#         for tk in tk:
#             if tk.status == 1:
#                 dem = dem + 1
#         if dem is not 0:
#             self.send(text_data=json.dumps({
#                 'aaa': dem
#             }))


class UserConsumer(WebsocketConsumer):
    def connect(self):
        self.user_name = self.scope['url_route']['kwargs']['username']
        self.room_group_name = 'chat_%s' % self.user_name
        
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # tkid = text_data_json['ticketid']

        print(message)
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
        }))
  

    
        
    