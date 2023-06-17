from django import forms

class VoiceForm(forms.Form):
    voice_sample = forms.FileField()