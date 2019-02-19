from . import models
from django.shortcuts import render, redirect
from .forms import RegisterForm, ActiveForm, ForgetForm, ResetForm
import hashlib
from login.utils.email_send import youjian
from .models import User, EmailVerifyRecord
from django.views.generic import View


def home(request):
    pass
    return render(request, 'login/home.html')


def login(request):
    # if request.session.get('is_login', None):
    #     return redirect('/')
    if request.method == "POST":
        email = request.POST.get('email', None)
        password = request.POST.get('pwd', None)
        message = "All fields must be filled in!"
        if email and password:  # 确保用户名和密码都不为空
            email = email.strip()
            try:
                email = models.User.objects.get(email=email)
                if email.password == hash_code(password):
                    if email.isactivate == 1:
                        # request.session['is_login'] = True
                        # request.session['user_id'] = User.id
                        # request.session['user_name'] = User.email
                        return redirect('/')
                    else:
                        message = "User is inactivated!"
                        return render(request, 'login/login.html', {"message": message})
                else:
                    message = "Incorrect password！"
            except:
                message = "Username does not exist！"
            return render(request, 'login/login.html', {"message": message})
        else:
            return render(request, 'login/login.html', {"message": message})
    return render(request, 'login/login.html')


def register(request):
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "Please check the password length！"
        if register_form.is_valid():  # 获取数据
            email = register_form.cleaned_data['email']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            if password1 != password2:  # 判断两次密码是否相同
                message = "The passwords entered twice are different！"
                return render(request, 'login/register.html', locals())
            else:
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:  # 邮箱地址唯一
                    message = "This email address has been registered!Please use another email address."
                    return render(request, 'login/register.html', locals())

                # 当一切都OK的情况下，创建新用户

                new_user = models.User.objects.create()
                new_user.email = email
                new_user.isactivate = False
                new_user.password = hash_code(password1)
                new_user.save()
                youjian(email, 'register')
                message = "Successful registration! Please go to email to activate."
                return render(request, 'login/register.html', locals())
    register_form = RegisterForm()
    return render(request, 'login/register.html', locals())


def logout(request):
        pass
        return redirect("/")


def hash_code(s, salt='mysite'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()


class ActiveUserView(View):
    def get(self, request, active_code):
        # 用于查询邮箱验证码是否存在
        all_record = EmailVerifyRecord.objects.filter(code=active_code)
        # 如果不为空也就是有用户
        active_form = ActiveForm(request.GET)
        if all_record:
            for record in all_record:
                # 获取到对应的邮箱
                email = record.email
                # 查找到邮箱对应的用户
                new_user = User.objects.get(email=email)
                new_user.isactivate = True
                new_user.save()
                # 激活成功跳转到登录页面
                return render(request, "login.html", )
        else:
            return render(request, "register.html", {"msg": "您的激活链接无效", "active_form": active_form})


class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, 'forget.html', {'forget_form': forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email', '')
            youjian(email, 'forget')
            return render(request, 'success_send.html')
        else:
            return render(request, 'forget.html', {'forget_form': forget_form})


class ResetView(View):
    def get(self, request, active_code):
        record = EmailVerifyRecord.objects.filter(code=active_code)
        print(record)
        if record:
            for i in record:
                email = i.email
                is_register = User.objects.filter(email=email)
                if is_register:
                    return render(request, 'pwd_reset.html', {'email': email})
        return redirect('')


class ModifyView(View):
    def post(self, request):
        reset_form = ResetForm(request.POST)
        if reset_form.is_valid():
            pwd1 = request.POST.get('newpwd1', '')
            pwd2 = request.POST.get('newpwd2', '')
            email = request.POST.get('email', '')
            if pwd1 != pwd2:
                return render(request, 'pwd_reset.html', {'msg': '密码不一致！'})
            else:
                user = User.objects.get(email=email)
                user.password = hash_code(pwd2)
                user.save()
                return redirect('/')
        else:
            email = request.POST.get('email', '')
            return render(request, 'pwd_reset.html', {'msg': reset_form.errors})