from django.urls import path
from.views import  event_detail,crud_event,update_event, index,booking,contact,event,about,category,create_event,delete_event,event_list,no_permission

urlpatterns = [

    path('index/',index,name='index'),
    path('booking/',booking,name='booking'),
    path('contact/',contact,name='contact'),
    path('event/',event,name='event'),
    path('about/',about,name='about'),
    path('category/',category,name='category'),
    path('create_event/',create_event,name='create_event'),
    path('crud_event/',crud_event,name='crud_event'),
    path('update_event/<int:id>/',update_event,name='update_event'),
    path('delete_event/<int:id>/',delete_event,name='delete_event'),
    path('events/',event_list, name='event_list'),
    
    path('event/<int:event_id>/', event_detail, name='event_detail'),

    path('no_permission/',no_permission,name='no_permission'),
]
