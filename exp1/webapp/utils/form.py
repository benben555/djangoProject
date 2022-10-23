from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from webapp.utils.encrypt import md5
from webapp import models
from webapp.utils.bootstrap import BootStrapModelForm, BootStrapForm


class UserModelForm(BootStrapModelForm):
    name = forms.CharField(min_length=3, label="用户名")

    class Meta:
        model = models.UserInfo
        fields = ["name", "password", "age", "account", "create_time", "depart", "gender"]
        # widgets = {
        #     "name": forms.TextInput(attrs={"class": "form-control"}),
        #     "password": forms.PasswordInput(attrs={"class": "form-control"})
        # }

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for name, field in self.fields.items():
    #         # if name=="password":
    #         #     continue
    #         field.widget.attrs = {"class": "form-control", "placeholder": field.label}


class PrettyModelForm(BootStrapModelForm):
    mobile = forms.CharField(
        label="手机号",
        # validators=[RegexValidator(r'^159[0-9]+$', '数字必须以159开头')],
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误'), ]
    )

    class Meta:
        model = models.PrettyNum
        fields = ["mobile", "price", "level", "status"]
        # fields="__all__"
        # exclude =['level']

    def clean_mobile(self):
        txt_mobile = self.cleaned_data['mobile']
        exists = models.PrettyNum.objects.filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError("手机号已存在")
        if len(txt_mobile) != 11:
            raise ValidationError("格式错误")
        return txt_mobile


class PrettyEditModelForm(BootStrapModelForm):
    mobile = forms.CharField(
        # disabled=True,
        label="手机号",
        # validators=[RegexValidator(r'^159[0-9]+$', '数字必须以159开头')],
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误'), ]
    )

    class Meta:
        model = models.PrettyNum
        fields = ["mobile", "price", "level", "status"]
        # fields="__all__"
        # exclude =['level']

    def clean_mobile(self):
        txt_mobile = self.cleaned_data['mobile']
        exists = models.PrettyNum.objects.exclude(id=self.instance.pk).filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError("手机号已存在")
        if len(txt_mobile) != 11:
            raise ValidationError("格式错误")

        return txt_mobile


class AdminModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput()
    )  # 自己定义字段

    class Meta:
        model = models.Admin
        fields = ["username", "password", "confirm_password"]
        # 为某些标签定制
        widgets = {
            "password": forms.PasswordInput(render_value=True)  # 输入错误保留密码
        }

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)

    def clean_confirm_password(self):
        # cleaned_data是经过验证后的数据
        confirm = md5(self.cleaned_data.get("confirm_password"))
        pwd = self.cleaned_data.get("password")
        if confirm != pwd:
            raise ValidationError("密码不一致，请重新输入")
        return confirm  # 返回校验字段值


class AdminEditModelForm(BootStrapModelForm):
    class Meta:
        model = models.Admin
        fields = ['username']


class AdminResetModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput()
    )  # 自己定义字段
    widgets = {
        "password": forms.PasswordInput(render_value=True)  # 输入错误保留密码
    }

    class Meta:
        model = models.Admin
        fields = ['password']

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        md5_pwd = md5(pwd)
        exists = models.Admin.objects.filter(id=self.instance.pk, password=md5_pwd).exists()
        if exists:
            raise ValidationError("密码不能和旧密码一致")
        return md5_pwd

    def clean_confirm_password(self):
        # cleaned_data是经过验证后的数据
        confirm = md5(self.cleaned_data.get("confirm_password"))
        pwd = self.cleaned_data.get("password")
        if confirm != pwd:
            raise ValidationError("密码不一致，请重新输入")
        return confirm  # 返回校验字段值


class LoginForm(BootStrapForm):
    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput,
        required=True  # 必填，不能为空
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(render_value=True),  # 密码错误保留密码
        required=True,
    )
    code = forms.CharField(
        label="验证码",
        widget=forms.TextInput(),
        required=True,
    )

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)


class TaskModelForm(BootStrapModelForm):
    class Meta:
        model = models.Task
        fields = "__all__"  # 所有字段
        widgets = {  # 定义插件
            # "detail": forms.Textarea
            "detail": forms.TextInput
        }


class OrderModelForm(BootStrapModelForm):
    class Meta:
        model = models.Order
        # fields = '__all__'
        exclude = ['oid', 'admin']  # 排除


class UpForm(BootStrapForm):
    bootstrap_exclude_fields = ['img']
    name = forms.CharField(label="姓名")
    age = forms.IntegerField(label="年龄")
    img = forms.FileField(label='头像')


class UpModelForm(BootStrapModelForm):
    class Meta:
        model = models.City
        fields = "__all__"
