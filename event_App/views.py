from django.shortcuts import render,get_object_or_404
from django.contrib import messages
from django.shortcuts import redirect
from event_App.models import Category,Participant,Event
from event_App. forms import ParticipantForm,CategoryForm,EventForm,CustomPasswordResetForm,CustomPasswordResetConfirmForm
from django.contrib.auth.decorators import login_required,user_passes_test
from admin_mng.views import is_admin,is_employee,is_manager,is_admin_or_manager
from django.views.generic import UpdateView,DeleteView,TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView,PasswordResetConfirmView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin,PermissionRequiredMixin

# Create your views here.
from django.contrib.auth import get_user_model
User=get_user_model()

def index(request):
    return render(request,'index.html')

# def booking(request):

#     return render(request,'booking.html')

def contact(request):
    return render(request,'contact.html')

def about(request):
    return render(request,'about.html')


@login_required
@user_passes_test(is_admin,login_url='no_permission')
def create_event(request):
    event_form=EventForm()
    if request.method == 'POST':
        event_form = EventForm(request.POST, request.FILES) 
        print("event1")
        if event_form.is_valid():
            print("event2")
            event_form.save()
            print("event2")
            messages.success(request, "Event created successfully!")
            return redirect('all_event') 
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        event_form = EventForm()

    context = {
        "event_form": event_form,
        "form_title": "Create Event",
        "submit_label": "Create",
        
    }

    return render(request, 'create_event.html', context)

"""
@login_required
@user_passes_test(is_admin,login_url='no_permission')
def update_event(request, id):
    event = get_object_or_404(Event, pk=id) 
    if request.method == 'POST':
        event_form = EventForm(request.POST, instance=event)
        if event_form.is_valid():
            event_form.save()
            messages.success(request, "Event updated successfully.")
            return redirect('event')
        messages.error(request, "Please fix the errors below.")
    else:
        event_form = EventForm(instance=event)

    context = {
        "event_form": event_form,
        "form_title": f"Update Event: {event.name}",
        "submit_label": "Update",
        
    }
    return render(request, 'create_event.html', context)

""" 
"""CBV er update event"""

class UpdateEvent(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model=Event
    form_class=EventForm
    template_name="create_event.html"
    context_object_name="event_form"
    pk_url_kwarg='id'
    def test_func(self):
        return is_admin(self.request.user)
    
    def handle_no_permission(self):
        return redirect('no_permission')
    
    def get_success_url(self):
        return reverse_lazy('all_event')
    
    def form_valid(self, form):
        messages.success(self.request, "Event updated successfully.")
        return super().form_valid(form)  
    
    def form_invalid(self, form):
        messages.error(self.request, "Please fix the errors below.")
        return super().form_invalid(form)    
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context["event_form"] = context.get("form")
        context["form_title"]=f"Update_Event:{self.object.name}"
        context["submit_label"]="Update"
        return context
    
# delete event
"""
@login_required
@user_passes_test(is_admin,login_url='no_permission')
def delete_event(request,id):

    if request.method=='POST':
        events=Event.objects.get(id=id)
        events.delete()
        return redirect('all_event')
"""

"""CBV with delete event"""
class Delete_Event_View(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model=Event
    success_url=reverse_lazy("all_event")
    pk_url_kwarg='id'

    def test_func(self):
        return is_admin(self.request.user)
    
    def handle_no_permission(self):
        return redirect('no_permission')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        messages.success(request,"Event deleted Successfully")
        return super().delete(request, *args, **kwargs)
# search event

def event(request):
    user = request.user
    
    query = request.GET.get('q')  
    if query:
        events = Event.objects.filter(name__icontains=query)  
    else:
        events = Event.objects.all()

    context = {
        'events': events,
        'query': query,
    }
    return render(request, 'event.html', context)


def booking(request):
    if request.method == 'POST':
        form = ParticipantForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your booking is successful!")
            return redirect('booking')
        else:
            messages.error(request, "Booking failed: " + str(form.errors))
    else:
        form = ParticipantForm(user=request.user)

    return render(request, 'booking.html', {'participant_form': form})

@login_required
@user_passes_test(is_admin,login_url='no_permission')
def category(request):
    category_form = CategoryForm()
    if request.method == 'POST':
        category_form = CategoryForm(request.POST)
        if category_form.is_valid():
            category = category_form.save()
            return redirect('category')
    context={
        'category_form':category_form
    }
    return render(request,'category.html',context)



def crud_event(request):
    return render(request,'crud_event.html')




def event_list(request):
    events = Event.objects.all()
    return render(request, 'event_list.html', {'events': events})



def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    user = request.user
    is_employee = user.groups.filter(name='Employee').exists()
    if request.method == 'POST':
        
        form = ParticipantForm(request.POST, user=request.user)
        if form.is_valid():
            participant = form.save()
           
            return redirect('booking', participant_id=participant.id)
    else:
        
        form = ParticipantForm(user=request.user)
        form.fields['events'].queryset = Event.objects.filter(id=event.id)  

    return render(request, 'event_detail.html', {'event': event, 'rsvp_form': form ,'is_employee':is_employee})



def no_permission(request):
    return render(request,'admin/no_permission.html')



class EventuserProfileView(TemplateView):
    template_name='event_user_profile.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user=self.request.user
        context["username"] =user.username 
        context["email"]=user.email
        context['name']=user.get_full_name()
        context['user_joinded']=user.date_joined
        context['user_last_login']=user.last_login

        return context
  
class CustomPasswordResetView(PasswordResetView):
    form_class=CustomPasswordResetForm
    template_name='password_reset.html'
    success_url=reverse_lazy('sign_in')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["protocol"] ='https' if self.request.is_secure() else 'http' 
        context['domain']=self.request.get_host()
        return context
    
    def form_valid(self, form):
        messages.success(
            self.request,'please check your confirm mail'
        )
        return super().form_valid(form)

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class=CustomPasswordResetConfirmForm
    template_name='password_reset_confirm.html'
    success_url=reverse_lazy('sign_in')

    def form_valid(self, form):
        messages.success(self.request,'password reset has been successfully')

        return super().form_valid(form)
    

