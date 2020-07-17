from django.contrib import admin
from main_web.models import *
# auto complete
from main_web.forms import qa_infoForm
import re


#admin 管理面板
class qa_infoAdmin(admin.ModelAdmin):
    # autocomplete 使用 forms.py 中定义的 UserProjectRelationshipForm
    form = qa_infoForm
    list_display = ('data', 'problem_description', 'department', 'sub_department', 'responsible_person',)
    list_display_links = ('data', 'problem_description', 'department', 'sub_department',)
    #如果没有按规则放则需单独声明
    #change_form_template = 'admin/main_web/mymodel/change_list.html'
    def save_model(self, request, obj, form, change):

        sub_information_classification = obj.sub_information_classification.name
        if obj.grade == None:
            try:
                sub_in_class_obj = Sub_Information_classification.objects.get(name = sub_information_classification)
                sub_value = sub_in_class_obj.value
                obj.grade = sub_value
                #print (sub_information_classification.encode('gb2312'))
            except Sub_Information_classification.DoesNotExist:

                print (' NO MATCH')



        print (obj.grade)

        obj.save()

class hr_infoAdmin(admin.ModelAdmin):
    list_display = ('hr_employee_number', 'hr_employee_name','hr_team', 'hr_sub_department',
                    'hr_department', 'hr_staff_manager', 'hr_party', 'hr_on_duty')
    list_display_links = ('hr_employee_name',)

class sub_information_classificationAdmin(admin.ModelAdmin):
    list_display = ('name', 'information_classification','value')
    list_display_links = ('name', 'information_classification','value')

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
admin.site.register(Sub_Information_classification, sub_information_classificationAdmin)
admin.site.register(Event_class)
admin.site.register(State)
