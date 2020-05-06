from django.contrib import admin
from main_web.models import *

import re


#admin 管理面板
class qa_infoAdmin(admin.ModelAdmin):
    list_display = ('data', 'problem_description', 'department', 'sub_department', 'responsible_person',)
    list_display_links = ('data', 'problem_description', 'department', 'sub_department',)
    #如果没有按规则放则需单独声明
    #change_form_template = 'admin/main_web/mymodel/change_list.html'
    def save_model(self, request, obj, form, change):
        filename = r'grade.csv'
        pos = []
        dict_grade = {}
        dict_grade.setdefault('找不到', )
        f_txt = open(filename, 'r')
        f_txt.readline()
        for line in f_txt:
            #print (line)
            #print (type(line))
            lines = line.split(',')
            lines[1] = lines[1].strip("\n")
            pos.append(lines)
            dict_grade[lines[0]] = lines[1]
        f_txt.close()
        sub_information_classification = obj.sub_information_classification.name


        if dict_grade.get(sub_information_classification):
            obj.grade = dict_grade[sub_information_classification]
            #print (sub_information_classification.encode('gb2312'))
        else:
            print (' NO MATCH')

        print (obj.grade)
        obj.save()

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
