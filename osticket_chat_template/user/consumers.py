# chat/consumers.py
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from user.models import *
from channels.layers import get_channel_layer

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
        try:
            f = r'notification/chat/'+self.room_group_name+'.txt'
            file = open(f,'r')
            for line in file:
                message = line.split('^%$^%$&^')[0]
                who = line.split('^%$^%$&^')[1].strip()
                time = line.split('^%$^%$&^')[2].strip()
                self.send(text_data=json.dumps({
                        'message': message,
                        'who': who,
                        'time' : time
                    }))
        except:
            pass
        

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
        who = text_data_json['who']
        time = text_data_json['time']

        f = r'notification/chat/'+self.room_group_name+'.txt'
        file = open(f,'a')
        file.write(message + "^%$^%$&^"+ who +"^%$^%$&^"+ time + "\n") 
        file.close()  

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'who' : who,
                'time' : time
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        who = event['who']
        time = event['time']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'who': who,
            'time' :  time
        }))



class UserConsumer(WebsocketConsumer):
    def connect(self):
        self.user_name = self.scope['url_route']['kwargs']['username']
        self.room_group_name = 'noti_%s' % self.user_name
        
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
        try:
            f = r'notification/user/'+self.room_group_name+'.txt'
            file = open(f, 'r')
            for line in file:
                message = line[:len(line)-1]
                if '*&*%^chat' in message:
                    msg = line.split('*&*%^chat')[0]
                    self.send(text_data=json.dumps({
                        'message': msg,
                        'type' : 're-noti-chat'
                    }))
                else:
                    self.send(text_data=json.dumps({
                            'message': line,
                            'type' : 're-noti'
                        }))
        except:
            pass

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
        
        try:
            type_save = text_data_json['type']
            if type_save == 'chat':
                f = r'notification/user/'+self.room_group_name+'.txt'
                file = open(f,'a') 
                file.write(str(message) + "*&*%^chat" + "\n") 
                file.close()
            else:
                f = r'notification/user/'+self.room_group_name+'.txt'
                file = open(f,'a') 
                file.write(str(message) + "\n")
                file.close()
        except:
            # Send message to room group
            time = text_data_json['time']
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'time': time,
                }
            )
            print(message)
        
        

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        time = event['time']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'time' : time,
        }))



class AgentConsumer(WebsocketConsumer):
    def connect(self):
        self.user_name = self.scope['url_route']['kwargs']['username']
        agentName = self.user_name.split('+')[0]
        group_agent = self.user_name.split('+')[1]
        self.room_group_name = 'noti_%s' % group_agent
        
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
        try:
            f = r'notification/agent/noti_'+agentName+'.txt'
            file = open(f, 'r')
            for line in file:
                message = line[:len(line)-1]
                if '*&*%^chat' in message:
                    msg = line.split('*&*%^chat')[0]
                    self.send(text_data=json.dumps({
                        'message': msg,
                        'type' : 're-noti-chat'
                    }))
                else:
                    self.send(text_data=json.dumps({
                            'message': line,
                            'type' : 're-noti'
                        }))
        except:
            pass

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
        

        try:
            type_save = text_data_json['type']
            agentName = text_data_json['agentName']
            if type_save == 'chat':
                f = r'notification/agent/noti_'+agentName+'.txt'
                file = open(f,'a') 
                file.write(str(message) + "*&*%^chat" + "\n")
                file.close()
            else:
                f = r'notification/agent/noti_'+agentName+'.txt'
                file = open(f,'a') 
                file.write(str(message) + "\n")
                file.close()
        except:
            # Send message to room group
            time = text_data_json['time']
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'time' : time,
                }
            )
            print(message)

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        time = event['time']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'time' : time
        }))
  

    
        
    