from django.urls import path
from.views import  manager_create_event,Mng_Details_View,All_Event_Details_Manager,MngProfileView
from django.contrib.auth.views import LogoutView,PasswordChangeView,PasswordChangeDoneView
urlpatterns = [
    #path('manager_dashbord/',manager_dashbord,name='manager_dashbord'),
    path('manager_dashbord/',All_Event_Details_Manager.as_view(),name='manager_dashbord'),
    path('manager_create_event/',manager_create_event,name='manager_create_event'),
    # path('manager_dashbord/',manager_dashbord,name='manager_dashbord'),
    # path('mng_details/<int:event_id>/',mng_details,name='mng_details'),
    path('mng_details/<int:event_id>/',Mng_Details_View.as_view(),name='mng_details'),
    path('profile/',MngProfileView.as_view(),name='mng_profile'),
    
]
