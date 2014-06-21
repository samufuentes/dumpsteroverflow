from django import forms
from dumpsteroverflow.do_core.models import Dumpster

class OverflowForm(forms.Form):
    is_brown = forms.BooleanField(required=False)
    is_yellow = forms.BooleanField(required=False)
    is_blue = forms.BooleanField(required=False)
    is_gray = forms.BooleanField(required=False)

    street_address = forms.CharField(max_length=200)
    zip_code = forms.IntegerField()
    city = forms.CharField(max_length=50)