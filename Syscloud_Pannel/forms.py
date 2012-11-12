# coding=utf-8
'''
Created on 2012-11-5

@author:  Lion
@email: 11315889@qq.com

'''
from Syscloud_Pannel.models import User, Flavor, Image, Region, Bandwith, Order, \
    AccountJournal
from Syscloud_Pannel.utils import validators
from django import forms
from django.core.exceptions import ObjectDoesNotExist
import logging


class LogonForm(forms.Form):
    username = forms.CharField(max_length=200, label=u'用户名')
    password = forms.CharField(label=u'密码',
                             widget=forms.PasswordInput()
                             )
    def validateUser(self, request):
        
        try:
            user = User.objects.get(username=request.POST['username'], password=request.POST['password'])
            return user
        except ObjectDoesNotExist:
            logging.info("user  %s login failed" % request.POST['username'])
            return False
            

class OrderForm(forms.Form):
    HOST_COUNT_CHOICES = (
    ('1', '1台'),
    ('2', '2台'),
    ('3', '3台'),
)
    PAYMENT_CHOICES = (
                     ('price_hour', '按小时支付'),
                      ('price_day', '按天支付'),
                       ('price_month', '按月支付'),
                       ('price_year', '按年支付'),
                     )
    region = forms.ModelChoiceField(label=u'请选择区域',
                                  queryset=Region.objects.all(),
                                  widget=forms.RadioSelect(),
                                  required=True,
                                  empty_label=None)
     
    flavor = forms.ModelChoiceField(label=u'请选择操作配置类型',
                                  queryset=Flavor.objects.all(),
                                  widget=forms.RadioSelect(),
                                  required=True,
                                  empty_label=None)
    image = forms.ModelChoiceField(label=u'请选择操作系统',
                                  queryset=Image.objects.all(),
                                  widget=forms.RadioSelect(),
                                  required=True,
                                  empty_label=None)
   
    bandwith = forms.ModelChoiceField(label=u'请选择网络带宽',
                                  queryset=Bandwith.objects.all(),
                                  widget=forms.RadioSelect(),
                                  required=True,
                                  empty_label=None)
    host_count = forms.ChoiceField(label=u'请输入要创建的主机数量',
                                 choices=HOST_COUNT_CHOICES,
                                 widget=forms.RadioSelect(),
                                 )
    payment = forms.ChoiceField(label=u'请选择支付方式',
                               choices=PAYMENT_CHOICES,
                               widget=forms.RadioSelect(),
                               )
    def handle(self, request):
        data = request.POST
        #try:
        sessionuser = request.session.get("username", None)
        
        logging.debug('Creating order "%s"' % sessionuser)
        order = Order(username=sessionuser,
                      flavor=Flavor.objects.get(id=data['flavor']),
                      region=Region.objects.get(id=data['region']),
                      image=Image.objects.get(id=data['image']),
                      bandwith=Bandwith.objects.get(id=data['bandwith']),
                      host_count=data['host_count'],
                      )
        logging.debug(order)
        #assert False
        order.save()
        return order
    #except:
        
        logging.debug('Unable to create order. %s' % Exception.message)
        return False
        #return False
    
class CreateUserForm(forms.Form):
    username = forms.CharField(label=("User Name"))
    email = forms.EmailField(label=("Email"))
    password = forms.RegexField(
            label=("Password"),
            widget=forms.PasswordInput(render_value=False),
            regex=validators.password_validator(),
            error_messages={'invalid':validators.password_validator_msg()})
    confirm_password = forms.CharField(
            label=("Confirm Password"),
            required=False,
            widget=forms.PasswordInput(render_value=False))
    company = forms.CharField(label=("Company Name"), required=False)
    real_name = forms.CharField(label=("Real Name"), required=False)
    ID_Card = forms.CharField(label=("ID Card"), required=False)
    mobile = forms.CharField(label=("Mobile"), required=False)
    qq = forms.CharField(label=("QQ"), required=False)

    def handle(self, request):
        data = request.POST
        try:
            logging.info('Creating user with username "%s"' % data['username'])
            new_user = User(
                            username=data['username'],
                            email=data['email'],
                            password=data['password'],
                            company=data['company'],
                            real_name=data['real_name'],
                            ID_Card=data['ID_Card'],
                            mobile=data['mobile'],
                            qq=data['qq'],
                            )
            new_user.save()
            
            return new_user
        except:
            logging.info('Unable to create user.')
            return False

class RechargeForm(forms.Form):
    cash=forms.FloatField(label="请输入充值金额")
    cash_from = forms.CharField(max_length=200)
    cash_remark = forms.CharField(max_length=200)
    
    def handle(self,request):
        data = request.POST
        user=User.objects.get(username=request.session.get('username'))
        try:
            accountJournal=AccountJournal(
                                          user=user,
                                          before=user.account,
                                          cash_amount=data['cash'],
                                          after=user.account+data['cash'],
                                          cash_from=data['cash_from'],
                                          cash_remark=data['cash_remark'],
                                          )
            accountJournal.save()
            return accountJournal
        except:
            return False