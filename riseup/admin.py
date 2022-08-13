from django.contrib import admin

from .models import *


class StartupAdmin(admin.ModelAdmin):
    list_display=['startup_id','user_type','name','email']

class StudentAdmin(admin.ModelAdmin):
    list_display=['table_id','user_type','name','email']

class InvestorAdmin(admin.ModelAdmin):
    list_display=['table_id','user_type','name','email']



admin.site.register(Startup,StartupAdmin)
admin.site.register(Student,StudentAdmin)
admin.site.register(Investor,InvestorAdmin)