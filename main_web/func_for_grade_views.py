#coding=utf-8
import pandas as pd
from main_web.models import hr_info
from main_web.models import Department
from main_web.models import Sub_Department
from main_web.models import Team
from django_pandas.io import read_frame

def get_hr_info():
    query_data = hr_info.objects.all()
    df = read_frame(query_data, verbose=True, coerce_float=False)
    df = df.iloc[:, 1:6]
    list_hr_info = df.values.tolist()
    return list_hr_info

def get_hr_info_df():
    query_data = hr_info.objects.all()
    df = read_frame(query_data, verbose=True, coerce_float=False)
    df = df.iloc[:, 1:6]
    df.columns = [u'员工编号',
            u'姓名',
            u'部门',
            u'分部',
            u'班组']
    return df