from django import forms
from.models import Category,Event,Participant



class CategoryForm(forms.ModelForm):
    class Meta:
        model=Category
        fields=['name','description']
        widgets={
            'name':forms.TextInput(attrs={'placeholder':'Enter your name..'}),
            'description': forms.Textarea(attrs={'placeholder': 'Enter category description'}),
        }
        
from django import forms
from .models import Category, Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name','description','date','time','location','category']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter event name'}),
            'description': forms.Textarea(attrs={'placeholder': 'Enter event details'}),
            'date': forms.DateInput(attrs={"type": 'date'}),
            'time': forms.TimeInput(attrs={"type": 'time'}),
            'location': forms.TextInput(attrs={'placeholder': 'Enter location'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
        }

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
       
        self.fields['category'].queryset = Category.objects.all()

class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['name', 'email', 'events']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter participant name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter email address'}),
            'events': forms.CheckboxSelectMultiple( ) 
  # Multiple events checkbox
        }
        

























# from django import forms
# from .models import Category, Event, Participant

# class CategoryForm(forms.ModelForm):
#     class Meta:
#         model = Category
#         fields = ['name', 'description']
#         widgets = {
#             'name': forms.TextInput(attrs={'placeholder': 'Enter your name..'}),
#             'description': forms.Textarea(attrs={'placeholder': 'Enter category description'}),
#         }

# class EventForm(forms.ModelForm):
#     class Meta:
#         model = Event
#         fields = ['name', 'description', 'date', 'time', 'location', 'category']
#         widgets = {
#             'name': forms.TextInput(attrs={'placeholder': 'Enter event name'}),
#             'description': forms.Textarea(attrs={'placeholder': 'Enter event details'}),
#             'date': forms.DateInput(attrs={"type": 'date'}),
#             'time': forms.TimeInput(attrs={"type": 'time'}),
#             'location': forms.TextInput(attrs={'placeholder': 'Enter location'}), 
#             'category': forms.Select(attrs={'class': 'form-select'}),     
#         }

#     # Correct indentation for __init__
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # ForeignKey dropdown choices
#         self.fields['category'].queryset = Category.objects.all()

# class ParticipantForm(forms.ModelForm):
#     class Meta:
#         model = Participant
#         fields = ['name', 'email', 'events']
#         widgets = {
#             'name': forms.TextInput(attrs={'placeholder': 'Enter participant name'}),
#             'email': forms.EmailInput(attrs={'placeholder': 'Enter email address'}),
#             'events': forms.CheckboxSelectMultiple(),  # Multiple events checkbox
#         }

#     # Correct indentation for __init__
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # Assign queryset for events field
#         self.fields['events'].queryset = Event.objects.all()
