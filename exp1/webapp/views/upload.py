import os.path

from django.http import HttpResponse
from django.shortcuts import render

from exp1 import settings
from webapp import models
from webapp.utils.form import UpForm, UpModelForm


def upload_list(request):
    if request.method == "GET":
        return render(request, 'upload_list.html')
    print(request.POST)  # 请求体中数据
    file_object = request.FILES.get("avatar", None)
    f = open("a1.txt", mode='wb')
    for chunk in file_object.chunks():
        f.write(chunk)
    f.close()
    print(file_object.name)
    return HttpResponse("...")


def upload_form(request):
    title = "Form上传"
    if request.method == "GET":
        form = UpForm()
        return render(request, "upload_form.html", {"form": form, "title": title})
    form = UpForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        image_object = form.cleaned_data.get('img')
        # file_path = os.path.join("webapp", "static", "img", image_object.name)
        # db_file_path = os.path.join("http://127.0.0.1:8000", "static", "img", image_object.name)
        # media_path = os.path.join(settings.MEDIA_ROOT, image_object.name)  # 绝对路径
        media_path = os.path.join('media', image_object.name)
        f = open(media_path, mode='wb')
        for chunk in image_object.chunks():
            f.write(chunk)
        f.close()
        models.Boss.objects.create(
            name=form.cleaned_data['name'],
            age=form.cleaned_data['age'],
            img=media_path,
        )
        return HttpResponse("...")
    return render(request, "upload_form.html", {"form": form, "title": title})


def upload_model_form(request):
    title = "ModelForm上传"
    if request.method == "GET":
        form = UpModelForm()
        return render(request, "upload_form.html", {"form": form, "title": title})
    form = UpModelForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        form.save()
        return render(request, "upload_form.html")
    return render(request, "upload_form.html", {"form": form, "title": title})
