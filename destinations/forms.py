from django import forms
from destinations.models import Destination, Photo


class DestinationForm(forms.ModelForm):
    class Meta:
        model = Destination
        fields = "__all__"
        exclude = ['host']


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['file', 'caption']


PhotoFormSet = forms.inlineformset_factory(
    Destination, Photo, form=PhotoForm, extra=5, can_delete=False
)


class DestinationSearchForm(forms.Form):
    city = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'City'}))
    # check_in = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    # check_out = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    guests = forms.ChoiceField(required=False, choices=[(i, i) for i in range(1, 16)] + [('15+', '15+')])
