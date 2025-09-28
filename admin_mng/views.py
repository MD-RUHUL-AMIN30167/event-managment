from django.shortcuts import render,get_object_or_404,redirect,HttpResponse
from django.contrib.auth.models import User,Group,Permission
from django.contrib.auth.forms import UserCreationForm
from admin_mng.forms import UserCreationForm,CustomRegistrationForm,CreateGroupForm
from django.shortcuts import redirect
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from admin_mng.forms import LoginForm
from event_App.forms import Event,Participant,ParticipantForm

from admin_mng.forms import EditProfileForm
from admin_mng.models import CustomUser

from django.db.models import Prefetch
from django import forms
from datetime import datetime
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required,user_passes_test
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin,PermissionRequiredMixin

from django.views.generic import DetailView,ListView,TemplateView,UpdateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import get_user_model
User=get_user_model()

# CreateLoginFrom
def is_admin(user):
    return user.groups.filter(name='Admin').exists()

def is_manager(user):
    return user.groups.filter(name='Manager').exists()

def is_admin_or_manager(user):
    return is_admin(user) or is_manager(user)

def is_employee(user):
    return user.groups.filter(name='Employee').exists()
"""
@login_required
@user_passes_test(is_admin,login_url='no_permission')
def all_event(request):
    
    query = request.GET.get('q')  
    if query:
        events = Event.objects.filter(name__icontains=query)
    else:
        events = Event.objects.all()

    
    context = {
        
        'events': events,       
        'query': query,          
    }
    return render(request, 'admin/admin_event.html', context)
"""

"""CBV """

class All_Event_View_Admin(LoginRequiredMixin,UserPassesTestMixin,ListView):
    model=Event
    template_name="admin/admin_event.html"
    context_object_name="events"

    def test_func(self):
        return is_admin(self.request.user)
    
    def handle_no_permission(self):
        return redirect('no_permission')
    
    def get_queryset(self):
        query= self.request.GET.get('q')
        if query:
            return Event.objects.filter(name__icontains=query)
        return Event.objects.all()
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context["query"]=self.request.GET.get('q')
        return context


def sign_up(request):
    form=CustomRegistrationForm()
    if request.method == 'POST':
        form=CustomRegistrationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False) 
            user.set_password(form.cleaned_data.get('password'))
            user.is_active=False  #administration er User er active statue sendmail pathoner age unactive kore
            user.save()
            print("User created:", user.username)
            
            messages.success(request,'Your mail send successfull')
        
        return redirect('sign_in')
    
    return render(request,'registration/sign_up.html',{'form':form})
 

from django.contrib import messages

def sign_in(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('main_dashbord')
        else:
            messages.error(request, "⚠️ Username Or Password Wrong !")
    return render(request, 'registration/sign_in.html', {'form': form})

class CustomLoginView(LoginView):
    form_class=LoginForm
    template_name='registration/sign_in.html'
    next_page=reverse_lazy('main_dashbord')
    def get_success_url(self):
        next_url=self.request.GET.get('next')
        return next_url if next_url else super().get_success_url()



@login_required
def sign_out(request):
    logout(request)
    next_url=request.POST.get('next')
    if next_url:
        return redirect('next_url')
    return redirect('/event_App/index/')
    
@login_required
@user_passes_test(is_admin,login_url='no_permission')
def admin_list(request):
    users = User.objects.prefetch_related(
        Prefetch('groups', queryset=Group.objects.all(), to_attr='all_group')
    ).all()

    for user in users:
        if user.all_group:  
            user.group_name = user.all_group[0].name
        else:
            user.group_name = 'No Group Assigned'

    return render(request, 'admin/admin_list.html', {"users": users})


"""
@login_required
@user_passes_test(is_admin,login_url='no_permission')
def admin_details(request, event_id):
    event = Event.objects.get(id=event_id)
    return render(request, 'admin/admin_details.html', {'event': event})
"""
"CBV with admin details"

class Details_Event_Admin(LoginRequiredMixin,UserPassesTestMixin,DetailView):
    model=Event
    template_name='admin/admin_details.html'
    context_object_name='event'
    pk_url_kwarg="event_id"

    def handle_no_permission(self):
        return redirect('no_permission')
    def test_func(self):
        return is_admin(self.request.user)
# create group admin and manager 
@login_required
@user_passes_test(is_admin,login_url='no_permission')
def create_group(request):
    form=CreateGroupForm()
    if request.method == 'POST':
        form=CreateGroupForm(request.POST)
        if form.is_valid():
            group=form.save()
            messages.success(request,f"Group {group.name} has been created successfully")
            return redirect('create_group')
    return render(request,'admin/create_group.html',{'form':form})



# groups list show admin
@login_required
@user_passes_test(is_admin,login_url='no_permission')

def groups_list(request):
    groups=Group.objects.all()
    return render(request,'admin/groups_list.html',{'groups':groups})


def activate_user(request, uid, token):
    try:
        user = get_object_or_404(User, pk=uid)
        
        
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, "Your account has been activated successfully!")
            return redirect("sign_in")
        else:
            messages.error(request, "Activation link is invalid or expired.")
            return redirect("sign_up")
    except Exception as e:
        messages.error(request, f"Error: {e}")
        return redirect("sign_up")
    
"""CBV with profile view """
class ProfileView(LoginRequiredMixin,TemplateView):
    template_name='accounts/dashbord_profile.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user=self.request.user
        context["username"] =user.username 
        context["email"]=user.email
        context['name']=user.get_full_name()
        context['user_joinded']=user.date_joined
        context['user_last_login']=user.last_login
      
        context["profile_image"] = getattr(user, 'profile_image', None)
        if context["profile_image"]:
            context["profile_image"] = user.profile_image.url
        else:
            context["profile_image"] = "https://via.placeholder.com/120"        
        context["bio"] = user.bio

        return context
    
class EditProfileView(UpdateView):
    model=CustomUser
    form_class=EditProfileForm
    template_name='edit_profile.html'
    context_object_name='form'

    def get_object(self):
        return self.request.user
    def form_valid(self, form):
        form.save(commit=True)
        return redirect('profile')
# main Dashbord

def main_dashbord(request):
    if is_admin(request.user):
        return redirect('all_event')
    elif is_manager(request.user):
        return redirect('manager_dashbord')
    elif is_employee(request.user):
        return redirect('index')
    else:
        return redirect('no_permission') 