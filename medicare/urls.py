from django.conf.urls import url

from . import views

from django.conf.urls import include


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^profile/$',views.profile,name='profile'),
    url(r'^profile/update/(?P<pk>\d+)/$',views.StudentProfileUpdate.as_view(),name='profile-update'),
    url(r'^profile/updatedoc/(?P<pk>\d+)/$', views.DoctorProfileUpdate.as_view(), name='profile-updatedoc'),
    url(r'^viewprofile/(?P<doc_id>\d+)/$',views.doctorinfo,name='docinfo'),
    url(r'^doclist/(?P<doctype>\d+)/$',views.doclist,name='doclist'),
]
urlpatterns += [
    url(r'^prescription/create/$', views.PrescriptionCreate.as_view(), name='prescription_create'),
    url(r'^prescription/(?P<pk>\d+)/update/$', views.PrescriptionUpdate.as_view(), name='prescription_update'),
    url(r'^prescription/(?P<pk>\d+)/delete/$', views.PrescriptionDelete.as_view(), name='prescription_delete'),
    url(r'^prescriptiondetail/(?P<pk>\d+)/$', views.prescriptiondetail, name='prescription-detail'),
    url(r'^prescriptionlist/$', views.prescriptionlist, name='prescription-list'),
]