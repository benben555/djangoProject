from django.shortcuts import render, redirect

from webapp import models
from webapp.utils.form import PrettyEditModelForm, UserModelForm, PrettyModelForm
from webapp.utils.pagination import Pagination


def pretty_list(request):
    # get_query_dict=copy.deepcopy(request.GET)
    # page = request.GET.get("page", 1)
    # page = int(page)
    # page_size = 10
    # start = (page - 1) * page_size
    # end = page * page_size
    # queryset=models.PrettyNum.objects.filter(**page)
    # q=models.PrettyNum.objects.filter(mobile=1)
    # for i in range(300):
    #     models.PrettyNum.objects.create(mobile="15072873046",price=10,level=1,status=1)
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["mobile__contains"] = search_data
    # res = models.PrettyNum.objects.filter(**data_dict)
    queryset = models.PrettyNum.objects.filter(**data_dict).order_by("-level")

    page_object = Pagination(request, queryset)
    page_queryset = page_object.page_queryset
    page_string = page_object.html()
    context = {
        "search_data": search_data,
        "queryset": page_queryset,
        "page_string": page_string
    }
    # total_count = models.PrettyNum.objects.filter(**data_dict).order_by("-level").count()
    # total_page_count, div = divmod(total_count, page_size)
    # if div:
    #     total_page_count += 1
    # plus = 5
    # start_page = max(1, min(page - 5, total_page_count - 2 * plus))
    # end_page = min(total_page_count, max(2 * plus + 1, page + plus))
    # if total_page_count <= 2 * plus + 1:
    #     start_page = 1
    #     end_page = total_page_count
    # else:
    #     if page <= plus:
    #         start_page = 1
    #         end_page = 2 * plus
    #     else:
    #         if page + plus > total_page_count:
    #             start_page=total_page_count-2*plus
    #             end_page = total_page_count
    #         else:
    #             start_page = page - plus
    #             end_page = page + plus
    # page_str_list.append('<li><a href="?page={}">首页</a></li>'.format(1))
    # prev = '<li><a href="?page={}">上一页</a></li>'.format(max(1,page - 1))
    #
    # page_str_list.append(prev)
    # for i in range(start_page, end_page + 1):
    #     if i == page:
    #         ele = '<li class="active"><a href="?page={}">{}</a></li>'.format(i, i)
    #     else:
    #         ele = '<li><a href="?page={}">{}</a></li>'.format(i, i)
    #     page_str_list.append(ele)
    # nextv = '<li><a href="?page={}">下一页</a></li>'.format(min(total_page_count, page + 1))
    # page_str_list.append(nextv)
    # page_str_list.append('<li><a href="?page={}">尾页</a></li>'.format(total_page_count))
    # page_string = mark_safe("".join(page_str_list))  # 后段写界面
    return render(request, "pretty_list.html", context)


def pretty_add(request):
    if request.method == "GET":
        form = PrettyModelForm()
        return render(request, "pretty_add.html", {"form": form})
    form = PrettyModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/pretty/list/')
    return render(request, "pretty_add.html", {"form": form})


def pretty_edit(request, nid):
    row_object = models.PrettyNum.objects.filter(id=nid).first()
    if request.method == "GET":
        form = UserModelForm(instance=row_object)
        return render(request, "pretty_edit.html", {'form': form})
    form = PrettyEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        # 默认保存的是用户输入的所有数据
        # form.instance.字段名=值，如果想要在用户输入意外增加一些值
        form.save()
        return redirect('/pretty/list/')
    return render(request, 'pretty_edit.html', {'form': form})


def pretty_delete(request, nid):
    models.PrettyNum.objects.filter(id=nid).delete()
    return redirect('/pretty/list/')
