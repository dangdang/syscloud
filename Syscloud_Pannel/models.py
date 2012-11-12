# -*- coding=utf-8
'''
Created on 2012-11-5

@author:  Lion
@email: 11315889@qq.com

'''
from django.contrib import admin
from django.db import models

class Region(models.Model):
    name = models.CharField(max_length=200)
    domainname = models.CharField(max_length=100)
    keystone_ip = models.CharField(max_length=200)
    def __unicode__(self):
        return '%s' % self.name

admin.site.register(Region)

class Flavor(models.Model):
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted = models.BooleanField(default=False)
    region = models.ForeignKey(Region)
    name = models.CharField(max_length=200)
    memory_mb = models.IntegerField()
    vcpus = models.IntegerField()
    swap = models.IntegerField()
    root_gb = models.IntegerField()
    ephemeral_gb = models.IntegerField()
    disabled = models.BooleanField()
    price_hour=models.FloatField()
    price_day = models.FloatField()
    price_month = models.FloatField()
    price_year = models.FloatField()
    def __unicode__(self):
        # (价格[元]:) %s/小时     %s/天    %s/月     %s/年
        #self.price_hour,self.price_day,self.price_month,self.price_year
        return u'%s (价格[元]: %s/小时     %s/天    %s/月     %s/年)' % (self.name,self.price_hour,self.price_day,self.price_month,self.price_year)
        #return self.name

admin.site.register(Flavor)

class Image(models.Model):
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted = models.BooleanField(default=False)
    region = models.ForeignKey(Region)
    name = models.CharField(max_length=200)
    is_public = models.BooleanField(default=True)
    min_disk = models.IntegerField()
    min_ram = models.IntegerField()
    glance_id = models.CharField(max_length=200)
    price_hour=models.FloatField()
    price_day = models.FloatField()
    price_month = models.FloatField()
    price_year = models.FloatField()
    def __unicode__(self):
        return u'%s (价格[元]: %s/小时     %s/天    %s/月     %s/年)' % (self.name,self.price_hour,self.price_day,self.price_month,self.price_year)
        #return '%s' % self.name

admin.site.register(Image)
    
class Bandwith(models.Model):
    region = models.ForeignKey(Region)
    name = models.CharField(max_length=200)
    price_hour=models.FloatField()
    price_day = models.FloatField()
    price_month = models.FloatField()
    price_year = models.FloatField()
    def __unicode__(self):
        return u'%s (价格[元]: %s/小时     %s/天    %s/月     %s/年)' % (self.name,self.price_hour,self.price_day,self.price_month,self.price_year)
        #return '%s' % self.name
    
admin.site.register(Bandwith)
  
class Price(models.Model):
    region = models.ForeignKey(Region)
    name = models.CharField(max_length=200)
    '计费模型，相关产品表名Flavor,Image,Bandwith'
    price_model = models.CharField(max_length=200)
    '计费单位,月，年'
    price_unit = models.CharField(max_length=200)
    '计费单位长度'
    price_size = models.IntegerField()
    price = models.FloatField()
    
admin.site.register(Price)

class Order(models.Model):
    '''
             订单表
    '''
    '用户名'
    username = models.CharField(max_length=200)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True,blank=True)
    deleted = models.BooleanField(default=False)
    '区域'
    region = models.ForeignKey(Region)
    '硬件配置'
    flavor = models.ForeignKey(Flavor)
    '操作系统image'
    image = models.ForeignKey(Image)
    '网络带宽'
    bandwith = models.ForeignKey(Bandwith)
    '计费单位,月，年'
    order_unit = models.CharField(max_length=200,default='month')
    '计费单位长度'
    order_size = models.IntegerField(default='1')
    '硬件单价'
    flavor_price = models.FloatField(default='0')
    '系统单价'
    image_price = models.FloatField(default='0')
    '带宽单价'
    bandwith_price = models.FloatField(default='0')
    '主机数量'
    host_count=models.IntegerField(default=1)
    def __unicode__(self):
        return '%s %s %s %s' %(self.username,self.region,self.flavor,self.bandwith)
    

admin.site.register(Order)

class User(models.Model):
    username = models.CharField(max_length=200, unique=True)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)
    deleted = models.BooleanField(default=False)
    password = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    real_name = models.CharField(max_length=200)
    ID_Card = models.CharField(max_length=200)
    mobile = models.CharField(max_length=200)
    qq = models.CharField(max_length=200, blank=True, null=True)
    account = models.FloatField(default=0.00, null=True)
    enabled = models.BooleanField(default=True)
    def __unicode__(self):
        return '%s' % self.username
    
admin.site.register(User)
    
class AccountJournal(models.Model):
    user = models.ForeignKey(User)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)
    deleted = models.BooleanField(default=False)
    befor = models.FloatField()
    cash_amount=models.FloatField()
    after = models.FloatField()
    cash_from = models.CharField(max_length=200)
    cash_remark = models.CharField(max_length=200)
    cash_operator= models.CharField(max_length=200)
    def __unicode__(self):
        return '%s' % self.username
    
admin.site.register(AccountJournal)
