from django import forms
from captcha.fields import CaptchaField


class RegisterForm(forms.Form):
    password1 = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control'}))


class ActiveForm(forms.Form):
    # 激活时不需要对邮箱的密码做验证
    # 应用验证码，自定义错误输出key必须与异常一样
    captcha = CaptchaField(error_messages={"invalid": u"验证码错误"})
