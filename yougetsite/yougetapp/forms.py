from django import forms

from .utilities.check_yturl import check_yturl

class UrlForm(forms.Form):
    url = forms.CharField(label='URL', max_length=200)

    FORMAT_CHOICES = (
        ('mp3', 'mp3'),
        ('mp4', 'mp4')
    )
    format_choice = forms.ChoiceField(choices=FORMAT_CHOICES)

    def clean(self):
        cleaned_data = super().clean()
        cleaned_url = cleaned_data.get('url')

        checked_yturl = check_yturl(cleaned_url)

        if checked_yturl:
            return
        else:
            self.add_error('url', 'Please enter a valid Youtube URL which starts with https://')