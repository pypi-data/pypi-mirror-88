from django.conf import settings
from django.db import models
from djangoldp.models import Model


class Conversation(Model):
    title = models.TextField()
    text = models.TextField(null=True)
    author_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    dateCreated = models.DateTimeField(auto_now_add=True)

    class Meta:
        auto_author = 'author_user'
        owner_field = 'author_user'
        ordering = ['-dateCreated']
        container_path = "conversations"
        nested_fields = ["message_set", "author_user"]
        rdf_type = 'hd:conversation'
        anonymous_perms = ['view']
        authenticated_perms = ['inherit', 'add']
        owner_perms = ['inherit', 'change', 'control', 'delete']

    def __str__(self):
        return '{}'.format(self.title)


class Message(Model):
    dateCreated = models.DateField(auto_now_add=True)
    text = models.TextField()
    conversation = models.ForeignKey("Conversation", on_delete=models.SET_NULL, null=True)
    author_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    class Meta:
        auto_author = 'author_user'
        owner_field = 'author_user'
        ordering = ['dateCreated']
        container_path = "messages"
        nested_fields = ["author_user"]
        rdf_type = 'hd:conversationmessage'
        anonymous_perms = ['view']
        authenticated_perms = ['inherit', 'add']
        owner_perms = ['inherit', 'change', 'control', 'delete']

    def __str__(self):
        return '{}, le {}'.format(self.text, self.dateCreated)
