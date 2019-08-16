from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from deployment_app.models import Comment, User, DeploymentNote
import json
from django.utils import timezone


# used a channel layer that uses Redis as its backing store.
class CommentConsumer(WebsocketConsumer):
    def connect(self):
        # Obtains the 'note_id' parameter from the URL route in
        # deployment_app/routing.py that opened the WebSocket
        # connection to the consumer.
        self.note_id = self.scope['url_route']['kwargs']['note_id']
        # Constructs a Channels group name
        self.comment_group_name = 'comment_%s' % self.note_id

        # join comment_group_name
        # The async_to_sync(…) wrapper is required because CommentConsumer
        # is a synchronous WebsocketConsumer but it is calling an asynchronous
        # channel layer method. (All channel layer methods are asynchronous.)
        async_to_sync(self.channel_layer.group_add)(
            self.comment_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.comment_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        # comment saved to database
        text_data_json = json.loads(text_data)
        user = User.objects.get(id=text_data_json['sender_id'])
        comment = Comment()
        comment.sender = user
        comment.comment = text_data_json['message']
        comment.created_at = timezone.now()
        deployment_note = DeploymentNote.objects.get(id=text_data_json['note_id'])
        comment.deployment_note = deployment_note
        comment.save()
        user_name = comment.sender.first_name.capitalize() + " " + comment.sender.last_name.capitalize()

        # send data to comment_group_name
        # An event has a special 'type' key corresponding to the name of
        # the method that should be invoked on consumers that receive the event.
        async_to_sync(self.channel_layer.group_send)(
            self.comment_group_name,
            {
                'type': 'comments',
                "sender": user_name,
                "comment": comment.comment,
                "created_at": comment.created_at.strftime('%B %d, %Y, %H:%M %p '),
                "note_id": comment.deployment_note.id,
            }
        )

    # receive datas from comment_group_name
    def comments(self, event):
        sender = event['sender']
        comment = event['comment']
        date = event['created_at']
        note_id = event['note_id']

        self.send(text_data=json.dumps({
            "sender": sender,
            "comment": comment,
            "created_at": date,
            "note_id": note_id,
        }))
