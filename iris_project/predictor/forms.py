from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator


class IrisPredictionForm(forms.Form):
    """Form để nhập 4 đặc trưng của hoa Iris."""
    
    sepal_length = forms.FloatField(
        validators=[MinValueValidator(0.1), MaxValueValidator(10.0)],
        widget=forms.NumberInput(attrs={'step': '0.1', 'placeholder': 'VD: 5.1'})
    )
    
    sepal_width = forms.FloatField(
        validators=[MinValueValidator(0.1), MaxValueValidator(6.0)],
        widget=forms.NumberInput(attrs={'step': '0.1', 'placeholder': 'VD: 3.5'})
    )
    
    petal_length = forms.FloatField(
        validators=[MinValueValidator(0.1), MaxValueValidator(8.0)],
        widget=forms.NumberInput(attrs={'step': '0.1', 'placeholder': 'VD: 1.4'})
    )
    
    petal_width = forms.FloatField(
        validators=[MinValueValidator(0.1), MaxValueValidator(3.0)],
        widget=forms.NumberInput(attrs={'step': '0.1', 'placeholder': 'VD: 0.2'})
    )
