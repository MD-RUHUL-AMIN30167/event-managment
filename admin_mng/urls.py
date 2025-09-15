from django.urls import path
from admin_mng.views import sign_up,sign_in,sign_out,all_event,admin_details,admin_list,create_group,groups_list,activate_user,main_dashbord

urlpatterns =[
    path('sign_up/',sign_up,name='sign_up'),
    path('sign_in/',sign_in,name='sign_in'),
    path('sign_out/',sign_out,name='sign_out'),
    # path('admin_dashbord/',admin_dashbord,name='admin_dashbord'),
    path('all_event/',all_event,name='all_event'),
    path('admin_details/<int:event_id>/',admin_details,name='admin_details'),
    path('admin_list/',admin_list,name='admin_list'),
    path('create_group/',create_group,name='create_group'),
    path('groups_list/',groups_list,name='groups_list'),
    path('activate/<int:user_id>/<str:token>/', activate_user),
    path('main_dashbord/',main_dashbord,name='main_dashbord'),

]