from django import forms



class UrlForm(forms.Form):
    url = forms.CharField(label='URL', max_length=200)

    FORMAT_CHOICES = (
        ('mp3', 'mp3'),
        ('mp4', 'mp4')
    )
    format_choice = forms.ChoiceField(choices=FORMAT_CHOICES)