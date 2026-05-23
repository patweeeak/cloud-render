from django import forms
from .models import RecipePhoto

class RecipePhotoForm(forms.ModelForm):
    class Meta:
        model = RecipePhoto
        fields = ['title', 'description', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'E.g., Spicy Tacos'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }