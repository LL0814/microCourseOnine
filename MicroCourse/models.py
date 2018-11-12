from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils import timezone
import datetime
from django.shortcuts import reverse
# Create your models here.


class UserType(models.Model):
    '''
        用户类型 包括类型和数量， 系统认为:
        id=1 type=admin 为管理员;
        id=2 tpye=teacher为老师;
        id=3 type=student为学生;
        该信息需要在管理员在创建数据库之后手动在数据库中添加数据
    '''
    type = models.CharField(max_length=64, blank=False)
    count = models.IntegerField(default=0)

#User 扩展字段
class UserProfile(models.Model):
    '''
        Django User表的拓展。
        包括userId, 昵称， 头像地址， 性别， 年级， 班级， 类型， 老师
    '''
    user = models.OneToOneField(User)
    nickname = models.CharField(max_length=64, blank=True)
    headImage = models.CharField(max_length=256,blank=True)  #person profile head image
    gender = models.IntegerField(default=0)
    grade = models.IntegerField(default=0)
    class1 = models.IntegerField(default=0)
    type = models.ForeignKey(UserType,default=3)
    teacher = models.IntegerField(default=0)

    def __str__(self):
        return self.token

    def __unicode__(self):
        return self.token

def create_user_profile(sender,instance,created,**kwargs):
    if created:
        profile = UserProfile()
        profile.user = instance
        profile.save()
post_save.connect(create_user_profile,sender=User)


#年级信息表
class GradeInfo(models.Model):
    '''
    年级信息表，包括年级名称以及描述
    '''
    name = models.CharField(max_length=64, blank=False)
    description = models.TextField(blank=True, default='')

#班级信息表
class ClassInfo(models.Model):
    '''
        班级信息表， 包括班级名，年级以及描述
    '''
    name = models.CharField(max_length=64, blank=False)
    description = models.TextField(blank=True, default='')
    grade = models.ForeignKey(GradeInfo)

#课程信息表
class CourseInfo(models.Model):
    '''
        课程信息表，包括课程名，上下册，年级以及课程描述
    '''
    name = models.CharField(max_length=64, blank=False)
    volume = models.CharField(max_length=64 , default='上册')
    description = models.TextField()
    grade = models.ForeignKey(GradeInfo)

class TaskInfo(models.Model):
    name = models.TextField(blank=False)
    type = models.IntegerField(default=1)
    alternativeAnswers = models.CharField(max_length=128, blank=False)
    standardAnswers = models.CharField(max_length=128, blank=False)
    owner = models.ForeignKey(User, default=1)

class TestPaper(models.Model):
    name = models.CharField(blank=False, max_length=1024, default='')
    tasks = models.CharField(blank=False, max_length=2048)
    scores = models.CharField(blank=False, max_length=2048)
    score_count = models.IntegerField(default=0)
    owner = models.ForeignKey(User, default=1)

class Test(models.Model):
    isActive = models.BooleanField(default=False)
    takeExamUserCount = models.IntegerField(default=0)
    owner = models.ForeignKey(User)
    paper = models.ForeignKey(TestPaper)

class TestHistory(models.Model):
    owner = models.ForeignKey(User)
    Test = models.ForeignKey(Test)
    score = models.IntegerField(default=0)

class Question(models.Model):
    title = models.CharField(max_length=64, default='',blank=False)
    content = models.TextField(default='')
    status = models.IntegerField(default=0,blank=False)
    time = models.DateTimeField(default=datetime.datetime.now())
    user = models.ForeignKey(User)

class Answer(models.Model):
    content = models.TextField(default='')
    user = models.ForeignKey(User)
    time = models.DateTimeField(default=datetime.datetime.now())
    question = models.ForeignKey(Question)