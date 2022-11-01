from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

class LoginView(View):

  def get(self,request):
    #逻辑代码
    return render(request,'login.html')

  def post(self,request):
    # 获取前端传递过来的用户名和密码
    username = request.POST.get('username')
    pwd = request.POST.get('pwd')
    record = request.POST.get('record')
    # 进行数据校验
    if not all([username,pwd]):
      return HttpResponse('数据输入不完整')
    # 验证用户名和密码是否正确
    user = authenticate(username=username,password=pwd)
    return render(request,''index.html')