from django import forms
from.models import Category,Event,Participant
from django.core.mail import send_mail
from django.conf import settings
"""starting to the Mixing apply style to form field"""
class StyleForMixin:
    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.apply_styled_widgets()
    default_classes = "border-2 border-gray-300 w-full p-3 rounded-lg shadow-sm focus:outline-none focus:border-rose-500 focus:ring-rose-500"

    def apply_styled_widgets(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({
                    'class': self.default_classes,
                    'placeholder': f"Enter {field.label.lower()}"
                })
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class': f"{self.default_classes} resize-none",
                    'placeholder':  f"Enter {field.label.lower()}",
                    'rows': 5
                })
            elif isinstance(field.widget, forms.SelectDateWidget):
                print("Inside Date")
                field.widget.attrs.update({
                    "class": "border-2 border-gray-300 p-3 rounded-lg shadow-sm focus:outline-none focus:border-rose-500 focus:ring-rose-500"
                })
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                print("Inside checkbox")
                field.widget.attrs.update({
                    'class': "space-y-2"
                })
            else:
                print("Inside else")
                field.widget.attrs.update({
                    'class': self.default_classes
                })





class CategoryForm(forms.ModelForm):
    class Meta:
        model=Category
        fields=['name','description']
        widgets={
            'name':forms.TextInput(attrs={'placeholder':'Enter your name..'}),
            'description': forms.Textarea(attrs={'placeholder': 'Enter category description'}),
        }
        


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name','description','date','time','location','category','event_image']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter event name'}),
            'description': forms.Textarea(attrs={'placeholder': 'Enter event details'}),
            'date': forms.DateInput(attrs={"type": 'date'}),
            'time': forms.TimeInput(attrs={"type": 'time'}),
            'location': forms.TextInput(attrs={'placeholder': 'Enter location'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'event_image': forms.ClearableFileInput(attrs={'class': 'form-input'}),
        }

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
       
        self.fields ['category'].queryset = Category.objects.all()
class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['name', 'email', 'events']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter participant name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter email address'}),
            'events': forms.CheckboxSelectMultiple()
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  
        super().__init__(*args, **kwargs)
        self.fields['events'].queryset = Event.objects.all()

    def clean_events(self):
        selected_events = self.cleaned_data.get('events')
        
        
        if self.user and Participant.objects.filter(user=self.user).exists():
            raise forms.ValidationError("You have already booked an event. You cannot book again.")

        
        for event in selected_events:
            if event.participants.exists():
                raise forms.ValidationError(f"'{event.name}' has already been booked by another user.")

        return selected_events

    def save(self, commit=True):
        participant = super().save(commit=False)
        if self.user:
            participant.user = self.user  
            participant.save()
            self.save_m2m()  
            #
            for event in participant.events.all():
                send_mail(
                    subject=f'RSVP Confirmation for {event.name}',
                    message=f'Hi {participant.name},\n\nYou have successfully booked "{event.name}".',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[participant.email],
                    fail_silently=False  
                )
        return participant
