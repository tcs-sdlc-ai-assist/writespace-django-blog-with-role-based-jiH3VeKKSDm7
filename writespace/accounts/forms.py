from django import forms
from django.contrib.auth.models import User


input_class = (
    'w-full px-4 py-2 border border-gray-300 rounded-lg '
    'focus:outline-none focus:ring-2 focus:ring-blue-500 '
    'focus:border-transparent'
)


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={
                'class': input_class,
                'placeholder': 'Enter your username',
            }
        ),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': input_class,
                'placeholder': 'Enter your password',
            }
        ),
    )

    def clean_username(self):
        username = self.cleaned_data.get('username', '').strip()
        if not username:
            raise forms.ValidationError('Username is required.')
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password', '').strip()
        if not password:
            raise forms.ValidationError('Password is required.')
        return password


class RegisterForm(forms.Form):
    display_name = forms.CharField(
        max_length=50,
        min_length=2,
        widget=forms.TextInput(
            attrs={
                'class': input_class,
                'placeholder': 'Enter your display name',
            }
        ),
    )
    username = forms.CharField(
        max_length=30,
        min_length=3,
        widget=forms.TextInput(
            attrs={
                'class': input_class,
                'placeholder': 'Choose a username',
            }
        ),
    )
    password1 = forms.CharField(
        min_length=8,
        widget=forms.PasswordInput(
            attrs={
                'class': input_class,
                'placeholder': 'Enter your password',
            }
        ),
        label='Password',
    )
    password2 = forms.CharField(
        min_length=8,
        widget=forms.PasswordInput(
            attrs={
                'class': input_class,
                'placeholder': 'Confirm your password',
            }
        ),
        label='Confirm Password',
    )

    def clean_display_name(self):
        display_name = self.cleaned_data.get('display_name', '').strip()
        if not display_name:
            raise forms.ValidationError('Display name is required.')
        if len(display_name) < 2:
            raise forms.ValidationError('Display name must be at least 2 characters.')
        if len(display_name) > 50:
            raise forms.ValidationError('Display name must be at most 50 characters.')
        return display_name

    def clean_username(self):
        username = self.cleaned_data.get('username', '').strip()
        if not username:
            raise forms.ValidationError('Username is required.')
        if len(username) < 3:
            raise forms.ValidationError('Username must be at least 3 characters.')
        if len(username) > 30:
            raise forms.ValidationError('Username must be at most 30 characters.')
        if not username.isalnum():
            raise forms.ValidationError('Username must contain only letters and numbers.')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('This username is already taken.')
        return username

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            self.add_error('password2', 'Passwords do not match.')
        return cleaned_data


ROLE_CHOICES = [
    ('user', 'User'),
    ('admin', 'Admin'),
]


class CreateUserForm(forms.Form):
    display_name = forms.CharField(
        max_length=50,
        min_length=2,
        widget=forms.TextInput(
            attrs={
                'class': input_class,
                'placeholder': 'Enter display name',
            }
        ),
    )
    username = forms.CharField(
        max_length=30,
        min_length=3,
        widget=forms.TextInput(
            attrs={
                'class': input_class,
                'placeholder': 'Choose a username',
            }
        ),
    )
    password = forms.CharField(
        min_length=8,
        widget=forms.PasswordInput(
            attrs={
                'class': input_class,
                'placeholder': 'Enter password',
            }
        ),
    )
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.Select(
            attrs={
                'class': input_class,
            }
        ),
    )

    def clean_display_name(self):
        display_name = self.cleaned_data.get('display_name', '').strip()
        if not display_name:
            raise forms.ValidationError('Display name is required.')
        if len(display_name) < 2:
            raise forms.ValidationError('Display name must be at least 2 characters.')
        if len(display_name) > 50:
            raise forms.ValidationError('Display name must be at most 50 characters.')
        return display_name

    def clean_username(self):
        username = self.cleaned_data.get('username', '').strip()
        if not username:
            raise forms.ValidationError('Username is required.')
        if len(username) < 3:
            raise forms.ValidationError('Username must be at least 3 characters.')
        if len(username) > 30:
            raise forms.ValidationError('Username must be at most 30 characters.')
        if not username.isalnum():
            raise forms.ValidationError('Username must contain only letters and numbers.')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('This username is already taken.')
        return username