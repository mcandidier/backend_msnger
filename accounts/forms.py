from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ("name", "email")


    def save(self, request):
        user = super(CustomUserCreationForm, self).save(request)
        user.save()
        return user
    

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ("name", "email")