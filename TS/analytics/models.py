import sys
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from .signals import object_viewed_signal
from techsemester.utils import get_client_ip
from django.contrib.gis.geoip2 import GeoIP2

User = get_user_model()


class ObjectViewed(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    ip_address = models.CharField(max_length=250, blank=True, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    viewed = models.BooleanField(default=False)
    actions = models.CharField(max_length=255, blank=True, null=True)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    country_name=models.CharField(max_length=150, blank=True, null=True)
    country_code=models.CharField(max_length=150, blank=True, null=True)
    continent_code=models.CharField(max_length=150, blank=True, null=True)
    continent_name=models.CharField(max_length=150, blank=True, null=True)
    city=models.CharField(max_length=150, blank=True, null=True)
    dma_code=models.CharField(max_length=150, blank=True, null=True)
    latitude=models.CharField(max_length=150, blank=True, null=True)
    longitude=models.CharField(max_length=150, blank=True, null=True)
    postal_code=models.CharField(max_length=150, blank=True, null=True)
    time_zone=models.CharField(max_length=150, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s viewed on %s" %(self.content_object, self.timestamp)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Object viewed'
        verbose_name_plural = 'Objects viewed'


class PivotObjectViewed(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user", null=True, blank=True)
    notifiers = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner", null=True, blank=True)
    notification = models.ForeignKey(ObjectViewed, on_delete=models.CASCADE, related_name="notify_objects")

    class Meta:
        verbose_name = 'Pivot Objective',
        verbose_name_plural = 'Pivot Objectives'


def object_viewed_receiver(sender, instance, request, *args, **kwargs):
    c_type = ContentType.objects.get_for_model(sender)
    request_ip=get_client_ip(request)
    chosen_ip=None
    g = GeoIP2()
    if (len(sys.argv) >= 2 and sys.argv[1] == 'runserver'):
        chosen_ip = '72.14.207.99'
    else:
        chosen_ip = request_ip

    country = g.country(chosen_ip)
    city = g.city(chosen_ip)

    notifier = ObjectViewed.objects.create(
        user=kwargs['user'],
        object_id=instance.id,
        content_type=c_type,
        ip_address=get_client_ip(request),
        actions=kwargs['actions'],
        country_name=country['country_name'],
        country_code=country['country_code'],
        city=city['city'],
        continent_code=city['continent_code'],
        continent_name=city['continent_name'],
        dma_code=city['dma_code'],
        latitude=city['latitude'],
        longitude=city['longitude'],
        postal_code=city['postal_code'],
        time_zone=city['time_zone'],
    )
    PivotObjectViewed.objects.create(
        user=kwargs['user'],
        notifiers=kwargs['replies'],
        notification=notifier
    )


object_viewed_signal.connect(object_viewed_receiver)
