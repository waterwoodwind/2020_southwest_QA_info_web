from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from main_web.models import qa_info
from django.core import serializers
import json
import pandas as pd
import arrow
from time import time

from django_pandas.io import read_frame
# autocomplete
from dal import autocomplete
from django.db.models import Q
from main_web.models import Location

def df_chinese_data():
    query_data = qa_info.objects.all().order_by('-data')
    df = read_frame(query_data, verbose = True, coerce_float = False)
    df.columns=["ID",
               "日期",
               "地点",
                "时间",
                "受检部门/大队",
                 "受检分部/中队",
                "责任班组",
                "责任人",
                "信息来源",
                "问题分类",
                "问题二级分类",
                "发生阶段",
                "问题描述",
                "整改措施",
                "处理意见",
                "关闭情况",
                "检查者",
                "相关附件",
                "评分"]
    #print(df)
    print("chinese_updata")
    df["日期"] = df["日期"].apply(lambda x: x.strftime("%Y-%m-%d"))
    chinese_updata = df.to_json(orient='records', force_ascii = False, date_format = 'iso')
    chinese_updata = json.loads(chinese_updata)
    return chinese_updata


def date_range_df_chinese_data(date_start, date_end):
    exclude_list = []

    query_data = qa_info.objects.filter(data__range=[date_start, date_end]).order_by('-data')
    json_data = serializers.serialize("json", query_data, use_natural_foreign_keys=True)
    list_data = json.loads(json_data)

    dict_name_verbose_name = {}
    columns_set = []
    colheaders = []
    dataSchema = {}
    for field in qa_info._meta.fields:
        dict_name_verbose_name[field.name] = field.verbose_name

        if not field.verbose_name in exclude_list:
            print (field.verbose_name)
            colheaders.append(field.verbose_name.encode("utf8"))
            dataSchema[field.verbose_name] = ''
            columns_item = {
                u"title": field.verbose_name,
                u"field": field.verbose_name,
                # u"sortable": u"true",
            }
            if field.verbose_name == u"问题描述":
                columns_item[u"width"] = u"20%"
                columns_item[u"title"] = u"问题描述"
            elif field.verbose_name == u"整改措施":
                columns_item[u"width"] = u"20%"
                columns_item[u"title"] = u"整改措施"
            elif field.verbose_name == u"处理意见":
                columns_item[u"width"] = u"6%"
                columns_item[u"title"] = u"处理意见"
            else:
                split_list = list(field.verbose_name)
                # every two word add
                title_str = ""
                for i in range(len(split_list)):
                    title_str = title_str + split_list[i]
                    if (i + 1) % 2 == 0:
                        title_str = title_str + u"<br>"
                if field.verbose_name == u"相关附件":
                    columns_item[u'formatter'] = "attachment"
                columns_item[u"title"] = title_str
                columns_item[u"width"] = u"2%"
            columns_set.append(columns_item)

    json_columns = json.dumps(columns_set)

    upload_data = []
    for item in list_data:
        single_data = item['fields']
        single_data[u'id'] = item['pk']
        upload_data.append(single_data)
        # print upload_data

    chinese_updata = []
    for item in upload_data:
        dict_updata = {}
        for key, value in item.items():
            dict_updata[dict_name_verbose_name[key]] = value

            # print chinese_updata
        chinese_updata.append(dict_updata)

    return chinese_updata


def index(request):
    print("index")
    upload_data = json.dumps(df_chinese_data())
    return render(request, 'background.html', {'json_data': upload_data})

def month_count_group_by_department(request):
    print("month_count_group_by_department")
    df_data = pd.DataFrame(df_chinese_data())
    df_da = pd.DataFrame(df_chinese_data(), index=df_data[u'日期'])
    string_index = df_data[u'日期']
    # 计算出起止月份
    start_day = string_index.min()
    end_day = string_index.max()
    start_ar = arrow.get(start_day)
    end_ar = arrow.get(end_day)
    print (end_ar)

    if start_ar.day >= 26:
        number_month = start_ar.month + 1
    else:
        number_month = start_ar.month
    start_month = start_ar.replace(month=number_month)
    if end_ar.day >= 26:
        number_month = end_ar.month + 1
    else:
        number_month = end_ar.month + 1
    end_month = end_ar.shift(months=number_month)
    print (end_month)

    list_month = []
    list_month_count_cd_1 = []
    list_month_count_cd_2 = []
    list_month_count_cq = []
    list_month_count_gy = []

    for r in arrow.Arrow.range('month', start_month, end_month):
        year_month = r.format("YYYY-MM")
        end = arrow.get(r)
        end = end.replace(day=25)
        start = end.shift(months=-1)
        start = start.replace(day=26)
        list_a_month = []
        for r in arrow.Arrow.range('day', start, end):
            a_day = r.format('YYYY-MM-DD')
            list_a_month.append(a_day)
        try:
            df_month = df_da.loc[list_a_month]
            list_month.append(year_month)
            list_month_count_cd_1.append(int(df_month[u'受检部门/大队'][df_month[u'受检部门/大队'] == u"成都航线一大队"].count()))
            list_month_count_cd_2.append(int(df_month[u'受检部门/大队'][df_month[u'受检部门/大队'] == u"成都航线二大队"].count()))
            list_month_count_cq.append(int(df_month[u'受检部门/大队'][df_month[u'受检部门/大队'] == u"重庆分公司"].count()))
            list_month_count_gy.append(int(df_month[u'受检部门/大队'][df_month[u'受检部门/大队'] == u"贵阳分公司"].count()))
        except:
            continue

    json_month = json.dumps(list_month)
    json_count_cd_1 = json.dumps(list_month_count_cd_1)
    json_count_cd_2 = json.dumps(list_month_count_cd_2)
    json_count_cq = json.dumps(list_month_count_cq)
    json_count_gy = json.dumps(list_month_count_gy)
    return render(request, "month_count_group_by_department.html", {"json_month": json_month,
                                                                    "json_count_cd_1": json_count_cd_1,
                                                                    "json_count_cd_2": json_count_cd_2,
                                                                    "json_count_cq": json_count_cq,
                                                                    "json_count_gy": json_count_gy})


def month_count_cd1_group_by_sub_department(request):
    df_data = pd.DataFrame(df_chinese_data())
    df_da = pd.DataFrame(df_chinese_data(), index=df_data[u'日期'])
    string_index = df_data[u'日期']
    # 计算出起止月份
    start_day = string_index.min()
    end_day = string_index.max()
    start_ar = arrow.get(start_day)
    end_ar = arrow.get(end_day)
    print (end_ar)

    if start_ar.day >= 26:
        number_month = start_ar.month + 1
    else:
        number_month = start_ar.month
    start_month = start_ar.replace(month=number_month)
    if end_ar.day >= 26:
        number_month = end_ar.month + 1
    else:
        number_month = end_ar.month + 1
    end_month = end_ar.shift(months=number_month)
    print (end_month)

    list_month = []
    list_month_count_cd_1 = []
    list_month_count_cd_2 = []
    list_month_count_cq = []
    list_month_count_gy = []

    for r in arrow.Arrow.range('month', start_month, end_month):
        year_month = r.format("YYYY-MM")
        end = arrow.get(r)
        end = end.replace(day=25)
        start = end.shift(months=-1)
        start = start.replace(day=26)
        list_a_month = []
        for r in arrow.Arrow.range('day', start, end):
            a_day = r.format('YYYY-MM-DD')
            list_a_month.append(a_day)
        try:
            df_month = df_da.loc[list_a_month]
            list_month.append(year_month)
            list_month_count_cd_1.append(int(df_month[u'受检分部/中队'][df_month[u'受检分部/中队'] == u"成都航一一中队"].count()))
            list_month_count_cd_2.append(int(df_month[u'受检分部/中队'][df_month[u'受检分部/中队'] == u"成都航一二中队"].count()))
            list_month_count_cq.append(int(df_month[u'受检分部/中队'][df_month[u'受检分部/中队'] == u"成都航一三方中队"].count()))
            list_month_count_gy.append(int(df_month[u'受检分部/中队'][df_month[u'受检分部/中队'] == u"成都航一排故中队"].count()))
        except:
            continue

    json_month = json.dumps(list_month)
    json_count_cd_1 = json.dumps(list_month_count_cd_1)
    json_count_cd_2 = json.dumps(list_month_count_cd_2)
    json_count_cq = json.dumps(list_month_count_cq)
    json_count_gy = json.dumps(list_month_count_gy)
    return render(request, "month_count_cd1_group_by_sub_department.html", {"json_month": json_month,
                                                                    "json_count_cd_1": json_count_cd_1,
                                                                    "json_count_cd_2": json_count_cd_2,
                                                                    "json_count_cq": json_count_cq,
                                                                    "json_count_gy": json_count_gy})


def month_count_cd2_group_by_sub_department(request):
    df_data = pd.DataFrame(df_chinese_data())
    df_da = pd.DataFrame(df_chinese_data(), index=df_data[u'日期'])
    string_index = df_data[u'日期']
    # 计算出起止月份
    start_day = string_index.min()
    end_day = string_index.max()
    start_ar = arrow.get(start_day)
    end_ar = arrow.get(end_day)
    print (end_ar)

    if start_ar.day >= 26:
        number_month = start_ar.month + 1
    else:
        number_month = start_ar.month
    start_month = start_ar.replace(month=number_month)
    if end_ar.day >= 26:
        number_month = end_ar.month + 1
    else:
        number_month = end_ar.month + 1
    end_month = end_ar.shift(months=number_month)
    print (end_month)

    list_month = []
    list_month_count_cd_1 = []
    list_month_count_cd_2 = []
    list_month_count_cq = []
    list_month_count_gy = []

    for r in arrow.Arrow.range('month', start_month, end_month):
        year_month = r.format("YYYY-MM")
        end = arrow.get(r)
        end = end.replace(day=25)
        start = end.shift(months=-1)
        start = start.replace(day=26)
        list_a_month = []
        for r in arrow.Arrow.range('day', start, end):
            a_day = r.format('YYYY-MM-DD')
            list_a_month.append(a_day)
        try:
            df_month = df_da.loc[list_a_month]
            list_month.append(year_month)
            list_month_count_cd_1.append(int(df_month[u'受检分部/中队'][df_month[u'受检分部/中队'] == u"成都航二定检中队"].count()))
            list_month_count_cd_2.append(int(df_month[u'受检分部/中队'][df_month[u'受检分部/中队'] == u"成都航二客舱中队"].count()))
            list_month_count_cq.append(int(df_month[u'受检分部/中队'][df_month[u'受检分部/中队'] == u"成都航一三方中队"].count()))
            list_month_count_gy.append(int(df_month[u'受检分部/中队'][df_month[u'受检分部/中队'] == u"成都航一排故中队"].count()))
        except:
            continue

    json_month = json.dumps(list_month)
    json_count_cd_1 = json.dumps(list_month_count_cd_1)
    json_count_cd_2 = json.dumps(list_month_count_cd_2)
    json_count_cq = json.dumps(list_month_count_cq)
    json_count_gy = json.dumps(list_month_count_gy)
    return render(request, "month_count_cd2_group_by_sub_department.html", {"json_month": json_month,
                                                                    "json_count_cd_1": json_count_cd_1,
                                                                    "json_count_cd_2": json_count_cd_2,
                                                                    "json_count_cq": json_count_cq,
                                                                    "json_count_gy": json_count_gy})


def month_count_cq_group_by_sub_department(request):
    df_data = pd.DataFrame(df_chinese_data())
    df_da = pd.DataFrame(df_chinese_data(), index=df_data[u'日期'])
    string_index = df_data[u'日期']
    # 计算出起止月份
    start_day = string_index.min()
    end_day = string_index.max()
    start_ar = arrow.get(start_day)
    end_ar = arrow.get(end_day)
    print (end_ar)

    if start_ar.day >= 26:
        number_month = start_ar.month + 1
    else:
        number_month = start_ar.month
    start_month = start_ar.replace(month=number_month)
    if end_ar.day >= 26:
        number_month = end_ar.month + 1
    else:
        number_month = end_ar.month + 1
    end_month = end_ar.shift(months=number_month)
    print (end_month)

    list_month = []
    list_month_count_cd_1 = []
    list_month_count_cd_2 = []
    list_month_count_cq = []
    list_month_count_gy = []

    for r in arrow.Arrow.range('month', start_month, end_month):
        year_month = r.format("YYYY-MM")
        end = arrow.get(r)
        end = end.replace(day=25)
        start = end.shift(months=-1)
        start = start.replace(day=26)
        list_a_month = []
        for r in arrow.Arrow.range('day', start, end):
            a_day = r.format('YYYY-MM-DD')
            list_a_month.append(a_day)
        try:
            df_month = df_da.loc[list_a_month]
            list_month.append(year_month)
            list_month_count_cd_1.append(int(df_month[u'受检分部/中队'][df_month[u'受检分部/中队'] == u"重庆航线一中队"].count()))
            list_month_count_cd_2.append(int(df_month[u'受检分部/中队'][df_month[u'受检分部/中队'] == u"重庆航线二中队"].count()))
            list_month_count_cq.append(int(df_month[u'受检分部/中队'][df_month[u'受检分部/中队'] == u"重庆航线三中队"].count()))
            list_month_count_gy.append(int(df_month[u'受检分部/中队'][df_month[u'受检分部/中队'] == u"重庆定检中队"].count()))
        except:
            continue

    json_month = json.dumps(list_month)
    json_count_cd_1 = json.dumps(list_month_count_cd_1)
    json_count_cd_2 = json.dumps(list_month_count_cd_2)
    json_count_cq = json.dumps(list_month_count_cq)
    json_count_gy = json.dumps(list_month_count_gy)
    return render(request, "month_count_cq_group_by_sub_department.html", {"json_month": json_month,
                                                                    "json_count_cd_1": json_count_cd_1,
                                                                    "json_count_cd_2": json_count_cd_2,
                                                                    "json_count_cq": json_count_cq,
                                                                    "json_count_gy": json_count_gy})


def month_count_gy_group_by_sub_department(request):
    df_data = pd.DataFrame(df_chinese_data())
    df_da = pd.DataFrame(df_chinese_data(), index=df_data[u'日期'])
    string_index = df_data[u'日期']
    # 计算出起止月份
    start_day = string_index.min()
    end_day = string_index.max()
    start_ar = arrow.get(start_day)
    end_ar = arrow.get(end_day)
    print (end_ar)

    if start_ar.day >= 26:
        number_month = start_ar.month + 1
    else:
        number_month = start_ar.month
    start_month = start_ar.replace(month=number_month)
    if end_ar.day >= 26:
        number_month = end_ar.month + 1
    else:
        number_month = end_ar.month + 1
    end_month = end_ar.shift(months=number_month)
    print (end_month)

    list_month = []
    list_month_count_cd_1 = []
    list_month_count_cd_2 = []
    list_month_count_cq = []
    list_month_count_gy = []

    for r in arrow.Arrow.range('month', start_month, end_month):
        year_month = r.format("YYYY-MM")
        end = arrow.get(r)
        end = end.replace(day=25)
        start = end.shift(months=-1)
        start = start.replace(day=26)
        list_a_month = []
        for r in arrow.Arrow.range('day', start, end):
            a_day = r.format('YYYY-MM-DD')
            list_a_month.append(a_day)
        try:
            df_month = df_da.loc[list_a_month]
            list_month.append(year_month)
            list_month_count_cd_1.append(int(df_month[u'受检分部/中队'][df_month[u'受检分部/中队'] == u"航线中队/技术支援分部"].count()))
            list_month_count_cd_2.append(int(df_month[u'受检分部/中队'][df_month[u'受检分部/中队'] == u"客舱中队"].count()))
            list_month_count_cq.append(int(df_month[u'受检分部/中队'][df_month[u'受检分部/中队'] == u"成都航一三方中队"].count()))
            list_month_count_gy.append(int(df_month[u'受检分部/中队'][df_month[u'受检分部/中队'] == u"成都航一排故中队"].count()))
        except:
            continue

    json_month = json.dumps(list_month)
    json_count_cd_1 = json.dumps(list_month_count_cd_1)
    json_count_cd_2 = json.dumps(list_month_count_cd_2)
    json_count_cq = json.dumps(list_month_count_cq)
    json_count_gy = json.dumps(list_month_count_gy)
    return render(request, "month_count_gy_group_by_sub_department.html", {"json_month": json_month,
                                                                    "json_count_cd_1": json_count_cd_1,
                                                                    "json_count_cd_2": json_count_cd_2,
                                                                    "json_count_cq": json_count_cq,
                                                                    "json_count_gy": json_count_gy})


class LocationAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:  # 这里校验是否为登录用户
            return Location.objects.none()

        print("self q:")
        print (self.q)

        qs = Location.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        # qs = qs.filter(Q(id__icontains=self.q) | Q(name__icontains=self.q))  # 复选框搜索条件(id 和 名称)
        print(qs)
        return qs