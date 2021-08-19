from django import forms

from .models import Users

class TransferForm(forms.Form):
    user_from  = forms.ModelChoiceField(queryset=Users.objects.all(), empty_label='От кого')
    inn_to      = forms.IntegerField(label='Кому') # замечания такие же как и к сериализатору
    amount      = forms.FloatField() # нужно DECIMAL!!!!
