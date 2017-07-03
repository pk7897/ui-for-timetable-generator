from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^processind/(?P<id>[0-9]+)$',views.processindex, name='processind'),
    url(r'^Class$', views.processClass, name='Class'),
    url(r'^Generate$', views.Generate, name='generate'),
    url(r'^Group/(?P<name>\S+)$', views.addGroup, name='Group'),
    url(r'^processGroup$',views.processGroup, name='processGroup'),
    url(r'^addSub/(?P<id>[0-9]+)$', views.addSubject, name='Sub'),
    url(r'^processSub/(?P<id>[0-9]+)$',views.processSub, name='processSub'),
    url(r'^addFac/(?P<id>[0-9]+)$', views.addFaculty, name='Fac'),
    url(r'^processFac/(?P<id>[0-9]+)$',views.processFaculty, name='processFac'),
    url(r'^mul_fac/(?P<id>[0-9]+)$', views.multiple_faculty, name='mul_fac'),
    url(r'^processWH/(?P<id>[0-9]+)$',views.processWH, name='processWH'),
    url(r'^processConstraints/(?P<id>[0-9]+)$',views.processConstraints, name='processConstraints'),
    url(r'^HandleSub$',views.HandleSub, name='HandleSub'),
    url(r'^Optionald$',views.Optionald, name='Optionald'),
    url(r'^displconstr/(?P<id>[0-9]+)$',views.displconstr, name='displconstr'),
    url(r'^Optional$',views.Optional, name='Optional'),
    url(r'^HandleFac$',views.HandleFac, name='HandleFac'),
]
