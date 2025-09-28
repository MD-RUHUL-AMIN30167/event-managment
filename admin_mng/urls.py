from django.urls import path
from admin_mng.views import sign_up,sign_out,Details_Event_Admin,admin_list,create_group,groups_list,activate_user,main_dashbord,All_Event_View_Admin,CustomLoginView,ProfileView,EditProfileView
from django.contrib.auth.views import LogoutView,PasswordChangeView,PasswordChangeDoneView
urlpatterns =[
    path('sign_up/',sign_up,name='sign_up'),
    # path('sign_in/',sign_in,name='sign_in'),
    path('sign_in/',CustomLoginView.as_view(),name='sign_in'),
    path('sign_out/',sign_out,name='sign_out'),
    #path('sign_out/',LogoutView.as_view(next_page='index'),name='sign_out'),
    # path('admin_dashbord/',admin_dashbord,name='admin_dashbord'),
    # path('all_event/',all_event,name='all_event'),
    path('all_event/',All_Event_View_Admin.as_view(),name='all_event'),                   
    path('admin_details/<int:event_id>/',Details_Event_Admin.as_view(),name='admin_details'),
    path('admin_list/',admin_list,name='admin_list'),
    path('create_group/',create_group,name='create_group'),
    path('groups_list/',groups_list,name='groups_list'),
    path('activate/<int:user_id>/<str:token>/', activate_user),
    path('main_dashbord/',main_dashbord,name='main_dashbord'),


    path('profile/',ProfileView.as_view(),name='profile'),
    # path('password_change/',PasswordChangeView.as_view(template_name='accounts/password_change.html'),name='password_change'),
    # path('password_change_done/',PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'),name='admin_password_change_done'),

    path('edit_profile/',EditProfileView.as_view(),name='edit_profile'),
]