from django.shortcuts import render,HttpResponse,redirect
import json
from app01 import models
from django.utils.html import mark_safe
from utils.page import Pagination
import os
# Create your views here.


def auth(func):
    def inner(request,*args,**kwargs):
        username = request.session.get("username")
        if username:
            return func(request,*args,**kwargs)
        else:
            return redirect("/login.html")
    return inner


def login(request):
    ret = {"status": True, "error": None, "data": None}
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        c = models.administrator.objects.filter(username=username,password=password).count()
        if c:
            ret["data"] = "登录成功"
            request.session["username"] = username
            request.session["is_login"] = True
        else:
            ret["error"] = "用户名或者密码错误"
            ret["status"] = False
        return HttpResponse(json.dumps(ret))
    return render(request, "login.html")


@auth
def manager(request):
    return render(request, "manager_master.html")


@auth
def manager_classes(request):
    current_page = int(request.GET.get("p",1))
    cls_item_count = models.classes.objects.count()
    obj = Pagination(current_page,cls_item_count,10,11)
    classes_list = models.classes.objects.all()[obj.db_start:obj.db_end]
    return render(request,"manager_classes.html",{"classes_list":classes_list,"page_str":obj.get_page_html()})


@auth
def api_add_classes(request):
    ret = {"status": True, "error": None, "data": None}
    caption = request.POST.get("caption")
    c = models.classes.objects.filter(caption=caption)

    if c:
        ret["status"] = False
        ret["error"] = "你添加的课程已经存在"
    else:
        models.classes.objects.create(caption=caption)
        classes_id = models.classes.objects.filter(caption=caption)[0].id
        ret["data"] = "添加[%s]课程成功" % caption
        ret["classes_id"] = classes_id
    return HttpResponse(json.dumps(ret))


@auth
def api_update_classes(request):
    ret = {"status": True, "error": None, "data": None}
    caption = request.POST.get("caption")
    classes_id = request.POST.get("id")
    models.classes.objects.filter(id=classes_id).update(caption=caption)
    return HttpResponse(json.dumps(ret))


@auth
def api_delete_classes(request):
    ret = {"status": True, "error": None, "data": "删除成功"}
    classes_id = request.POST.get("id")
    models.classes.objects.filter(id=classes_id).delete()
    return HttpResponse(json.dumps(ret))



@auth
def manager_student(request):
    student_list = models.student.objects.all()
    classes_list = models.classes.objects.all()
    return render(request,"manager_student.html",{"student_list":student_list,"classes_list":classes_list})


@auth
def api_add_student(request):
    ret = {"status": True, "error": None, "data": None}
    classes_id = request.POST.get("classes_select")
    username = request.POST.get("username")
    c = models.student.objects.filter(username=username)
    if c:
        ret["status"] = False
        ret["error"] = "你添加的用户已经存在"
    else:
        models.student.objects.create(username=username,cls_id=classes_id)
        student_id = models.student.objects.filter(username=username)[0].id
        ret["data"] = "添加[%s]用户成功" % username
        ret["student_id"] = student_id
    return HttpResponse(json.dumps(ret))


@auth
def api_update_student(request):
    ret = {"status": True, "error": None, "data": None}
    cls_id = request.POST.get("cls_id")
    username = request.POST.get("username")
    student_id = request.POST.get("id")
    models.student.objects.filter(id=student_id).update(username=username,cls_id=cls_id)
    return HttpResponse(json.dumps(ret))


@auth
def api_delete_student(request):
    ret = {"status": True, "error": None, "data": "删除成功"}
    student_id = request.POST.get("id")
    models.student.objects.filter(id=student_id).delete()
    return HttpResponse(json.dumps(ret))


@auth
def manager_teacher(request):
    teacher_list = models.teacher.objects.all()
    classes_list = models.classes.objects.all()
    return render(request,"manager_teacher.html",{"teacher_list":teacher_list,"classes_list":classes_list})


@auth
def api_add_teacher(request):
    ret = {"status": True, "error": None, "data": None}
    cls_id_list = request.POST.getlist("classes_select")
    username = request.POST.get("username")
    c = models.teacher.objects.filter(username=username).count()
    cls_obj_list = []
    for i in cls_id_list:
        cls_obj_list.append(models.classes.objects.get(id=i))
    if c:
        obj = models.teacher.objects.get(username=username)
        obj.cls.set(cls_obj_list)
    else:
        obj = models.teacher.objects.create(username=username)
        obj.cls.add(*cls_obj_list)
    obj.save()
    teacher_id = models.teacher.objects.get(username=username).id
    ret["data"] = "添加记录成功"
    ret["teacher_id"] = teacher_id
    return HttpResponse(json.dumps(ret))

@auth
def api_update_teacher(request):
    ret = {"status": True, "error": None, "data": None}
    cls_id_list = request.POST.getlist("classes_select")
    teacher_id = request.POST.get("teacher_id")
    obj = models.teacher.objects.get(id=teacher_id)
    cls_obj_list = []
    for i in cls_id_list:
        cls_obj_list.append(models.classes.objects.get(id=i))
    obj.cls.set(cls_obj_list)
    obj.save()
    return HttpResponse(json.dumps(ret))


@auth
def api_delete_teacher(request):
    ret = {"status": True, "error": None, "data": "删除成功"}
    teacher_id = request.POST.get("id")
    classes_id = request.POST.get("classes_id")
    obj = models.teacher.objects.get(id=teacher_id)
    obj.cls.remove(models.classes.objects.get(id=classes_id))
    return HttpResponse(json.dumps(ret))


def logout(request):
    request.session.clear()
    return redirect("/login.html")


def test(request):
    """
    tip：
        1，一对多关系中的foreignkey字段可以是写fk_id,也可以是fk对象
        2，filter(),get(),update() 中不能使用双引号，字段必须是表存在的，__
        3，values(),values_list() 中要使用双引号，字段可以是关联表，__
        4，对多对表中反向查找使用_set
    :param request:
    :return:
    """
    # 增加数据 普通表
    # models.Publisher.objects.create(name="新闻出版社")
    # obj = models.Publisher(name="吉林出版社")
    # obj.save()
    # dic = {"name":"中华出版社"}
    # models.Publisher.objects.create(**dic)

    # 一对多表添加数据
    # models.Book.objects.create(name="西游记",publish=models.Publisher.objects.get(id=1))
    # models.Book.objects.create(name="三国演义",publish_id=2)

    # 多对多添加数据
    # models.Book.objects.create(name="水浒传",publish_id=3)
    # models.Book.objects.create(name="红楼梦",publish_id=1)
    # models.Author.objects.create(name="李杰")
    # models.Author.objects.create(name="张三")
    # models.Author.objects.create(name="胡伟")

    # 多对多添加对应关系
    # 正向添加，Author表中有m字段
    # obj = models.Author.objects.get(id=1)
    # obj.m.add(1,2)
    # obj.m.add(models.Book.objects.get(id=3))
    # 反向添加，Book表中没有关系字段，可以通过author_set字段来处理
    # obj = models.Book.objects.get(id=2)
    # obj.author_set.add(1,2,3)
    # obj.author_set.add(*[4,5,6])



    ########################################################################################

    # 查询数据 普通表
    # ret_all = models.Publisher.objects.all()
    # ret_filter = models.Publisher.objects.filter(id=1)
    # ret_get = models.Publisher.objects.get(id=1)
    # ret_values = models.Publisher.objects.values("id","name")
    # ret_values_list = models.Publisher.objects.values_list("id","name")
    # print(ret_all)
    # print(ret_filter)
    # print(ret_get)
    # print(ret_values)
    # print(ret_values_list)

    # 一对多表查询数据
    # ret_all = models.Book.objects.all()
    # print(ret_all[0].publish, ret_all[0].publish_id)
    # print(models.Book.objects.filter(publish=models.Publisher.objects.get(id=2)))
    # print(models.Book.objects.filter(publish_id=1,id__gt=1))
    # print(models.Book.objects.filter(publish_id=1,id__gt=1).values_list("name","publish_id","publish__name","publish"))
    # print(models.Book.objects.get(publish_id=3))

    # 对多对表查询数据，正向查询，m得到的是Book对应的QuerySet集合，可以通过all(),filter(),get()操作，
    # ret_all = models.Author.objects.all()
    # print(ret_all[0].m.all())
    # print(ret_all[0].m.filter(id=9))
    # print(ret_all[0].m.values())
    # print(ret_all[0].m.values_list())

    # obj = models.Author.objects.filter(id=1)[0]
    # print(obj.name,obj.id,obj.m.all())
    # print(models.Author.objects.values("name","m__name"))
    # print(models.Author.objects.values_list("name","m__name"))

    # 反向查询
    # ret_all = models.Book.objects.all()
    # print(ret_all[0].author_set.all())
    # print(ret_all[0].author_set.filter(id=1))

    ########################################################################################

    # 修改数据 普通表
    # models.Publisher.objects.filter(id=1).update(name="武汉出版社")

    # 一对多
    # models.Book.objects.filter(id=1).update(publish=models.Publisher.objects.get(id=2))
    # models.Book.objects.filter(id=1).update(publish_id=1)
    # models.Book.objects.filter(id=4).update(name="Linux鸟哥私房菜")

    # 多对多
    # obj = models.Author.objects.filter(id=1)[0]
    # obj.m.set([1,4,7])

    ########################################################################################
    # 删除数据 普通表
    # models.Publisher.objects.filter(id=1).delete()

    # 一对多表
    # models.Book.objects.filter(id=4).delete()

    # 多对多表
    # obj = models.Author.objects.filter(id=1)[0]
    # obj.m.remove(7)
    # obj.m.clear()
    return HttpResponse("ok")


def upload(request):
    if request.method == "GET":
        file_list = models.Upload.objects.all()
        return render(request,"upload.html",{"file_list":file_list})
    elif request.method == "POST":
        user = request.POST.get("user")
        obj = request.FILES.get("foo")
        file_path = os.path.join("static","upload",obj.name)
        f = open(file_path,"wb")
        for chunk in obj.chunks():
            f.write(chunk)
        f.close()
        ret = {"status": True, "path":file_path}
        models.Upload.objects.create(path=file_path)
        # return redirect("/upload.html") form 表单提交
        return HttpResponse(json.dumps(ret)) # xhrHttpRequest 和 ajax 提交
    else:
        return redirect("/login.html")
