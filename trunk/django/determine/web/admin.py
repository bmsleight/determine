from django.contrib import admin
from determine.web.models import *


#admin.site.register(SignalSite, prepopulated_fields = {'slug': ('title','description') })
admin.site.register(SignalSite,prepopulated_fields = {'slug': ('title',) })
