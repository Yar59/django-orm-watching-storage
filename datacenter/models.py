from django.db import models
from django.utils import timezone

class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard, on_delete=models.CASCADE)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return '{user} entered at {entered} {leaved}'.format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved=(
                f'leaved at {self.leaved_at}'
                if self.leaved_at else 'not leaved'
            )
        )


def calculate_visit_duration(visit):
    entered_at = timezone.localtime(visit.entered_at)
    leaved_at = timezone.localtime(visit.leaved_at)
    if leaved_at:
        seconds_inside = (leaved_at-entered_at).total_seconds()
    else:
        time_now = timezone.now()
        seconds_inside = (time_now-entered_at).total_seconds()
    return seconds_inside


def convert_duration(seconds_inside):
    hours_inside = int(seconds_inside // 3600)
    minutes_inside = int((seconds_inside % 3600) // 60)
    return f'{hours_inside} ч {minutes_inside} мин'


def is_visit_strange(seconds_inside, minutes=60):
    return seconds_inside > minutes*60
    