from django.conf.urls import patterns, include, url
from django.contrib import admin
#from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
     url(r'^$', 'Syscloud_Pannel.views.home', name='home'),
     url(r'^user/register/','Syscloud_Pannel.views.register',name='register'),
     url(r'^user/logon/','Syscloud_Pannel.views.logon',name='logon'),
     url(r'^user/logout','Syscloud_Pannel.views.logout',name='logout'),
     url(r'^user/dashboard','Syscloud_Pannel.views.dashboard',name='dashboard'),
     url(r'^user/recharge','Syscloud_Pannel.views.recharge',name='recharge'),
     #rl(r'^product/order/','Syscloud_Pannel.views.order',name='order'),
    # url(r'^Syscloud_Pannel/', include('Syscloud_Pannel.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
     
)

#urlpatterns += staticfiles_urlpatterns()