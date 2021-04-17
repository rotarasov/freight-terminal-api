from datetime import timedelta

from django.db import models
from django.utils.translation import ugettext_lazy as _

from freight_terminal import settings


class Company(models.Model):
    class Type(models.TextChoices):
        INBOUND = 'inbound', _('Inbound')
        OUTBOUND = 'outbound', _('Outbound')
        THIRD_PARTY = 'third_party', _('Third party')
        FOURTH_PARTY = 'fourth_party', _('Fourth party')
        DISTRIBUTION = 'distribution', _('Distribution')
        REVERSE = 'reverse', _('Reverse')

    account = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(_('name'), max_length=150)
    type = models.CharField(_('type'), max_length=30, choices=Type.choices)

    def __str__(self):
        return self.name


class Robot(models.Model):
    class Type(models.TextChoices):
        SEA = 'sea', _('Sea')
        AIR = 'air', _('Air')
        LAND = 'land', _('land')

    class Status(models.TextChoices):
        BUSY = 'busy', _('Busy')
        FREE = 'free', _('Free')
        UNAVAILABLE = 'unavailable', _('Unavailable')

    model = models.CharField(_('model'), max_length=50)
    type = models.CharField(_('type'), max_length=30, choices=Type.choices)
    company = models.ForeignKey('Company', on_delete=models.CASCADE, related_name='robots')
    status = models.CharField(_('status'), max_length=30, choices=Status.choices, default=Status.FREE)

    def __str__(self):
        return f'{self.model}({self.company})'

    def start_transit(self):
        self.status = Robot.Status.BUSY

    def finish_transit(self):
        self.status = Robot.Status.FREE


class Service(models.Model):
    class Type(models.TextChoices):
        DELIVERY = 'delivery', _('Delivery')
        RECEPTION = 'reception', _('Reception')

    class Status(models.TextChoices):
        NOT_STARTED = 'not_started', _('Not started')
        IN_TRANSIT_WITHOUT_FREIGHT = 'in_transit_without_freight', _('In transit without freight')
        IN_TRANSIT_WITH_FREIGHT = 'in_transit_with_freight', _('In transit with freight')
        TRANSFERING = 'transfering', _('Transfering')
        WAITING = 'waiting', _('Waiting')
        DONE = 'done', _('Done')

    arrival_datetime = models.DateTimeField(_('arrival datetime'))
    delay_time = models.DurationField(_('delay time'), default=timedelta())
    robot = models.ForeignKey('Robot', on_delete=models.CASCADE, related_name='services')
    type = models.CharField(_('type'), max_length=30, choices=Type.choices)
    status = models.CharField(_('status'), max_length=30, choices=Status.choices, default=Status.NOT_STARTED)

    def __str__(self):
        return f'{self.type} by {self.robot}'

    def is_started(self):
        return self.status != Service.Status.NOT_STARTED

    def return_freight(self):
        pass


class Transfer(models.Model):
    delivery_service = models.OneToOneField('Service', on_delete=models.CASCADE, related_name='delivery_transfer')
    reception_service = models.OneToOneField('Service', on_delete=models.CASCADE, related_name='reception_transfer')

    def __str__(self):
        return f'{self.delivery_service}; {self.reception_service}'

    @classmethod
    def exists(cls, delivery_service, reception_service, instance=None):
        transfers = Transfer.objects.filter(models.Q(delivery_service=delivery_service) |
                                            models.Q(reception_service=reception_service))
        if instance:
            return transfers.exclude(id=instance.id).exists()
        return transfers.exists()

    def start_freight_return(self):
        self.delivery_service.return_freight()
        self.reception_service.return_freight()

