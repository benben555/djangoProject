from django.http import JsonResponse
from django.shortcuts import render


def chart_list(request):
    return render(request, 'chart_list.html')


def chart_bar(request):
    legend = []
    x_axis = []
    series_list = []
    result = {
        'status': True,
        "data": {
            'legend': legend,
            "series_list": series_list,
            "x_axis": x_axis
        }
    }
    return JsonResponse(result)


def chart_pie(request):
    db_data_list = [{'value': 1048, 'name': 'IT部门'},
                    {'value': 735, 'name': '运营部门'},
                    {'value': 580, 'name': '新媒体部门'},
                    {'value': 484, 'name': '广告部门'}, ]
    result = {
        'status': True,
        "data": db_data_list
    }
    return JsonResponse(result)


def chart_line(request):
    x_axis = {"data": ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']}

    series_list = {"data": [150, 230, 224, 218, 135, 147, 260]}
    result = {
        'status': True,
        "series_list": series_list,
        "x_axis": x_axis
    }
    return JsonResponse(result)
