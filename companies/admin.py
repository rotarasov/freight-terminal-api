from django.contrib import admin

from companies.models import Company, Robot, Service, Transfer


admin.site.register(Company)
admin.site.register(Robot)
admin.site.register(Service)
admin.site.register(Transfer)
