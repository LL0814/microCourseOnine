"""MicroCourseOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from MicroCourse import views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/$', views.index),
    url(r'^signUp/$', views.register),
    url(r'^login/$', views.login),
    url(r'^logout/$', views.logout),
    url(r'^404/$', views.forbidden),
    url(r'^profile/$', views.profile),
    url(r'^resources/$', views.video),
    url(r'^records/$', views.records),
    url(r'^gradeManage/([0-9]*)$', views.gradeManage),
    url(r'^grades/$', views.gradeInfo),
    url(r'^classManage/([0-9]*)$', views.classManage),
    url(r'^classes/$', views.classInfo),
    url(r'^courseManage/([0-9]*)$', views.courseManage),
    url(r'^courses/$', views.courseInfo),
    url(r'^teacherManage/([0-9]*)$', views.teacherManage),
    url(r'^teachers/$', views.teachers),
    url(r'^myStudentManage/([0-9]*)$', views.myStudentManage),
    url(r'^myStudents/$', views.getMyStudents),
    url(r'^myTaskManage/([0-9]*)$', views.myTaskManage),
    url(r'^myTasks/$', views.myTasks),
    url(r'^taskDetail/([0-9]*)$', views.taskDetail),
    url(r'^allTasks/$', views.allTasks),
    url(r'^addTestPaper/([0-9]*)$', views.addTestPaper),
    url(r'^testPaperDetail/([0-9]*)$', views.testPaperDetail),
    url(r'^testPapers/$', views.testPapers),
    url(r'^myTests/$', views.myTests),
    url(r'^QA/$', views.allQA),
    url(r'^QADetail/([0-9]+)$', views.QADetail),
    url(r'^ask/$', views.student_ask),
    url(r'^upload_imgs/', views.img_upload_path),
    url(r'^', views.forbidden)
]
