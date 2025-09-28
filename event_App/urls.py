from django.urls import path
from.views import  event_detail,crud_event, index,booking,contact,event,about,category,create_event,event_list,no_permission,UpdateEvent,Delete_Event_View,EventuserProfileView,CustomPasswordResetView,CustomPasswordResetConfirmView
from django.contrib.auth.views import LogoutView,PasswordChangeView,PasswordChangeDoneView
urlpatterns = [

    path('index/',index,name='index'),
    path('booking/',booking,name='booking'),
    path('contact/',contact,name='contact'),
    path('event/',event,name='event'),
    path('about/',about,name='about'),
    path('category/',category,name='category'),
    path('create_event/',create_event,name='create_event'),
    path('crud_event/',crud_event,name='crud_event'),
    # path('update_event/<int:id>/',update_event,name='update_event'),
    path('update_event/<int:id>/',UpdateEvent.as_view(),name='update_event'),
    # path('delete_event/<int:id>/',delete_event,name='delete_event'),
    path('delete_event/<int:id>/',Delete_Event_View.as_view(),name='delete_event'),
    path('events/',event_list, name='event_list'),
    
    path('event/<int:event_id>/', event_detail, name='event_detail'),

    path('no_permission/',no_permission,name='no_permission'),
    path('profile/',EventuserProfileView.as_view(),name='profile'),
    path('password_change/',PasswordChangeView.as_view(template_name='event_user_password_change.html'),name='password_change'),
    path('password_change_done/',PasswordChangeDoneView.as_view(template_name='event_user_password_change_done.html'),name='password_change_done'),

    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset_confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    

]
