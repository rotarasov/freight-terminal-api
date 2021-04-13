from django.contrib import admin

from freights.models import Freight, Rule, State


admin.site.register(Freight)
admin.site.register(Rule)
admin.site.register(State)