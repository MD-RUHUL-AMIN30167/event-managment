from django.shortcuts import render
from django.shortcuts import render,get_object_or_404,redirect,HttpResponse
from django.contrib.auth.models import User,Group,Permission
from django.contrib.auth.forms import UserCreationForm
from admin_mng.forms import UserCreationForm,CustomRegistrationForm,CreateGroupForm
from django.shortcuts import redirect
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from admin_mng.forms import LoginForm
from event_App.forms import Event,Participant,ParticipantForm
from django.db.models import Prefetch
from django import forms
import time
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin,PermissionRequiredMixin

from django.contrib.auth.tokens import default_token_generator
from event_App. forms import ParticipantForm,CategoryForm,EventForm
from django.contrib.auth.decorators import login_required,user_passes_test
from admin_mng.views import is_admin,is_employee,is_manager,is_admin_or_manager
from django.views.generic import DetailView,ListView,TemplateView
from django.contrib.auth import get_user_model
User=get_user_model()
"""
@login_required
@user_passes_test(is_admin_or_manager,login_url='no_permission')
def manager_dashbord(request):
    
    query = request.GET.get('q')  
    if query:
        events = Event.objects.filter(name__icontains=query)
    else:
        events = Event.objects.all()

    
    context = {
        
        'events': events,       
        'query': query,          
    }
    return render(request, 'manager_dashbord.html', context)
"""

"""CBV with manager dashbord all event"""
class All_Event_Details_Manager(LoginRequiredMixin,UserPassesTestMixin,ListView):
    model=Event
    template_name='manager_dashbord.html'
    context_object_name='events'
    def test_func(self):
        return is_admin_or_manager(self.request.user)
    def handle_no_permission(self):
        return redirect('no_permission')
    
    def get_queryset(self):
        query=self.request.GET.get('q')
        if query:
            return Event.objects.filter(name__icontains=query)
        return Event.objects.all()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] =self.request.GET.get('q') 
        return context
    
@login_required
@user_passes_test(is_admin_or_manager,login_url='no_permission')
def manager_create_event(request):

    event_form=EventForm()
    if request.method == 'POST':
        event_form = EventForm(request.POST, request.FILES) 
        print("event1")
        if event_form.is_valid():
            print("event2")
            event_form.save()
            print("event2")
            messages.success(request, "Event created successfully!")
            return redirect('manager_dashbord') 
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        event_form = EventForm()

    context = {
        "event_form": event_form,
        "form_title": "Create Event",
        "submit_label": "Create",
        
    }

    return render(request, 'mng_create_event.html', context)
# @login_required
# @user_passes_test(is_admin_or_manager,login_url="no_permission")

"""
def mng_details(request, event_id):
    event = Event.objects.get(id=event_id)
    return render(request, 'mng_details.html', {'event': event})
"""

"""CBV with mng_details"""
class Mng_Details_View(LoginRequiredMixin,UserPassesTestMixin,DetailView):
    model=Event
    template_name='mng_details.html'
    pk_url_kwarg='event_id'
    context_object_name='event'
    def test_func(self):
        return is_admin_or_manager(self.request.user)
    def handle_no_permission(self):
        return redirect('no_permission')

"""CBV with profile view """
class MngProfileView(TemplateView):
    template_name='mng_profile.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user=self.request.user
        context["username"] =user.username 
        context["email"]=user.email
        context['name']=user.get_full_name()
        context['user_joinded']=user.date_joined
        context['user_last_login']=user.last_login

        return context


class ProfileView(TemplateView):
    template_name='mng_profile.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user=self.request.user
        context["username"] =user.username 
        context["email"]=user.email
        context['name']=user.get_full_name()
        context['user_joinded']=user.date_joined
        context['user_last_login']=user.last_login
        context["profile_image"] = user.profile_image.url if user.profile_image else None
        context["bio"] = user.bio
