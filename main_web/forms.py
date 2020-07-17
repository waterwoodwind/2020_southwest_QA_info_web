from django import forms
from dal import autocomplete

from main_web.models import qa_info

class qa_infoForm(forms.ModelForm):
    class Media:
        def __init__(self):
            pass

        js = (
            'admin/js/vendor/jquery/jquery.min.js',
        )
    class Meta:
        model = qa_info
        fields = ('__all__')
        widgets = {
            'location': autocomplete.ModelSelect2(url='location-autocomplete'),
        }