"""parking URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
import rest

base_url = r"^api/rest/v1"
session = r"(?P<sessid>[0-9a-f\-]+)"

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    url(r'%s/register' % base_url,									'rest.views.register'),
    url(r'%s/login' % base_url,										'rest.views.login'),
    url(r'%s/logout/%s/$' % (base_url,session),						'rest.views.logout'),

    url(r'%s/users/%s/$' % (base_url,session),						'rest.views.user'),
    url(r'%s/users/%s/(?P<uid>\d+)/$' % (base_url,session),			'rest.views.user'),

    url(r'%s/parking/%s/$' % (base_url,session),					'rest.views.parking'),
    url(r'%s/parking/%s/(?P<pid>\d+)/$' % (base_url,session),		'rest.views.parking'),

    url(r'%s/transactionmethod/%s/$' % (base_url,session),			'rest.views.transactionmethod'),

    url(r'%s/spot/%s/my$' % (base_url,session),						'rest.views.spot_my'),
    url(r'%s/spot/%s/(?P<sid>\d+)/$' % (base_url,session),			'rest.views.spot'),
    url(r'%s/spot/%s/(?P<sid>\d+)/free/$' % (base_url,session),		'rest.views.spot_free'),

    url(r'%s/freespot/%s/$' % (base_url,session),					'rest.views.freespot'),
    url(r'%s/freespot/%s/(?P<pid>\d+)/$' % (base_url,session),		'rest.views.freespot'),

    url(r'%s/wallet/%s/$' % (base_url,session),						'rest.views.wallet'),
    url(r'%s/wallet/%s/withdraw' % (base_url,session),				'rest.views.withdraw'),

    url(r'%s/transaction/%s/$' % (base_url,session),				'rest.views.transaction'),
    url(r'%s/transaction/%s' % (base_url,session),					'rest.views.transaction'),

    url(r'%s/car/%s/$' % (base_url,session),						'rest.views.car'),
    url(r'%s/car/%s/(?P<cid>\d+)/$' % (base_url,session),			'rest.views.car'),
    url(r'%s/car-add/%s/(?P<plate>.*)$' % (base_url,session),		'rest.views.car_add'),

    url(r'%s/code/%s/(?P<cid>\d+)/$' % (base_url,session),			'rest.views.code'),

    url(r'%s/reservation/%s/$' % (base_url,session),				'rest.views.reservation'),
    url(r'%s/reservation/%s' % (base_url,session),					'rest.views.reservation'),
    url(r'%s/reservation-prolong/%s/(?P<rid>\d+)' % (base_url,session),'rest.views.reservation_prolong'),

    url(r'%s/search/%s' % (base_url,session),						'rest.views.search'),
    url(r'%s/notifications/%s' % (base_url,session),				'rest.views.notifications'),


    url(r'%s/payment/(?P<wid>\d+)' % base_url,						'rest.views.payment'),
    url(r'%s/open/(?P<data>.*)$' % base_url,						'rest.views.open'),
]
