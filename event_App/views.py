from django.shortcuts import render,get_object_or_404
from django.contrib import messages
from django.shortcuts import redirect
from event_App.models import Category,Participant,Event
from event_App. forms import ParticipantForm,CategoryForm,EventForm




# Create your views here.

def index(request):
    return render(request,'index.html')

# def booking(request):

#     return render(request,'booking.html')

def contact(request):
    return render(request,'contact.html')

def about(request):
    return render(request,'about.html')

def create_event(request):
    event_form = EventForm()
    if request.method == 'POST':
        event_form = EventForm(request.POST)
        if event_form.is_valid():
            event_form.save()

        return redirect('create_event')
    context={"event_form":event_form}



    return render(request,'create_event.html',context)
# update/edit event

# def update_event(request,id):
#     event=Event.objects.get(id=id)
#     event_form = EventForm(instance=event)
#     if request.method == 'POST':
#         event_form = EventForm(request.POST,instance=event)
#         if event_form.is_valid():
#             event_form.save()

#         return redirect('event')
#     context={"event_form":event_form}

#     context = {
#         "event_form": event_form
#     }

#     return render(request, 'create_event.html', context)


def update_event(request, id):
    event = get_object_or_404(Event, id=id)

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
    

# delete event
def delete_event(request,id):
    if request.method=='POST':
        events=Event.objects.get(id=id)
        events.delete()
        return redirect('event')


# search event
def event(request):
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




# def event(request):
#     events=Event.objects.all()
#     context={
#        'events':events,
#     }
#     return render(request,'event.html',context)
 

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ParticipantForm

def booking(request):
    participant_form = ParticipantForm()

    if request.method == 'POST':
        participant_form = ParticipantForm(request.POST)
        if participant_form.is_valid():
            participant_form.save()  # Automatically saves selected events
            messages.success(request, "Your Booking Successfully")
            return redirect('booking')

    return render(request, 'booking.html', {
        'participant_form': participant_form,
    })


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