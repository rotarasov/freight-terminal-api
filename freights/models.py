from datetime import timedelta

from django.db import models
from django.utils.translation import ugettext_lazy as _

from django.core.validators import MaxValueValidator


class Freight(models.Model):
    class Status(models.TextChoices):
        NOT_ASSIGNED = 'not_assigned', _('Not assigned')
        WAITING = 'waiting', _('Waiting')
        IN_DELIVERY_TRANSIT = 'in_delivery_transit', _('In delivery transit')
        TRANSFERING = 'transfering', _('Transfering')
        IN_RECEPTION_TRANSIT = 'in_reception_transit', _('In reception transit')
        DELIVERED = 'delivered', _('Delivered')

        RETURNING = 'returning', _('Returning')
        RETURNED = 'returned', _('Returned')

    name = models.CharField(_('name'), max_length=150)
    status = models.CharField(_('status'), max_length=30, choices=Status.choices)
    transfer = models.OneToOneField('companies.Transfer', on_delete=models.CASCADE, null=True)
    is_damaged = models.BooleanField(_('is damaged'), default=False)

    def __str__(self):
        return self.name

    def sum_of_rule_coeffs(self):
        return sum(rule.coefficient for rule in self.rules.all())

    def return_damage_freight(self):
        if self.transfer:
            self.status = self.Status.RETURNING
            self.save()
            self.transfer.start_freight_return()


class Rule(models.Model):
    DAMAGE_THRESHOLD_VALUE = 0.2

    coefficient = models.FloatField(_('coefficient'), validators=[MaxValueValidator(1.0)])
    max_value = models.FloatField(_('max value'))
    min_value = models.FloatField(_('min value'))
    possible_deviation = models.FloatField(_('possible deviation'), default=0)
    time_interval = models.DurationField(_('time interval'), default=timedelta(hours=1))
    freight = models.ForeignKey('Freight', on_delete=models.CASCADE, related_name='rules')
    device = models.ForeignKey('devices.Device', on_delete=models.CASCADE, related_name='rules')

    def __str__(self):
        return f'{self.device}({self.freight})'

    def is_violated(self) -> bool:
        out_of_limit_values = 0

        for state in self.states.all():
            if state.value > self.max_value or state.value < self.min_value:
                out_of_limit_values += 1
                deviation = min(abs(state.value - self.max_value), abs(state.value - self.min_value))

                if deviation > self.possible_deviation:
                    return True

        num_of_states = self.states.count()
        if num_of_states and out_of_limit_values / num_of_states > self.DAMAGE_THRESHOLD_VALUE:
            return True

        return False


class State(models.Model):
    value = models.FloatField(_('value'))
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)
    rule = models.ForeignKey('Rule', on_delete=models.CASCADE, related_name='states')

    def __str__(self):
        return f'{self.rule} at {self.timestamp}'



