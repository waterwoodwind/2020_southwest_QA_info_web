"""southwest_QA_info_web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from main_web import views as main_views
from main_web import grade_views
from main_web import get_views
# 给tooldebug bar
from django.conf import settings
from django.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", main_views.index),
    path("home", main_views.index),
    path("month_count_group_by_department", main_views.month_count_group_by_department),
    path("month_count_cd1_group_by_sub_department", main_views.month_count_cd1_group_by_sub_department),
    path("month_count_cd2_group_by_sub_department", main_views.month_count_cd2_group_by_sub_department),
    path("month_count_cq_group_by_sub_department", main_views.month_count_cq_group_by_sub_department),
    path("month_count_gy_group_by_sub_department", main_views.month_count_gy_group_by_sub_department),
    # grade
    path("grade_staff_year", grade_views.grade_staff_year),
    path("grade_department", grade_views.grade_department),
    # 由一级分类获取二级分类
    path('get_sub_class/<int:obj_id>', get_views.get_sub_class, name='add2'),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns