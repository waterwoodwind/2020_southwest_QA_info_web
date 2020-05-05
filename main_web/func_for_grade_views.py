#coding=utf-8
import pandas as pd
from main_web.models import hr_info
from main_web.models import Department
from main_web.models import Sub_Department
from main_web.models import Team

"""
def get_qa_info_with_grade():
    
    df_data = pd.read_hdf('data.h5', 'df')
    df_data = df_data[df_data[u"严重程度"] > 0]
    df_data = df_data.loc[:, [u"责任人",u"检查者", u"严重程度"]]
    df_data[[u"严重程度"]] = df_data[[u"严重程度"]].apply(pd.to_numeric)
    
    return df_data
"""

def get_hr_info():
    tuple_hr_info = list(hr_info.objects.values_list('hr_employee_number', 'hr_employee_name', 'hr_department',
                                                     'hr_sub_department', 'hr_team'))
    list_hr_info = []
    for i,item in enumerate(tuple_hr_info):
        element = []
        element.append(tuple_hr_info[i][0])
        element.append(tuple_hr_info[i][1])
        if item[2] != None:
            element.append(Department.objects.get(id = item[2]).name)
        else:
            element.append(item[2])
        if item[3] != None:
            element.append(Sub_Department.objects.get( id = item[3]).name)
        else:
            element.append(item[3])
        if item[4] != None:
            element.append(Team.objects.get( id = item[4]).name)
        else:
            element.append(item[4])
        list_hr_info.append(element)
    return list_hr_info

def get_hr_info_df():
    tuple_hr_info = list(hr_info.objects.values_list('hr_employee_number', 'hr_employee_name', 'hr_department',
                                                     'hr_sub_department', 'hr_team'))
    list_hr_info = []
    number_list = []
    name_list = []
    department_list = []
    sub_department_list = []
    team_list = []
    for i,item in enumerate(tuple_hr_info):
        element = []
        number_list.append(tuple_hr_info[i][0])
        name_list.append(tuple_hr_info[i][1])
        if item[2] != None:
            department_list.append(Department.objects.get(id = item[2]).name)
        else:
            department_list.append(item[2])
        if item[3] != None:
            sub_department_list.append(Sub_Department.objects.get( id = item[3]).name)
        else:
            sub_department_list.append(item[3])
        if item[4] != None:
            team_list.append(Team.objects.get( id = item[4]).name)
        else:
            team_list.append(item[4])

    data = {u'员工编号': number_list,
            u'姓名': name_list,
            u'部门': department_list ,
            u'分部': sub_department_list,
            u'班组': team_list}
    df = pd.DataFrame(data)
    return df