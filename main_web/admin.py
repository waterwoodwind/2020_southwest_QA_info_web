from django.contrib import admin
from main_web.models import *

#admin 管理面板
class qa_infoAdmin(admin.ModelAdmin):
    list_display = ('data', 'problem_description', 'department', 'sub_department', 'responsible_person',)
    list_display_links = ('data', 'problem_description', 'department', 'sub_department',)

class hr_infoAdmin(admin.ModelAdmin):
    list_display = ('hr_employee_number', 'hr_employee_name','hr_team', 'hr_sub_department',
                    'hr_department', 'hr_staff_manager', 'hr_party', 'hr_on_duty')
    list_display_links = ('hr_employee_name',)

# Register your models here.
admin.site.register(hr_info, hr_infoAdmin)
admin.site.register(qa_info, qa_infoAdmin)
admin.site.register(Location)
admin.site.register(Time_Bucket)
admin.site.register(Department)
admin.site.register(Sub_Department)
admin.site.register(Team)
admin.site.register(Information_Source)
admin.site.register(Information_classification)
admin.site.register(Sub_Information_classification)
admin.site.register(Event_class)
admin.site.register(State)
