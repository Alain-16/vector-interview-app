from django import forms
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()

class LoginForm(forms.Form):
    # Using username for authentication (default behavior).
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'input100', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input100', 'placeholder': 'Password'}))

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("Invalid login credentials")
            cleaned_data['user'] = user
        return cleaned_data


class SignUpForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'input100', 'placeholder': 'Password'}),
        label="Password"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'input100', 'placeholder': 'Confirm Password'}),
        label="Confirm Password"
    )

    class Meta:
        model = User
        fields = ('username', 'email')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'input100', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'input100', 'placeholder': 'Email'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
