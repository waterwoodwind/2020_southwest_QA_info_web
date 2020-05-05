#coding=utf-8

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "southwest_QA_info_web.settings")

import django
django.setup()

from main_web.models import *
import codecs
def import_location():
    f = open('Location.txt')
    txt = f.read()
    LocationList = []
    title = txt.split(',')
    for item in title:
        #print item
        start,end = map(int,item.split('-'))
        #print start,end
        for number in range(start,(end + 1)):
            location = Location(name=number)
            LocationList.append(location)
    #location = Location(name=title)
    #LocationList.append(location)
    f.close()
    Location.objects.bulk_create(LocationList)

def import_Time_Bucket():
    Time_Bucket_list = []
    for hour in range(24):
        str_hour = str(hour).zfill(2)
        line_hour = str_hour + ":00-" + str_hour + ":59"
        time_bucket = Time_Bucket(name = line_hour)
        Time_Bucket_list.append(time_bucket)
    Time_Bucket.objects.bulk_create(Time_Bucket_list)

def import_Department():
    f = open('Department.txt')
    txt = f.read()
    f.close()
    objectList = []
    title = txt.split('，')
    #print title
    for item in title:
        department = Department(name=item)
        objectList.append(department)
    Department.objects.bulk_create(objectList)

def import_model(txt_file,model_object):
    f = open(txt_file)
    txt = f.read()
    f.close()
    objectList = []
    title = txt.split('，')
    for item in title:
        single_object = model_object(name=item)
        objectList.append(single_object)
    model_object.objects.bulk_create(objectList)

def import_hr_info():
    objectList = []
    f = open(u'人岗 按数据库department匹配名.csv')
    for line in f:
        item_list = line.split(',')
        employee_number, employee_name, department = item_list[0], item_list[1], item_list[2]
        department_id = Department.objects.get(name = department)
        single_object = hr_info(hr_employee_number = employee_number,
                               hr_employee_name = employee_name,
                               hr_department = department_id)
        objectList.append(single_object)
    f.close()
    hr_info.objects.bulk_create(objectList)

def import_hr_info_team():
    objectList = []
    f = open(u'重庆 航线三 人事.csv', "r")
    # f = open(u'人岗 按数据库department匹配名 含班组.csv','r', 'utf-8')
    print (f)
    s = f.readlines()
    print (s)
    for line in s:
        hr_object = hr_info()
        print (line)
        item_list = line.split(',')
        employee_number, employee_name, department, sub_department = item_list[0], item_list[1], item_list[2], item_list[3]
        if employee_number == u'\ufeff338747':
            employee_number = u'338747'

        employee_number = employee_number.zfill(8)
        sub_department = sub_department.strip()
        employee_number = employee_number.strip()
        department_id = Department.objects.get(name=department)
        sub_department_id = Sub_Department.objects.get(name=sub_department)
        #print employee_number, team
        #print type(team)
        #print team == u'无'
        # print chardet.detect(team)
        # print chardet.detect(department)

        # print employee_number, team_id
        #hr_object = hr_info.objects.get(hr_employee_number=employee_number)
        hr_object.hr_employee_number = employee_number
        hr_object.hr_employee_name = employee_name
        hr_object.hr_department = department_id
        hr_object.hr_sub_department = sub_department_id
        objectList.append(hr_object)
        hr_object.save()
    f.close()

if __name__ == "__main__":
    '''初始化时已完成
    import_location()
    import_Time_Bucket()
    import_Department()
    import_model("Information_Source.txt",Information_Source)
    import_model("Information_classification.txt", Information_classification)
    import_model("Event_class.txt", Event_class)
    import_model("Team.txt", Team)
    import_model("State.txt", State)
    '''
    import_hr_info_team()
    print('Done!')