from django import forms
from products. models import *

class AddProducts(forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'

