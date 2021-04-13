from django.db import models
from django.utils.translation import ugettext_lazy as _


class Device(models.Model):
    class Unit(models.TextChoices):
        METER = 'm', _('Meter')
        KILOGRAM = 'kg', _('Kilogram')
        SECOND = 's', _('Second')
        AMPERE = 'A', _('Ampere')
        KELVIN = 'K', _('Kelvin')
        MOLE = 'mol', _('Mole')
        CANDELA = 'Cd', _('Candela')

    class Prefix(models.TextChoices):
        GIGA = 'G', _('Giga')
        MEGA = 'M', _('Mega')
        KILO = 'K', _('Kilo')
        CENTI = 'C', _('Centi')
        MILLI = 'm', _('Milli')
        MICRO = 'micro', _('Micro')
        NANO = 'n', _('Nano')

    name = models.CharField(_('name'), max_length=150, unique=True)
    max_value = models.FloatField(_('max value'))
    min_value = models.FloatField(_('min value'))
    unit = models.CharField(_('unit'), max_length=30, choices=Unit.choices)
    prefix = models.CharField(_('prefix'), max_length=30, choices=Prefix.choices, null=True)

    def __str__(self):
        return self.name
