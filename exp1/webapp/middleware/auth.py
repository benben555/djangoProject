from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin


class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # 0排除那些不需要登录就可以访问的页面
        # request.path_info 获取当前用户访问的url /login/
        if request.path_info in ['/login/', '/image/code/']:
            return
        # 1读取当前访问的用户的session信息，如果能读到，说明以及登录过
        info_dict = request.session.get("info")
        # print(info_dict)
        if info_dict:
            return
        # 2如果没有登录过，显示未登录
        return redirect('/login/')

    def process_response(self, request, response):
        return response

# class M2(MiddlewareMixin):
#     def process_request(self, request):
#         print("m2")
#
#     def process_response(self, request, response):
#         print("go")
#         return response
