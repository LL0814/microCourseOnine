from django.shortcuts import render, HttpResponse, redirect
from django.contrib import auth
from MicroCourse import models
from MicroCourse.Utils import Users
from django.contrib.auth.models import User
import datetime
import re
import json


# Create your views here.

#用户认证装饰器，判断is_login 是否等于True
def auth_login(func):
    def wrapper(request,*args,**kwargs):
        if not request.session.get("is_login",None):
            return redirect("/login/")
        return func(request,*args,**kwargs)
    return wrapper

#学生认证装饰器，如果是学生， 该网页可以继续访问，否则跳转到404页面
def auth_student(func):
    def  wrapper(request, *args, **kwargs):
        if request.session.get('type', None) == 'student':
            return func(request, *args, **kwargs)
        return redirect('/404/')
    return wrapper

#教师认证装饰器，如果是教师， 该网页可以继续访问，否则跳转到404页面
def auth_teacher(func):
    def wrapper(request, *args, **kwargs):
        if request.session.get('type', None) == 'teacher':
            return func(request, *args, **kwargs)
        return redirect('/404/')
    return wrapper

#管理员认证装饰器，如果是管理员，该网页可以继续访问，否则跳转到404页面
def auth_admin(func):
    def  wrapper(request, *args, **kwargs):
        if request.session.get('type', None) == 'admin':
            return func(request, *args, **kwargs)
        return redirect('/404/')
    return wrapper

#管理员认证装饰器，如果是管理员或者教师，该网页可以继续访问，否则跳转到404页面
def auth_admin_teacher(func):
    def  wrapper(request, *args, **kwargs):
        if request.session.get('type', None) == 'admin' or request.session.get('type', None) == 'teacher':
            return func(request, *args, **kwargs)
        return redirect('/404/')
    return wrapper


@auth_login
def index(request):
    username = request.session.get('username', None)
    userprofile = models.UserProfile.objects.filter(user__username=username).values().first()
    return render(request, 'MicroCourse/index.html', {'userprofile': userprofile})

def register(requset):
    '''
    用户注册
    :param requset:
    :return:
    '''
    try:
        if requset.method == 'GET':
            return render(requset, 'MicroCourse/sign_up.html')
        if requset.method == 'POST':
            UserName = requset.POST.get('UserName')
            PassWord = requset.POST.get('Password')
            user = Users.Users()
            Feedback = user._register(UserName, PassWord, 'student') #type='student' 学生注册
            return Feedback
    except Exception as e:
        print(e)
        return HttpResponse('err')

def login(requset):
    '''
    用户登陆
    :param requset:
    :return:
    '''
    if requset.method == 'GET':
        return render(requset,'MicroCourse/sign_in.html')
    if requset.method == 'POST':
        try:
            UserName = requset.POST.get('UserName')
            PassWord = requset.POST.get('Password')
            Remember = requset.POST.get('Remember') #是否保持登陆状态
            user = Users.Users()
            Feedback = user._login(requset, UserName, PassWord, Remember) #用户登录
            print(Feedback)
            return Feedback
        except Exception as e:
            return HttpResponse('err')

def logout(request):
    '''
    退出登录
    :param request:
    :return:
    '''
    auth.logout(request)
    request.session["is_login"] = False #is_login=False 用户退出登录
    return redirect('/login/')

def forbidden(request):
    return render(request, 'MicroCourse/err404.html')

def profile(request):
    feedback = Users.Users()._myself(request)
    return feedback

def video(request):
    return render(request, 'MicroCourse/ui_elements.html')

def records(request):
    return render(request, 'MicroCourse/tables.html')


'''-------------------------管理员-------------------------'''
@auth_login
@auth_admin
def gradeInfo(request):
    '''
    年级信息
    :param request:
    :return:
    '''
    if request.method == 'GET':
        admin = Users.SuperAdmin() #实例化一个管理员
        return admin._showAllGrades(request) #展示所有的年级信息

@auth_login
@auth_admin
def gradeManage(request, *args):
    '''
    管理年级信息
    :param request:
    :param args:
    :return:
    '''
    if request.method == 'GET':
        username = request.session.get('username', None)
        userprofile = models.UserProfile.objects.filter(user__username=username).values().first()
        grade = {
            'name': '',
            'description': '',
        }
        id = args[0] if args[0] != '' else 0
        if id == 0:
            return render(request, 'MicroCourseAdmin/gradeManage.html', {'id': id, 'grade': grade,'userprofile':userprofile})
        admin = Users.SuperAdmin()
        grade = admin._selectGrade(id)
        if grade != 'notExist':
            return render(request, 'MicroCourseAdmin/gradeManage.html' ,{'id':id, 'grade':grade, 'userprofile': userprofile})
        else:
            return redirect('/grades/')
    if request.method == 'POST':
        admin = Users.SuperAdmin()
        return admin._gradeManage(request) #创建或者修改年级信息

@auth_login
@auth_admin
def classInfo(request):
    '''
    班级信息
    :param request:
    :return:
    '''
    if request.method == 'GET':
        admin = Users.SuperAdmin()
        return admin._showAllClasses(request) #展示所有的班级信息

@auth_login
@auth_admin
def classManage(request, *args):
    '''
    管理班级信息
    :param request:
    :param args:
    :return:
    '''
    if request.method == 'GET':
        username = request.session.get('username', None)
        userprofile = models.UserProfile.objects.filter(user__username=username).values().first()
        class1 = {
            'name': '',
            'description': '',
        }
        id = args[0] if args[0] != '' else 0
        admin = Users.SuperAdmin()
        grades = admin._getAllGrades()
        if id == 0:
            return render(request, 'MicroCourseAdmin/classManage.html', {'id': id, 'class1': class1, 'grades':grades, 'userprofile':userprofile})
        class1 = admin._selectClass(id)
        if class1 != 'notExist':
            return render(request, 'MicroCourseAdmin/classManage.html' ,{'id':id, 'class1':class1, 'grades':grades, 'userprofile':userprofile})
        else:
            return redirect('/classes/')
    if request.method == 'POST':
        admin = Users.SuperAdmin()
        return admin._classManage(request) #创建或者修改班级信息

@auth_login
@auth_admin
def courseInfo(request):
    '''
    课程信息
    :param request:
    :return:
    '''
    if request.method == 'GET':
        admin = Users.SuperAdmin()
        return admin._showAllCourses(request) #展示所有的课程信息

@auth_login
@auth_admin
def courseManage(request, *args):
    '''
    管理课程信息
    :param request:
    :param args:
    :return:
    '''
    if request.method == 'GET':
        username = request.session.get('username', None)
        userprofile = models.UserProfile.objects.filter(user__username=username).values().first()
        course = {
            'name': '',
            'description': '',
        }
        id = args[0] if args[0] != '' else 0
        admin = Users.SuperAdmin()
        grades = admin._getAllGrades()
        if id == 0:
            return render(request, 'MicroCourseAdmin/courseManage.html', {'id': id, 'course': course, 'grades':grades, 'userprofile':userprofile})
        course = admin._selectCourse(id)
        if course != 'notExist':
            return render(request, 'MicroCourseAdmin/courseManage.html' ,{'id':id, 'course':course, 'grades':grades, 'userprofile':userprofile})
        else:
            return redirect('/classes/')
    if request.method == 'POST':
        admin = Users.SuperAdmin()
        return admin._courseManage(request) #创建或者更新课程信息

@auth_login
@auth_admin
def teachers(request):
    '''
    展示所有的教师信息
    :param request:
    :return:
    '''
    if request.method == 'GET':
        user = Users.SuperAdmin()
        return user._showAllTeachers(request)

@auth_login
@auth_admin
def teacherManage(request, *args):
    '''
    教师管理
    :param request:
    :param args:
    :return:
    '''
    if request.method == 'GET':
        username = request.session.get('username', None)
        userprofile = models.UserProfile.objects.filter(user__username=username).values().first()
        teacher = {
            'username': '',
        }
        id = args[0] if args[0] != '' else 0
        admin = Users.SuperAdmin()
        if id == 0:
            return render(request, 'MicroCourseAdmin/teacherManage.html', {'id':id, 'teacher':teacher, 'userprofile':userprofile})
        teacher = admin._selectTeacher(id)
        if teacher != 'notExist':
            return render(request, 'MicroCourseAdmin/teacherManage.html', {'id':id, 'teacher': teacher, 'userprofile':userprofile})
        else:
            return redirect('/teachers/')
    if request.method == 'POST':
        admin = Users.SuperAdmin()
        return admin._teacherManage(request) #创建或者更新教师信息

'''-------------------------教师-------------------------'''

@auth_login
@auth_admin_teacher
def getMyStudents(request):
    '''
    获取当前教师的所有学生信息
    :param request:
    :return:
    '''
    if request.method == 'GET':
        teacher = Users.Teacher()
        return teacher._showMyStudents(request)

@auth_login
@auth_admin_teacher
def myStudentManage(request, *args):
    '''
    学生管理
    :param request:
    :return:
    '''
    if request.method == 'GET':
        username = request.session.get('username', None)
        userprofile = models.UserProfile.objects.filter(user__username=username).values().first()
        student = {
            'username': '',
        }
        id = args[0] if args[0] != '' else 0
        teacher = Users.Teacher()
        if id == 0:
            return render(request, 'MicroCourseAdmin/myStudentManage.html', {'id':id, 'student':student, 'userprofile':userprofile})
        student = teacher._selectStudent(id)
        if student != 'notExist':
            return render(request, 'MicroCourseAdmin/myStudentManage.html', {'id':id, 'student': student, 'userprofile':userprofile})
        else:
            return redirect('/myStudents/')
    if request.method == 'POST':
        admin = Users.SuperAdmin()
        return admin._studentManage(request) #创建或者更新教师信息

@auth_login
@auth_admin_teacher
def myTasks(request):
    if request.method == 'GET':
        teacher = Users.Teacher()
        return teacher._showMyTasks(request)

@auth_login
@auth_admin_teacher
def myTaskManage(request, *args):
    if request.method == 'GET':
        username = request.session.get('username', None)
        userprofile = models.UserProfile.objects.filter(user__username=username).values().first()
        task = {
            'name': '',
            'type': '单选题',
        }
        id = args[0] if args[0] != '' else 0
        teacher = Users.Teacher()
        if id == 0:
            return render(request, 'MicroCourseAdmin/myTaskManage.html', {'id':id, 'task':task, 'userprofile':userprofile})
        return  teacher._renderTask(request, id)
    if request.method == 'POST':
        admin = Users.SuperAdmin()
        return admin._myTaskManage(request) #创建或者更新教师信息

@auth_login
@auth_admin_teacher
def allTasks(request):
    if request.method == 'GET':
        username = request.session.get('username', None)
        userprofile = models.UserProfile.objects.filter(user__username=username).values().first()
        teacher = Users.Teacher()
        allTasks = teacher._formatAllTasks(request)
        return render(request, 'MicroCourseAdmin/allTasks.html', {'allTasks': allTasks, 'userprofile':userprofile })

@auth_login
@auth_admin_teacher
def taskDetail(request, *args):
    if request.method == 'GET':
        teacher = Users.Teacher()
        id = args[0] if args[0] != '' else 0
        if id == 0:
            return redirect('/allTasks/')
        return teacher._renderTaskOfAll(request, id)

def testPapers(request):
    teacher = Users.Teacher()
    callback =  teacher._fetchAllTestPapers(request)
    return callback

@auth_login
@auth_admin_teacher
def addTestPaper(request, *args):
    teacher = Users.Teacher()
    if request.method == 'GET':
        username = request.session.get('username', None)
        userprofile = models.UserProfile.objects.filter(user__username=username).values().first()
        allTasks = teacher._formatAllTasks(request)
        return render(request, 'MicroCourseAdmin/addTestPaper.html', {'allTasks' : allTasks, 'userprofile':userprofile })
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'query':
            taskName = request.POST.get('taskName')
            type = request.POST.get('type')
            if taskName == '' or taskName == None:
                tasks = []
            else:
                tasks = teacher._getTasksByNameAndType(taskName, type)
            return HttpResponse(json.dumps(list(tasks)), content_type="application/json")
        elif action == 'submit':
            id = teacher._createTestPaper(request)
            return HttpResponse(id)

@auth_login
@auth_admin_teacher
def testPaperDetail(request, *args):
    teacher = Users.Teacher()
    if request.method == 'GET':
        username = request.session.get('username', None)
        userprofile = models.UserProfile.objects.filter(user__username=username).values().first()
        id = args[0]
        feedback = teacher._getTestPaperDetail(request, id)
        return feedback
    elif request.method == 'POST':
        URL = request.POST.get('url')
        testPaperid =  URL.split('/')[-1]
        feedback = teacher._createTest(testPaperid, request)
        return feedback



@auth_login
@auth_admin_teacher
def myTests(request):
    teacher = Users.Teacher()
    if request.method == 'GET':
        feedback = teacher._getMyTests(request)
        return feedback
    elif request.method == 'POST':
        feedback = teacher._updateTestStatus(request)
        return feedback

@auth_login
def allQA(request):
    user = Users.Users()
    feedback = user._getAllQA(request)
    return feedback

def student_ask(request):
    if request.method == 'GET':
        username = request.session.get('username', None)
        userprofile = models.UserProfile.objects.filter(user__username=username).values().first()
        return render(request, 'MicroCourse/question.html', {'userprofile':userprofile})
    if request.method == 'POST':
        user = Users.Users()
        feedback = user._createQuestion(request)
        if feedback:
            return HttpResponse('success')
        else:
            return HttpResponse('error')
def QADetail(request, *args):
    user = Users.Users()
    if request.method == 'GET':
        id = args[0]
        feedback = user._getQAById(id, request)
        return feedback
    if request.method =='POST':
        feedback = user._addAnswer(request)
        return feedback

#系统的图片上传，并回显给客户端
@auth_login
def img_upload_path(request):
    image = request.FILES.get("imgFile")
    username = request.session.get("username", None)
    prefix = request.POST.get("prefix", None)
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    time1= re.sub(r"\D",'',str(time))
    with open("static/upload_imgs/%s.png" %time1,'wb') as f:
        for item in image.chunks():
            f.write(item)
    dic = {
        'error': 0,
        'url': '/static/upload_imgs/%s.png' %time1,
        'message': '错误了...'
    }
    if prefix == 'head':
        userid = User.objects.filter(username=username).values().first()["id"]
        models.UserProfile.objects.filter(user_id=userid).update(headImage=dic["url"])
    if prefix == 'newImg':
        return  HttpResponse('/static/upload_imgs/%s.png' %time1)
    return HttpResponse(json.dumps(dic))

