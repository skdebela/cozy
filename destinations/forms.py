from django import forms
from destinations.models import Destination, Photo


class DestinationSearchForm(forms.Form):
    city = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'City'}))
    check_in = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    check_out = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    guests = forms.ChoiceField(required=False, choices=[(i, i) for i in range(1, 16)] + [('15+', '15+')])


class DestinationForm(forms.ModelForm):
    # Field for destination photos
    photos = forms.FileField(label='Upload Destination Photos',
                             widget=forms.TextInput(attrs={
                                 "name": "images",
                                 "type": "File",
                                 "class": "form-control",
                                 "multiple": "True",
                             }),
                             required=False)

    class Meta:
        model = Destination
        fields = "__all__"
        exclude = ['created_at', 'updated_at', 'host']

    def save(self, commit=True):
        # Save the destination instance
        destination = super().save(commit=False)
        if commit:
            destination.save()

        # Handle photos upload
        if self.cleaned_data.get('photos'):
            for photo in self.cleaned_data['photos']:
                Photo.objects.create(destination=destination, file=photo, caption=photo.name)
        return destination
