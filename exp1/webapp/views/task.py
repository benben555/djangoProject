from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from webapp.utils.pagination import Pagination
from webapp import models
from webapp.utils.form import TaskModelForm


def task_list(request):
    queryset = models.Task.objects.all().order_by('-id')
    page_object = Pagination(request, queryset)
    form = TaskModelForm()
    context = {
        "queryset": page_object.page_queryset,
        "form": form,
        "page_string": page_object.html()

    }
    return render(request, "task_list.html", context)


@csrf_exempt  # 取消csrf认证
def task_ajax(request):
    # request.GET

    data_list = {"status": True, "data": [111, 33]}
    # context = json.dumps(data_list)  # 转化为json格式
    # return HttpResponse(context)
    return JsonResponse(data_list)


@csrf_exempt
def task_add(request):
    print(request.POST)
    form = TaskModelForm(data=request.POST)
    if form.is_valid():
        form.save()  # 保存数据库
        data_list = {"status": True}
        # return HttpResponse(json.dumps(data_list))
        return JsonResponse(data_list)
    data_list = {"status": False, "error": form.errors}
    return JsonResponse(data_list)
    # return HttpResponse(json.dumps(data_list, ensure_ascii=False))
