from django.forms import ModelForm
from .models import RequestTypes

class RequestTypesForm(ModelForm):
    class Meta:
        model = RequestTypes
        fields = '__all__'