import random

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from datetime import datetime

from webapp import models
from webapp.utils.form import OrderModelForm
from webapp.utils.pagination import Pagination


def order_list(request):
    queryset = models.Order.objects.all().order_by('-id')
    page_object = Pagination(request, queryset)
    form = OrderModelForm()
    context = {
        "form": form,
        "queryset": page_object.page_queryset,
        "page_string": page_object.html()
    }

    return render(request, "order_list.html", context)


@csrf_exempt
def order_add(request):
    form = OrderModelForm(data=request.POST)  # 获取用户提交的数据
    if form.is_valid():
        # 应该保存到数据库中 title price status admin_id
        form.instance.oid = datetime.now().strftime("%Y%m%d%H%M%S") + str(random.randint(1000, 9999))
        form.instance.admin_id = request.session['info']['id']
        form.save()
        return JsonResponse({"status": True})
    return JsonResponse({"status": False, "error": form.errors})


def order_delete(request):
    uid = request.GET.get('uid')
    exists = models.Order.objects.filter(id=uid).exists()
    if not exists:
        return JsonResponse({"status": False, "error": "删除失败，数据不存在"})
    models.Order.objects.filter(id=uid).delete()
    return JsonResponse({"status": True})


def order_detail(request):
    # uid = request.GET.get('uid')
    # row_object = models.Order.objects.filter(id=uid).first()
    # if not row_object:
    #     return JsonResponse({"status": False, "error": "编辑失败，数据不存在"})
    # result = {
    #     "status": True,
    #     "data": {
    #         "title": row_object.title,
    #         "price": row_object.price,
    #         "status": row_object.status,
    #     }
    # }
    # return JsonResponse(result)
    uid = request.GET.get('uid')
    row_object = models.Order.objects.filter(id=uid).values("title", 'price', 'status').first()
    if not row_object:
        return JsonResponse({"status": False, "error": "编辑失败，数据不存在"})
    result = {
        "status": True,
        "data": row_object
    }
    return JsonResponse(result)


@csrf_exempt
def order_edit(request):
    uid = request.GET.get('uid')
    row_object = models.Order.objects.filter(id=uid).first()
    if not row_object:
        return JsonResponse({"status": False, "tips": "编辑失败，数据不存在"})
    form = OrderModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": True})
    return JsonResponse({"status": False, "error": form.errors})
