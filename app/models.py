from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


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


@receiver(post_save, sender=Order)
def order_status_changed(sender, instance, **kwargs):
    # Order modeli saqlanganidan so'ng, status o'zgarsa, WebSocket orqali xabar yuborish
    if True:
        channel_layer = get_channel_layer()
        group_name = 'order_status_group'

        # Groupdan foydalanib xabar yuborish
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                'type': 'order.status_changed',
                'message': {
                    'order_id': instance.id,
                    'new_status': instance.status,
                },
            },
        )
