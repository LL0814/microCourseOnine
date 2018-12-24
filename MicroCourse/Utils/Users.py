from django.shortcuts import HttpResponse, redirect, render
from django.contrib.auth.models import User
from django.contrib import auth
from MicroCourse import models
from django.db.models import Q,F
from django.db import transaction
import re, datetime


class Users:
    '''
        用户方法父类
    '''
    def __init__(self):
        pass

    def _register(self, UserName, Password, Type, teacher = 0):
        '''
        用户注册
        :param UserName:
        :param Password:
        :param Type:
        :return: UserName是否为空或者是否存在，True=> 注册失败 否则注册成功
        '''
        try:
            if not self._checkUsernameIsValid(UserName):
                return HttpResponse('该用户名已存在')
            if UserName == "":
                '''判断是否存在'''
                errormg = "unIsBlank"
                return HttpResponse(errormg)
            User.objects.get(username=UserName)
            errormg = "unIsExist"
            return HttpResponse(errormg)
        except User.DoesNotExist:
            '''判断UserName是否存在'''
            try:
                if Password == '':
                    errormg = "pwIsBlank"
                    return HttpResponse(errormg)
                else:
                    with transaction.atomic():
                        user = User.objects.create_user(username=UserName, password=Password, is_active=True) #创建用户
                        user.save()
                        models.UserProfile.objects.filter(user_id=user.id).update(
                                headImage='/static/authentication/images/defautHeadImage.png',
                                nickname=UserName,
                                teacher=teacher,
                                type = self._getTypeIdByType(Type)) #给刚创建用的用户赋予其他属性
                        models.UserType.objects.filter(type=Type).update( count = F('count') + 1) #相关类型的USER 数量加一
                    errormg = "success"
                    return HttpResponse(errormg)
            except Exception as e:
                print(e)
                return HttpResponse('err')

    def _login(self, request, UserName, Password, Remember):
        '''
        用户登陆
        :param request:
        :param UserName:
        :param Password:
        :param Remember:
        :return:
        '''
        try:
            if UserName == '':
                return HttpResponse("用户名或密码错误")
            if Password == '':
                return HttpResponse("用户名或密码错误")
            if UserName and Password:
                user = auth.authenticate(username=UserName, password=Password) #验证用户名和密码
                if user is None:
                    return HttpResponse("用户名或密码错误")
                elif user and user.is_active and not user.check_password(Password):
                    return HttpResponse("用户名或密码错误")
                else:
                    auth.login(request, user)  # 用户验证成功
                    request.session['username'] = UserName  # username存入session
                    request.session['is_login'] = True  # is_login=True
                    type = models.UserProfile.objects.filter(user__username=user.username).first().type.type
                    request.session['type'] = type
                    print(type)
                    if type == 'student':
                        redirectURL = '/index/'
                    elif type == 'teacher':
                        redirectURL = '/myStudents/'
                    else:
                        redirectURL = '/grades/'
                    print(redirectURL)
                    if Remember == "true":#是否保持登陆状态
                        request.session.set_expiry(30*24*3600) #保存30天
                        return HttpResponse(redirectURL)
                    return HttpResponse(redirectURL)
            else:
                return redirect('/login/')
        except Exception as e:
            return HttpResponse('err')

    def _logout(self):
        pass

    def _modifiy(self):
        pass

    def _getTypeIdByType(self, type):
        type = models.UserType.objects.filter(type=type)
        if type != None:
            return type.first().id
        else:
            return 0

    def _checkUsernameIsValid(self, username):
        inValidKeyword = ['admin', 'super']
        for keyword in inValidKeyword:
            if keyword  in username:
                return False
        return True

    def _myself(self, request):
        username = request.session.get('username', None)
        userprofile = models.UserProfile.objects.filter(user__username=username).first()
        teachers = SuperAdmin()._getAllTeahcerWithProfile()
        grades = SuperAdmin()._getAllGrades()
        classes = SuperAdmin()._getClassesByGradeId(userprofile.grade)
        teachersinfo = []
        grade2class = {}
        gradeid2name = {}
        for grade in grades:
            gradeid2name[grade['id']] = grade['name']
        for t in teachers:
            teacher = {}
            teacher['name'] = t.userprofile.nickname
            teacher['id'] = t.id
            teachersinfo.append(teacher)
        for grade in grades:
            classes = SuperAdmin()._getClassesByGradeId(grade['id'])
            grade2class[grade['name']] = list(classes)
        return render(request, 'MicroCourse/user_profile.html', {'userprofile':userprofile, 'teachers':teachersinfo, 'grades':list(grades), 'classes':classes, 'grade2class':grade2class, 'gradeid2name':gradeid2name })

    def _resetPassword(self, request):
        username = request.session.get('username', None)
        password = request.POST.get('password')
        user = User.objects.get(username=username)
        user.set_password(password)  # 设置新的密码
        try:
            with transaction.atomic():
                user.save()
                return HttpResponse('success')
        except:
            return HttpResponse('error')

    def _editProfile(self, request):
        username = request.session.get('username', None)
        nickname = request.POST.get('nickname')
        teacherId = request.POST.get('teacherId')
        gradeId = request.POST.get('gradeId')
        classId = request.POST.get('classId')
        print(username, nickname, teacherId, gradeId, classId)
        try:
            with transaction.atomic():
                models.UserProfile.objects.filter(user__username=username).update(nickname=nickname,
                                                                                  teacher=teacherId,
                                                                                  grade=gradeId,
                                                                                  class1=classId)
                return HttpResponse('success')
        except:
            return HttpResponse('error')

    def _createQuestion(self, request):
        title = request.POST.get('title')
        content = request.POST.get('html')
        username = request.session.get('username', None)
        userid = User.objects.filter(username=username).first().id
        try:
            with transaction.atomic():
                models.Question.objects.create(title=title, content=content, user_id=userid)
            return True
        except:
            return False

    def _getAllQA(self, request):
        QA = models.Question.objects.filter().all()
        username = request.session.get('username', None)
        userprofile = models.UserProfile.objects.filter(user__username=username).values().first()
        return render(request, 'MicroCourse/qa.html', {'userprofile': userprofile, 'QA':QA, })

    def _getQAById(self, id, request):
        username = request.session.get('username', None)
        userprofile = models.UserProfile.objects.filter(user__username=username).values().first()
        QA = models.Question.objects.filter(id=id)
        AQ = models.Answer.objects.filter(question_id=id).order_by("-time")
        answerCount = len(AQ)
        return render(request, 'MicroCourse/QAitem.html', {'userprofile': userprofile, 'QA':QA.first(), 'AQ':AQ,
                                                           'answerCount':answerCount,})

    def _addAnswer(self, request):
        answer = request.POST.get("answer")
        url = request.POST.get("url", None)
        Qid = url.split('/')[-1].replace('#commentedit', '')
        username = request.session.get("username", None)
        user = User.objects.get(username=username)
        try:
            models.Answer.objects.create(content=answer, question_id=Qid, user_id=user.id, time=datetime.datetime.now())
            models.Question.objects.filter(id=Qid).update(status=1)
            return HttpResponse("success")
        except:
            return HttpResponse("success")

class student(Users):
    '''
    学生类
    '''
    def __init__(self):
        super(student, self).__init__()

    def _study(self):
        pass

    def _test(self):
        pass

    def _askQ(self, request):
        pass

class Teacher(Users):
    '''
    教师类
    '''
    def __init__(self):
        super(Teacher, self).__init__()

    def _studentManage(self, request):
        '''
        学生管理
        :param request:
        :return:
        '''
        teacher_username = request.session.get('username', None)
        tid = User.objects.filter(username=teacher_username).first().id
        username = request.POST.get('username')
        passowrd = request.POST.get('password')
        id = int(request.POST.get('id'))
        try:
            with transaction.atomic():
                studentCount = self._checkStudent(username)
                if id == 0 and studentCount == 0:
                    return self._createStudent(username, passowrd, tid)
                elif id > 0 and studentCount == 1:
                    return self._updateStudent(id, username, passowrd)
                elif id > 0 and studentCount == 0:
                    return HttpResponse('用户名不允许被修改')
                else:
                    return HttpResponse('该用户名已存在')
        except Exception as e:
            print(e)
            return HttpResponse('错误：请稍后再试')

    def _checkStudent(self, name):
        '''
        使用名称检查该学生是否存在
        :param name:
        :return:
        '''
        return models.User.objects.filter(username=name).count()

    def _selectStudent(self, id):
        '''
        查询该id的学生信息并返回信息或者错误信息
        :param id:
        :return:
        '''
        res = models.User.objects.filter(id=id).values()
        if res.count() > 0:
            return res.first()
        else:
            return 'notExist'

    @transaction.atomic
    def _updateStudent(self, id, name, password):
        '''
        更新该id的学生信息
        :param id:
        :param name:
        :param password:
        :return:
        '''
        if not super()._checkUsernameIsValid(name):
            return HttpResponse('该用户名已存在')
        models.User.objects.filter(id=id).update(username=name)
        self._resetStudentPassword(id, password)
        return HttpResponse('success')

    @transaction.atomic
    def _resetStudentPassword(self, id, password):
        '''
        修改学生密码
        :param id:
        :param password:
        :return:
        '''
        user = models.User.objects.get(id=id)
        user.set_password(password) #设置新的密码
        user.save()

    @transaction.atomic()
    def _createStudent(self, name, password, tid):
        '''
        新增学生
        :param name:
        :param des:
        :param gradeId:
        :return:
        '''
        return super()._register(name,password,'student', tid) #调用父类的注册方法

    def _showMyStudents(self, request):
        '''
        格式化并展示该教师的所有学生的信息
        :param request:
        :return:
        '''
        username = request.session.get('username')

        teacher = User.objects.filter(username=username).first()
        userprofile = models.UserProfile.objects.filter(user_id=teacher.id).values().first()
        if userprofile['type_id'] == 1:
            students = self._getAllStudents()
        else:
            students = self._getMyStudents(teacher.id)
        for student in students:
            studentProfile = models.UserProfile.objects.filter(id=student['id']).first()
            student['nickname'] = studentProfile.nickname
            student['gender'] = '男' if studentProfile.gender == 1 else ' 女'
        return render(request, 'MicroCourseAdmin/myStudents.html', {'students': students, 'userprofile':userprofile})

    def _getMyStudents(self, teacherid):
        '''
        获取当前教师的所有学生信息
        :param teacherid:
        :return:
        '''

        return User.objects.filter(userprofile__type=super()._getTypeIdByType('student'), userprofile__teacher=teacherid).values().all()

    def _getAllStudents(self):
        '''
        获取全部的学生信息// 管理员
        :return:
        '''
        return User.objects.filter(userprofile__type=super()._getTypeIdByType('student')).values().all()

    def _showMyTasks(self, request):
        type = ['单选题', '多选题', '判断题', '填空题']
        username = request.session.get('username', None)
        userprofile = models.UserProfile.objects.filter(user__username=username).values().first()
        owner = User.objects.filter(username=username).first()
        myTasks = self._getMyTasks(owner.id)
        for task in myTasks:
            task['type'] = type[task['type'] - 1]
        return render(request, 'MicroCourseAdmin/myTasks.html', {'myTasks': myTasks, 'userprofile':userprofile})

    def _getMyTasks(self, ownerId):
        return models.TaskInfo.objects.filter(owner=ownerId).values().all()

    def _formatAllTasks(self, request):
        type = ['单选题', '多选题', '判断题', '填空题']
        username = request.session.get('username')
        owner = User.objects.filter(username=username).first()
        allTasks = self._getAllTasks()
        for task in allTasks:
            task['type'] = type[task['type'] - 1]
        return allTasks

    def _getAllTasks(self):
        return models.TaskInfo.objects.filter().values().all()

    def _getTasksByNameAndType(self, name, type):
        return models.TaskInfo.objects.filter(type=type, name__icontains=name).values()

    def _myTaskManage(self, request):
        username = request.session.get('username')
        ownerId = self._getOwnerId(username)
        name = request.POST.get('name')
        standardAnswer = request.POST.get('standardAnswer')
        alternativeAnswers = request.POST.get('alternativeAnswers')
        type = request.POST.get('type')
        id = int(request.POST.get('id'))
        try:
            with transaction.atomic():
                taskCount = self._checkTask(name)
                if id == 0 and taskCount == 0:
                    self._createTask(name, standardAnswer, alternativeAnswers, type, ownerId)
                    return HttpResponse('success')
                elif id > 0 and taskCount <= 1:
                    self._updateTask(id, name, standardAnswer, alternativeAnswers, type, ownerId)
                    return HttpResponse('success')
                else:
                    return HttpResponse('该题目已存在')
        except Exception as e:
            print(e)
            return HttpResponse('错误：请稍后再试')

    def _getOwnerId(self, username):
        return User.objects.filter(username=username).first().id

    def _getOwnerProfileById(self, id):
        return models.UserProfile.objects.filter(user_id=id).values().first()

    def _checkTaskById(self, id):
        return models.TaskInfo.objects.filter(id=id).all().count()

    def _checkTask(self, name):
        return models.TaskInfo.objects.filter(name=name).all().count()

    def _createTask(self, name, standardAnswers, alternativeAnswers, type, ownerId):
        with transaction.atomic():
            models.TaskInfo.objects.create(name=name, standardAnswers=standardAnswers, alternativeAnswers=alternativeAnswers, type=type, owner_id=ownerId)

    def _updateTask(self, id, name, standardAnswers, alternativeAnswers, type, ownerId):
        with transaction.atomic():
            models.TaskInfo.objects.filter(id=id).update(name=name, standardAnswers=standardAnswers, alternativeAnswers=alternativeAnswers, type=type, owner_id=ownerId)

    def _renderTask(self, request, id):
        username = request.session.get('username', None)
        userprofile = models.UserProfile.objects.filter(user__username=username).values().first()
        count = self._checkTaskById(id)
        if count > 0:
            task = models.TaskInfo.objects.filter(id=id).values().first()
            return render(request, 'MicroCourseAdmin/myTaskManage.html', {'id': id, 'task': task, 'userprofile':userprofile})
        else:
            return redirect('/myTasks/')

    def _renderTaskOfAll(self, request, id):
        username = request.session.get('username', None)
        userprofile = models.UserProfile.objects.filter(user__username=username).values().first()
        count = self._checkTaskById(id)
        if count > 0:
            task = models.TaskInfo.objects.filter(id=id).values().first()
            return render(request, 'MicroCourseAdmin/taskDetail.html', {'id': id, 'task': task, 'userprofile':userprofile})
        else:
            return redirect('/myTasks/')

    def _createTestPaper(self, request):
        name = request.POST.get('testPaperName')
        tasks = request.POST.get('tasks')
        scores = request.POST.get('scores')
        score_count = request.POST.get('score_count')
        username = request.session.get('username')
        ownerId = self._getOwnerId(username)
        with transaction.atomic():
            res = models.TestPaper.objects.create(name=name, tasks=tasks, scores=scores, score_count=score_count, owner_id=ownerId)
            return res.id

    def _fetchAllTestPapers(self, request):
        username = request.session.get('username', None)
        userprofile = models.UserProfile.objects.filter(user__username=username).values().first()
        tests = models.TestPaper.objects.filter().values()
        for test in tests:
            user = User.objects.filter(id=test['owner_id']).values().first()
            userprofile = self._getOwnerProfileById(user['id'])
            username = userprofile['nickname'] if userprofile['nickname'] !='' else user['username']
            test['username'] = username
            name =test['name'].split('&&&')
            test['name'] =name[0] + ' - ' + name[1]
        return render(request, 'MicroCourseAdmin/allTestPapers.html', {'tests':tests, 'userprofile':userprofile})

    def _getTestPaperDetail(self,request, id):
        username = request.session.get('username', None)
        userprofile = models.UserProfile.objects.filter(user__username=username).values().first()
        if self._checkTestPaper(id):
            testPaper = self._getTestPaper(id)
            taskids = testPaper['tasks'].split('&&&')
            title = testPaper['name'].split('&&&')
            tasks = models.TaskInfo.objects.filter(id__in = taskids).values().all()
            test = {}
            test["tasks"] = list(tasks)
            test["title"] = title
            return render(request, 'MicroCourseAdmin/testPaperDetail.html', {'userprofile': userprofile, 'test':test,})
        else:
            return redirect('/404/')

    def _checkTestPaper(self, id):
        res = models.TestPaper.objects.filter(id=id)
        if res:
            return True
        else:
            return False

    def _getTestPaper(self, id):
        return models.TestPaper.objects.filter(id=id).values().first()

    def _createTest(self, id, request):
        if self._checkTestPaper(id):
            username = request.session.get('username', None)
            owner = User.objects.filter(username=username).values().first()
            testPaper = models.TestPaper.objects.filter(id=id).values().first()
            with transaction.atomic():
                models.Test.objects.create(owner_id=owner['id'], paper_id=testPaper['id'], isActive=False, takeExamUserCount=0)
                return HttpResponse('ok')
        else:
            return HttpResponse('该试卷不存在或者已被删除')

    def _getMyTests(self, request):
        username = request.session.get('username', None)
        owner = User.objects.filter(username=username).first()
        userprofile = models.UserProfile.objects.filter(user_id=owner.id).first()
        result = models.Test.objects.filter(owner_id=owner.id)
        tests = []
        for res in result:
            test = {}
            title = res.paper.name.split('&&&')
            test['papername'] = title[0] + ' - ' + title[1]
            test['id'] = res.id
            test['ownername'] = res.owner.userprofile.nickname
            test['takeExamUserCount'] = res.takeExamUserCount
            test['isActive'] = '进行中' if res.isActive else '未激活'
            test['action'] = '结束' if res.isActive else '开始'
            tests.append(test)
        return render(request, 'MicroCourseAdmin/allTests.html', {'tests':tests, 'userprofile':userprofile })

    def _updateTestStatus(self, request):
        url = request.POST.get('url')
        testid = url.split('/')[-1]
        test = models.Test.objects.get(id = testid)
        if test.isActive:
            test.isActive = False
            test.save()
            return HttpResponse('stop')
        else:
            test.isActive = True
            test.save()
            return HttpResponse('start')

    def _getUnitById(self, request, id):
        units = models.UnitCourse.objects.filter(id=id)
        if len(units) == 0:
            return redirect('/404/')
        else:
            unit = units.first()
            files = self._getFilesByUnitId(id)
            username = request.session.get('username', None)
            print(unit)
            print(files)
            userprofile = models.UserProfile.objects.filter(user__username=username).values().first()
            return render(request, 'MicroCourseAdmin/unitCourseManage.html', {'unit':unit, 'files':files, 'userprofile':userprofile})

    def _getFilesByUnitId(self, id):
        files = models.Files.objects.filter(unitCourse=id)
        return files

    def _fileUpload(self, request, unitid):
        pass

class SuperAdmin(Teacher):
    '''
    超级管理员类
    '''
    def __init__(self):
        super(SuperAdmin, self).__init__()

    def _gradeManage(self, request):
        '''
        年级管理
        :param request:
        :return:
        '''
        name = request.POST.get('gradeName')
        des = request.POST.get('gradeDes')
        id = int(request.POST.get('gradeId'))
        try:
            '''
                如果id=='0'则创建新的年级信息 否则更新该年级信息
            '''
            gradeCount = self._checkGradeByName(name)
            if id == 0 and gradeCount == 0:
                self._createGrade(name, des)
            elif id > 0 and gradeCount <= 1:
                self._updateGrade(id, name, des)
            else:
                return HttpResponse('该班级已存在')
            return HttpResponse('success')
        except Exception as e:
            return HttpResponse('错误：请稍后再试')

    def _checkGradeByName(self, name):
        '''
        使用年级名称检查该年级是否已经存在
        :param name:
        :return:
        '''
        return models.GradeInfo.objects.filter(name=name).count()

    def _checkGradeById(self, id):
        '''
        使用年级ID检查改年级是否已经存在
        :param id:
        :return:
        '''
        res = models.GradeInfo.objects.filter(id=id).count()
        if res > 0:
            return False
        else:
            return True

    def _selectGrade(self, id):
        '''
        查询该ID的年级信息，
        :param id:
        :return:
        '''
        res = models.GradeInfo.objects.filter(id=id).values()
        if res.count() > 0:
            return res.first()
        else:
            return 'notExist'

    @transaction.atomic
    def _updateGrade(self, id, name, des):
        '''
        更新年级信息
        :param id:
        :param name:
        :param des:
        :return:
        '''
        models.GradeInfo.objects.filter(id=id).update(name=name, description=des)

    @transaction.atomic
    def _createGrade(self, name, des):
        '''
        创建年级信息
        :param name:
        :param des:
        :return:
        '''
        models.GradeInfo.objects.create(name=name, description=des)

    def _showAllGrades(self, request):
        '''
        查询并展示所有的年级信息
        :param request:
        :return:
        '''
        username = request.session.get('username', None)
        userprofile = models.UserProfile.objects.filter(user__username=username).values().first()
        grades = self._getAllGrades()
        for grade in grades:
            grade['classCount'] = models.ClassInfo.objects.filter(grade=grade['id']).count()
            grade['studentCount'] = User.objects.filter(userprofile__grade=grade['id']).count()
        return render(request, 'MicroCourseAdmin/gradeInfo.html', {'grades':grades, 'userprofile': userprofile})

    def _getAllGrades(self):
        '''
        查询所有的年级信息
        :return:
        '''
        return models.GradeInfo.objects.values().all()

    def _classManage(self, request):
        '''
        班级管理
        :param request:
        :return:
        '''
        name = request.POST.get('className')
        des = request.POST.get('classDes')
        id = int(request.POST.get('classId'))
        gradeId =int(request.POST.get('gradeId'))
        if not self._checkGradeById(gradeId):
            try:
                '''如果id==0 则创建新的班级信息 否则更新该班级信息'''
                classCount = self._checkClass(name, gradeId)
                if id == 0 and classCount == 0:
                    self._createClass(name, des, gradeId)
                elif id >0 and classCount == 1:
                    self._updateClass(id, name, des)
                else:
                    return HttpResponse('该年级已存在该班级')
                return HttpResponse('success')
            except:
                return HttpResponse('错误：请稍后再试')
        else:
            return HttpResponse('该年级不存在')

    def _checkClass(self, name, gradeId):
        '''
        使用班级名称检查该班级是否已经存在
        :param name:
        :return:
        '''
        print(name, gradeId)
        return models.ClassInfo.objects.filter(name=name, grade_id=gradeId).count()

    def _selectClass(self, id):
        '''
        查询该id的班级信息
        :param id:
        :return:
        '''
        res = models.ClassInfo.objects.filter(id=id).values()
        if res.count() > 0:
            return res.first()
        else:
            return 'notExist'

    @transaction.atomic
    def _updateClass(self, id, name, des, gradeId):
        '''
        更新该id的班级信息
        :param id:
        :param name:
        :param des:
        :return:
        '''
        models.ClassInfo.objects.filter(id=id).update(name=name, description=des, grade=gradeId)

    @transaction.atomic
    def _updateClass(self, id, name, des):
        '''
        更新该id的班级信息
        :param id:
        :param name:
        :param des:
        :return:
        '''
        models.ClassInfo.objects.filter(id=id).update(name=name, description=des)

    @transaction.atomic
    def _createClass(self, name, des, gradeId):
        '''
        创建新的班级信息
        :param name:
        :param des:
        :param gradeId:
        :return:
        '''
        models.ClassInfo.objects.create(name=name, description=des, grade_id=gradeId)

    def _showAllClasses(self, request):
        '''
        查询并展示所有的班级信息
        :param request:
        :return:
        '''
        username = request.session.get('username', None)
        userprofile = models.UserProfile.objects.filter(user__username=username).values().first()
        classes = self._getAllClasses()
        for class1 in classes:
            class1['gradeName'] = models.GradeInfo.objects.filter(id=class1['grade_id']).first().name
            class1['studentCount'] = User.objects.filter(userprofile__class1=class1['id'], userprofile__grade=class1['grade_id']).count()
        return render(request, 'MicroCourseAdmin/classes.html', {'classes':classes, 'userprofile':userprofile})

    def _getAllClasses(self):
        '''
        查询所有的班级信息
        :return:
        '''
        return models.ClassInfo.objects.values().all()

    def _courseManage(self, request):
        '''
        课程管理
        :param request:
        :return:
        '''
        name = request.POST.get('courseName')
        des = request.POST.get('courseDes')
        id = int(request.POST.get('courseId'))
        volume = '上册' if request.POST.get('volume') == '1' else '下册'
        gradeId =int(request.POST.get('gradeId'))
        if not self._checkGradeById(gradeId):
            try:
                courseCount = self._checkCourse(name, gradeId, volume)
                if id == 0 and courseCount == 0:
                    self._createCourse(name, des, gradeId ,volume)
                    return HttpResponse('success')
                elif id > 0 and courseCount == 1:
                    self._updateCourse(id, name, des)
                    return HttpResponse('success')
                else:
                    return HttpResponse('该课程名称已存在')
            except Exception as e:
                print(e)
                return HttpResponse('错误：请稍后再试')
        else:
            return HttpResponse('该年级不存在')

    def _checkCourse(self, name, gradeId, volume):
        '''
        使用名称检查该课程是否存在
        :param name:
        :return:
        '''
        return models.CourseInfo.objects.filter(name=name, grade_id=gradeId, volume=volume).count()

    def _selectCourse(self, id):
        '''
        查询该id的课程信息并返回信息或者错误信息
        :param id:
        :return:
        '''
        res = models.CourseInfo.objects.filter(id=id).values()
        if res.count() > 0:
            return res.first()
        else:
            return 'notExist'

    @transaction.atomic
    def _updateCourse(self, id, name, des):
        '''
        更新该id的课程信息
        :param id:
        :param name:
        :param des:
        :return:
        '''
        models.CourseInfo.objects.filter(id=id).update(name=name, description=des)

    @transaction.atomic
    def _createCourse(self, name, des, gradeId, volume):
        '''
        新建课程
        :param name:
        :param des:
        :param gradeId:
        :return:
        '''
        models.CourseInfo.objects.create(name=name, description=des, grade_id=gradeId, volume=volume)

    def _showAllCourses(self, request):
        '''
        展示所有的课程信息
        :param request:
        :return:
        '''
        username = request.session.get('username', None)
        userprofile = models.UserProfile.objects.filter(user__username=username).values().first()
        courses = self._getAllCourses()
        for course in courses:
            course['gradeName'] = models.GradeInfo.objects.filter(id=course['grade_id']).first().name
        return render(request, 'MicroCourseAdmin/courses.html', {'courses':courses, 'userprofile':userprofile})

    def  _getAllCourses(self):
        '''
        查询所有的课程信息
        :return:
        '''
        return models.CourseInfo.objects.values().all()

    def _getUnitCoursesByCourseId(self, id):
        unitCourses = models.UnitCourse.objects.filter(course_id=id).values()
        return unitCourses

    def _createUnitCourse(self, name, des, courseId):
        if self._checkUnitCourseByNameAndCourseId(name, courseId):
            try:
                models.UnitCourse.objects.create(name=name, description=des, course_id=courseId)
                return 'success'
            except:
                return '创建新章节失败, 请稍后再试'
        else:
            return '该章节名称在该课程中已存在'

    def _checkUnitCourseByNameAndCourseId(self, name , courseId):
        count = models.UnitCourse.objects.filter(name=name, course_id=courseId).count()
        return False if count >0 else True

    def _teacherManage(self, request):
        '''
        教师管理
        :param request:
        :return:
        '''
        username = request.POST.get('username')
        passowrd = request.POST.get('password')
        id = int(request.POST.get('id'))
        try:
            with transaction.atomic():
                teacherCount = self._checkTeacher(username)
                print(teacherCount, id)
                if id == 0 and teacherCount == 0:
                    return self._createTeacher(username, passowrd)
                elif id > 0 and teacherCount == 1:
                    return self._updateTeacher(id, username, passowrd)
                elif id > teacherCount == 0:
                    return HttpResponse('用户名不允许被修改')
                else:
                    return HttpResponse('该用户名已存在')
        except Exception as e:
            print(e)
            return HttpResponse('错误：请稍后再试')

    def _checkTeacher(self, name):
        '''
        使用名称检查该教师是否存在
        :param name:
        :return:
        '''
        return models.User.objects.filter(username=name).count()

    def _selectTeacher(self, id):
        '''
        查询该id的教师信息并返回信息或者错误信息
        :param id:
        :return:
        '''
        res = models.User.objects.filter(id=id).values()
        if res.count() > 0:
            return res.first()
        else:
            return 'notExist'

    @transaction.atomic
    def _updateTeacher(self, id, name, password):
        '''
        更新该id的教师信息
        :param id:
        :param name:
        :param password:
        :return:
        '''
        if not super()._checkUsernameIsValid(name):
            print('c')
            return HttpResponse('该用户名已存在')
        models.User.objects.filter(id=id).update(username=name)
        self._resetTeacherPassword(id, password)
        return HttpResponse('success')

    @transaction.atomic
    def _resetTeacherPassword(self, id, password):
        '''
        修改教师密码
        :param id:
        :param password:
        :return:
        '''
        user = models.User.objects.get(id=id)
        user.set_password(password) #设置新的密码
        user.save()

    @transaction.atomic()
    def _createTeacher(self, name, password):
        '''
        新增教师
        :param name:
        :param des:
        :param gradeId:
        :return:
        '''
        return super()._register(name,password,'teacher') #调用父类的注册方法

    def _showAllTeachers(self, request):
        '''
        展示所有的教师信息
        :param request:
        :return:
        '''
        username = request.session.get('username', None)
        userprofile = models.UserProfile.objects.filter(user__username=username).values().first()
        teachers = self._getAllTeachers()
        for teacher in teachers:
            teacherProfile = models.UserProfile.objects.filter(id=teacher['id']).first()
            teacher['nickname'] = teacherProfile.nickname
            teacher['gender'] =  '男' if teacherProfile.gender == 1 else ' 女'
            teacher['grade'] = teacherProfile.grade
            teacher['class1'] = teacherProfile.class1
            teacher['studentCount'] = models.User.objects.filter(userprofile__type=super()._getTypeIdByType('student'),
                                                                 userprofile__teacher=teacher['id']).count()
        return render(request, 'MicroCourseAdmin/teachers.html', {'teachers':teachers, 'userprofile':userprofile})

    def  _getAllTeachers(self):
        '''
        查询所有的教师信息
        :return:
        '''
        return models.User.objects.filter(userprofile__type=super()._getTypeIdByType('teacher')).values().all()

    def _getAllTeahcerWithProfile(self):
        '''
        查询所有的教师详细信息
        :return:
        '''
        return models.User.objects.filter(userprofile__type=super()._getTypeIdByType('teacher'))

    def _getClassesByGradeId(self, id):
        return models.ClassInfo.objects.filter(grade_id=id).values().all()

    def _getCoursesByGradeId(self, id):
        return models.CourseInfo.objects.filter(grade_id=id).values().all()

    def _getGrade2Class2Course(self):
        grades = self._getAllGrades()
        classes = self._getAllClasses()
        courses = self._getAllCourses()
        print(grades)
        print(classes)
        print(courses)
        print('------------------------------')
        dataCustom = []

        for grade in grades:
            gradeid = 'grade-' + str(grade['id'])
            gradedata = {'v': gradeid, 'n': grade['name'], 's': []}
            for class1 in classes:
                classid = 'class-' + str(class1['id'])
                classdata = {'v': classid, 'n': class1['name'], 's': []}
                for course in courses:
                    courseid = 'course-' + str(course['id'])
                    coursedata = {'v': courseid, 'n': course['name']}
                    classdata['s'].append(coursedata)
                if class1['grade_id'] == grade['id']:
                    gradedata['s'].append(classdata)
            dataCustom.append(gradedata)
        print(dataCustom)

    def _getGrade2Class_Course(self, request):
        username = request.session.get('username', None)
        userprofile = models.UserProfile.objects.filter(user__username=username).first()
        grades = self._getAllGrades()
        gradeid2name = {}
        grade2course = {}
        for grade in grades:
            gradeid2name[grade['id']] = grade['name']
        for grade in grades:
            courses = self._getCoursesByGradeId(grade['id'])
            for course in courses:
                course['name'] = course['name'] + '-' + course['volume']
            grade2course[grade['name']] = list(courses)
        return render(request, 'MicroCourseAdmin/selectUnitCourse.html', {'userprofile':userprofile, 'grades':list(grades),
                                                                 'gradeid2name':gradeid2name,
                                                                 'grade2course':grade2course, })