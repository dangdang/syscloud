# coding=utf-8
'''
Created on 2012-11-5

@author:  Lion
@email: 11315889@qq.com

'''
from Syscloud_Pannel import models, settings
from Syscloud_Pannel.forms import OrderForm, CreateUserForm, LogonForm, \
    RechargeForm
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.timezone import now

def home(request,**k):
    
    if request.method=='POST' and k.get('logon',0)!=1:
        sessionuser=request.session.get('username',None);
        request.session['order_step']=1
        request.session['order_data']=request.POST
        if sessionuser==None:
            return logon(request,order=1)
        form = OrderForm(request.POST)
        if form.is_valid():
           # assert False
            if(int(request.POST.get('confirm',0))==1):
                order=form.handle(request)
                if order:
                    return  dashboard(request)
                else:
                    return  HttpResponse("Order has error.")
            else:
                
                flavor= models.Flavor.objects.get(id=request.POST['flavor'])
                image=models.Image.objects.get(id=request.POST['image'])
                region=models.Region.objects.get(id=request.POST['region'])
                bandwith=models.Bandwith.objects.get(id=request.POST['bandwith'])
                host_count=int(request.POST['host_count'])
                payment=request.POST.get('payment',None)
                if payment=='price_hour':
                    payables=(flavor.price_hour + image.price_hour + bandwith.price_hour)* (host_count)
                elif payment=='price_day':
                    payables=(flavor.price_day + image.price_day + bandwith.price_day)* (host_count)
                elif payment=='price_month':
                    payables=(flavor.price_month + image.price_month + bandwith.price_month)* (host_count)
                elif payment=='price_year':
                    payables=(flavor.price_year + image.price_year + bandwith.price_year)* (host_count)
                else:
                    payables=0
                    return  HttpResponse("请选择付款方式")
                
                confirm_form={
                              'flavor': flavor,
                              'image': image,
                              'region':region,
                              'bandwith':bandwith,
                              'host_count':host_count,
                              'payment':settings.SYSCLOUD_CONFIG['payment'][payment],
                              'payables':payables,
                              'account':models.User.objects.get(username=sessionuser).account,
                              }
                return render(request,'order_confirm.html',{'welcome':'Welcome to Syscloud!','form':form,'confirm_form':confirm_form,'username':request.session.get('username','')})
                
            
    else:
        form=OrderForm()
    return render(request,'home.html',{'welcome':'Welcome to Syscloud!','form':form,'username':request.session.get('username','')})

def dashboard(request):
    username=request.session.get('username',None)
    order_list=models.Order.objects.filter(username=username)
    return render(request,'user/dashboard.html',{'welcome':'用户控制中心','order_list':order_list,'username':username,})
def order_host_count(request):
    return render(request,'')
def logon(request,**k):
    formmsg=''
    if request.method=='POST':
        if k.get('order',None)==1:
            form=LogonForm()
        else:
            form = LogonForm(request.POST)
            if form.is_valid():
                user=form.validateUser(request)
                if user:
                    setlogonsession(request, user)
                    return home(request,logon=1)
                else:
                    formmsg="用户名或者密码错误，请重试！"
                    #return  HttpResponse("LogonForm sumitted has an error.")
    else:
        form=LogonForm()
    return render(request,'user/logon.html',{'formmsg':formmsg,'form':form})

def logout(request):
    request.session.clear()
    return home(request)

def setlogonsession(request,user):
    request.session['username']=user.username
    request.session['logintime']=now()
    
def register(request):
    if request.method=='POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            new_user=form.handle(request)
            if new_user :
                setlogonsession(request,new_user)
                return home(request)
            else:
                return HttpResponse("注册用户失败，可能用户已经存在.")
    else:
        form=CreateUserForm()
    return render(request,'user/register.html',{'welcome':'Welcome to Register!','form':form})

def recharge(request):
    username=request.session.get('username',None)
    if request.method=='POST':
        form = RechargeForm(request.POST)
        if form.is_valid():
            aj=form.handle(request)
            if(aj):
                return HttpResponse("充值成功")
            else:
                return HttpResponse("充值失败.")
    else:
        form = RechargeForm()
        return render(request,'user/recharge.html',{'welcome':'用户控制中心','username':username,'form':form})