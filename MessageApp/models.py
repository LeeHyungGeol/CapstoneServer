from django.db import models
from userApp.models import User

# Create your models here.
class MessageReceiver(models.Model):
    idx = models.AutoField(primary_key=True)
    recv_idx = models.ForeignKey(User, models.DO_NOTHING, db_column='recv_idx', blank=True, null=True, related_name='receiver_recv_set')
    send_idx = models.ForeignKey(User, models.DO_NOTHING, db_column='send_idx', blank=True, null=True, related_name='receiver_send_set')
    send_date = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'message_receiver'


class MessageSender(models.Model):
    idx = models.AutoField(primary_key=True)
    recv_idx = models.ForeignKey(User, models.DO_NOTHING, db_column='recv_idx', blank=True, null=True, related_name='sender_recv_set')
    send_idx = models.ForeignKey(User, models.DO_NOTHING, db_column='send_idx', blank=True, null=True, related_name='sender_send_set')
    send_date = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=100, blank=True, null=True)
    recv_chk = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'message_sender'