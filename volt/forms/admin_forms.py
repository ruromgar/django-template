from django import forms


class GenerateInviteCodesForm(forms.Form):
    source_event = forms.CharField(label="Source Event", required=False, max_length=500)
    num_codes = forms.IntegerField(label="Number of Codes", min_value=1)
    expires_at = forms.DateTimeField(label="Expiration Date", required=False, widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
