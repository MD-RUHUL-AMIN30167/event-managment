from django.urls import path
from.views import  manager_dashbord,manager_create_event,mng_details
urlpatterns = [
    path('manager_dashbord/',manager_dashbord,name='manager_dashbord'),
    path('manager_create_event/',manager_create_event,name='manager_create_event'),
    path('manager_dashbord/',manager_dashbord,name='manager_dashbord'),
    path('mng_details/<int:event_id>/',mng_details,name='mng_details'),
    # path('event/<int:event_id>/', event_detail, name='event_detail')
]
