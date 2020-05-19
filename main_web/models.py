from django.db import models

# Create your models here.
class Location(models.Model):
    name = models.CharField(max_length=50)

    def natural_key(self):
        return (self.name)

    class Meta:
        unique_together = (('name'),)

    def __str__(self):
        return self.name

class Time_Bucket(models.Model):
    name = models.CharField(max_length=50)

    def natural_key(self):
        return (self.name)

    class Meta:
        unique_together = (('name'),)

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=50)

    def natural_key(self):
        return (self.name)

    class Meta:
        unique_together = (('name'),)

    def __str__(self):
        return self.name

class Sub_Department(models.Model):
    name = models.CharField(max_length=50)

    def natural_key(self):
        return (self.name)

    class Meta:
        unique_together = (('name'),)

    def __str__(self):
        return self.name

class Team(models.Model):
    name = models.CharField(max_length=50)

    def natural_key(self):
        return (self.name)

    class Meta:
        unique_together = (('name'),)

    def __str__(self):
        return self.name

class Information_Source(models.Model):
    name = models.CharField(max_length=50)

    def natural_key(self):
        return (self.name)

    class Meta:
        unique_together = (('name'),)

    def __str__(self):
        return self.name

class Information_classification(models.Model):
    name = models.CharField(max_length=50)

    def natural_key(self):
        return (self.name)

    class Meta:
        unique_together = (('name'),)

    def __str__(self):
        return self.name

class Sub_Information_classification(models.Model):
    name = models.CharField(max_length=50)
    information_classification = models.ForeignKey(Information_classification, on_delete=models.CASCADE,
                                                   verbose_name=u'问题分类')
    value = models.DecimalField(max_digits=1, decimal_places=0, verbose_name=u'分值', blank=True, null=True)

    def natural_key(self):
        return (self.name)

    class Meta:
        unique_together = (('name'),)

    def __str__(self):
        return self.name

class Event_class(models.Model):
    name = models.CharField(max_length=50)

    def natural_key(self):
        return (self.name)

    class Meta:
        unique_together = (('name'),)

    def __str__(self):
        return self.name


class State(models.Model):
    name = models.CharField(max_length=50)

    def natural_key(self):
        return (self.name)

    class Meta:
        unique_together = (('name'),)

    def __str__(self):
        return self.name

class qa_info(models.Model):
    data = models.DateField(u'日期')
    location = models.ForeignKey(Location, on_delete = models.CASCADE, verbose_name=u'地点')
    time_bucket = models.ForeignKey(Time_Bucket, on_delete = models.CASCADE, verbose_name=u'时间')
    department = models.ForeignKey(Department, on_delete = models.CASCADE, verbose_name=u'受检部门/大队')
    sub_department = models.ForeignKey(Sub_Department, on_delete = models.CASCADE, verbose_name=u'受检分部/中队')
    team = models.ForeignKey(Team, on_delete = models.CASCADE, default = u'无', verbose_name=u'责任班组')
    responsible_person = models.CharField(max_length=100, verbose_name=u'责任人')
    information_Source = models.ForeignKey(Information_Source, on_delete = models.CASCADE, verbose_name=u'信息来源')
    information_classification = models.ForeignKey(Information_classification, on_delete = models.CASCADE, verbose_name=u'问题分类')
    sub_information_classification = models.ForeignKey(Sub_Information_classification, on_delete=models.CASCADE,
                                                   verbose_name=u'问题二级分类')
    event_class = models.ForeignKey(Event_class, on_delete = models.CASCADE, verbose_name=u'发生阶段')
    problem_description = models.TextField(verbose_name = u'问题描述', unique_for_date = 'data')
    corrective_action = models.TextField(u'整改措施')
    treatment_suggestion = models.TextField(u'处理意见')
    state = models.ForeignKey(State, on_delete = models.CASCADE, verbose_name=u'关闭情况')
    scrutator = models.CharField(max_length=100, verbose_name=u'检查者')
    Appendix = models.FileField(upload_to='upload/%Y/%m/%d',blank=True, verbose_name=u'相关附件')
    grade = models.DecimalField(max_digits=1, decimal_places=0,verbose_name = u'评分', blank= True, null=True)

    class Meta:
        ordering = ["-data"]

    def __str__(self):
        return self.problem_description


class hr_info(models.Model):
    hr_employee_number = models.CharField(max_length=100, verbose_name=u'员工编号')
    hr_employee_name = models.CharField(max_length=100, verbose_name=u'员工姓名')
    hr_department = models.ForeignKey(Department, on_delete = models.CASCADE, blank= True,
                                      null=True,verbose_name=u'部门/大队')
    hr_sub_department = models.ForeignKey(Sub_Department, on_delete=models.CASCADE, blank=True,
                                          null=True, verbose_name=u'分部/中队')
    hr_team = models.ForeignKey(Team, on_delete = models.CASCADE, blank= True, null=True,
                                verbose_name=u'责任班组')
    hr_staff_manager = models.CharField(max_length=10, verbose_name=u'是否干部', blank= True,
                                        null=True)
    hr_party = models.CharField(max_length=10, verbose_name=u'是否党员', blank= True,
                                        null=True,)
    hr_on_duty = models.CharField(max_length=10, verbose_name=u'是否在职检查者', blank= True,
                                        null=True,)

    def __str__(self):
        return self.hr_employee_name