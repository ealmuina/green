from datetime import timedelta

from django.db import models
from django.utils import timezone


class Node(models.Model):
    TYPE_FULL = 0
    TYPE_PUMP = 1
    TYPE_VALVE = 2

    TYPE_CHOICES = (
        (TYPE_FULL, 'Full'),
        (TYPE_PUMP, 'Pump'),
        (TYPE_VALVE, 'Valve')
    )

    chip_id = models.CharField(max_length=20, unique=True)
    pump = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    node_type = models.IntegerField(choices=TYPE_CHOICES)
    is_open = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    min_moisture = models.IntegerField(null=True, blank=True)
    max_moisture = models.IntegerField(null=True, blank=True)
    max_open_time = models.IntegerField(default=30)

    @property
    def current_moisture(self):
        return self.records.values_list('moisture', flat=True).last()

    @property
    def last_seen(self):
        return self.records.values_list('date', flat=True).last()

    @property
    def is_active(self):
        return self.last_seen and self.last_seen > timezone.now() - timedelta(hours=2)

    def __str__(self):
        return self.chip_id


class Record(models.Model):
    node = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='records')
    moisture = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)


class Firmware(models.Model):
    node_type = models.IntegerField(choices=Node.TYPE_CHOICES)
    version = models.IntegerField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    file = models.FileField(upload_to='media/firmware')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.get_node_type_display().lower()}_v{self.version}'
