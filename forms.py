from django import forms
from simple_menus.models import Menu

class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
