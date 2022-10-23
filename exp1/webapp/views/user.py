from django.shortcuts import render, redirect

from webapp import models
from webapp.utils.form import UserModelForm
from webapp.utils.pagination import Pagination


def user_list(request):
    queryset = models.UserInfo.objects.all()
    # for obj in queryset:
    #     print(obj.create_time.strftime("%Y-%m-%d"),obj.get_gender_display(),obj.depart.title)
    page_object = Pagination(request, queryset, page_size=2)
    context = {"queryset": page_object.page_queryset,
               "page_string": page_object.html()}
    return render(request, "user_list.html", context)


def user_add(request):
    if request.method == "GET":
        context = {
            'gender_choices': models.UserInfo.gender_choice,
            'depart_list': models.Department.objects.all()
        }

        return render(request, "user_add.html", context)
    #
    name = request.POST.get("name")
    pwd = request.POST.get("pwd")
    age = request.POST.get("age")
    account = request.POST.get("account")
    time = request.POST.get("time")
    dp = request.POST.get("dp")
    gender = request.POST.get("gender")
    models.UserInfo.objects.create(name=name, password=pwd, age=age, account=account, create_time=time, depart_id=dp,
                                   gender=gender)
    return redirect("/user/list/")


def user_model_form_add(request):
    if request.method == "GET":
        form = UserModelForm()
        return render(request, "user_model_form_add.html", {"form": form})
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        # print(form.cleaned_data)
        form.save()
        return redirect('/user/list/')
    return render(request, "user_model_form_add.html", {"form": form})


def user_edit(request, nid):
    row_object = models.UserInfo.objects.filter(id=nid).first()
    if request.method == "GET":
        form = UserModelForm(instance=row_object)
        return render(request, "user_edit.html", {'form': form})
    form = UserModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        # 默认保存的是用户输入的所有数据
        # form.instance.字段名=值，如果想要在用户输入意外增加一些值
        form.save()
        return redirect('/user/list/')
    return render(request, 'user_edit.html', {'form': form})


def user_delete(request, nid):
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect('/user/list/')
