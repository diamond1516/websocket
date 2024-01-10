from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db import models


# Create your models here.


class Model(models.Model):
    name = models.TextField()
    title = models.TextField(null=True)
    son = models.TextField(null=True)


class Order(models.Model):
    name = models.CharField(max_length=255, null=True)
    status = models.CharField(
        max_length=255,
        choices=[('pending', 'Pending'), ('cencelled', 'Cencelled'), ('completed', 'Completed')]
    )

    def save(self, *args, **kwargs):
        channel_layer = self.scope.get('channel_layer', get_channel_layer())
        async_to_sync(channel_layer.group_send)(
            'salom',
            {
                "type": "notification.send",
                "data": {
                    'status': self.status,
                    "message": f"Buyurtmangiz {self.status} holatiga kirdi",
                    "order": self.pk,
                },
            },
        )

        super(Order, self).save(*args, **kwargs)


