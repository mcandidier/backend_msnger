from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ("email", "name",)

    def save(self,*args,**kwargs):
        password  = self.clean_password2()
        user = super().save(commit=False)
        if password:
            user.set_password(self.cleaned_data['password2'])
            user.name = self.cleaned_data['name']
            user.save()
        return user


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ("email", "name",)
