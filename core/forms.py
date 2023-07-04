from django import forms
from .models import Item

INPUT_CLASSES = 'form-control'

class DateTimeInput(forms.DateTimeInput):
    def __init__(self, attrs=None):
        attrs = attrs or {}
        attrs['type'] = 'datetime-local'
        super().__init__(attrs)
        self.use_required = False  

class NewItemForm(forms.ModelForm):
    
    auction_end_datetime = forms.DateTimeField(widget=DateTimeInput)
    class Meta:
        model = Item
        fields = ('name', 'description', 'min_bid_price', 'image','auction_end_datetime')
        widgets = {
            
            'name': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'description': forms.Textarea(attrs={
                'class': INPUT_CLASSES
            }),
            'min_bid_price': forms.NumberInput(attrs={
                'class': INPUT_CLASSES
            }),
            'image': forms.FileInput(attrs={
                'class': INPUT_CLASSES
            })
        }