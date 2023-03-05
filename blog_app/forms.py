from django import forms
from django.core.mail import send_mail
from django.http import BadHeaderError, HttpResponse

from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("name", "email", "content")


# Contact Us
class ContactForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email_address = forms.EmailField(max_length=150)
    message = forms.CharField(widget=forms.Textarea, max_length=2000)

    def send_email(self):
        subject = "Website Inquiry."
        body = {
            "first_name": self.cleaned_data["first_name"],
            "last_name": self.cleaned_data["last_name"],
            "email": self.cleaned_data["email_address"],
            "message": self.cleaned_data["message"],
        }
        message = "\n".join(body.values())
        try:
            send_mail(subject, message, "admin@noreply.com", ["admin@noreply.com"])
        except BadHeaderError:
            return HttpResponse("Invalid header found.")
