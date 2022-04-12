from allauth.account.forms import SignupForm, LoginForm, ResetPasswordForm, ResetPasswordKeyForm, ChangePasswordForm, AddEmailForm
from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django import forms

from .models import KYCVerify

User = get_user_model()


class UserAdminChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User


class UserAdminCreationForm(admin_forms.UserCreationForm):
    """
    Form for User Creation in the Admin Area.
    To change user signup, see UserSignupForm and UserSocialSignupForm.
    """

    class Meta(admin_forms.UserCreationForm.Meta):
        model = User

        error_messages = {
            "username": {"unique": _("This username has already been taken.")}
        }


class UserLoginForm(LoginForm):

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['email'].label = ""
        self.fields['password'].label = ""
        self.fields['login'].widget = forms.TextInput(
            attrs={'type': 'email', 'class': 'textinput textInput form-control fbc-has-badge fbc-UID_1 appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-dark rounded-t-md focus:outline-none focus:ring-primary focus:border-primary focus:z-10 sm:text-xl'})
        self.fields['password'].widget = forms.PasswordInput(
            attrs={'class': 'textinput textInput form-control fbc-has-badge fbc-UID_1 appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-dark rounded-b-md focus:outline-none focus:ring-primary focus:border-primary focus:z-10 sm:text-xl'})


class UserSignupForm(SignupForm):
    """
    Form that will be rendered on a user sign up section/screen.
    Default fields will be added automatically.
    Check UserSocialSignupForm for accounts created from social.
    """

    name = forms.CharField(max_length=255, label='', widget=forms.TextInput(attrs={'title': 'Your Name', 'placeholder': 'Firstname Lastname',
                           "class": "textinput textInput form-control fbc-has-badge fbc-UID_1 appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-dark focus:outline-none focus:ring-primary focus:border-primary focus:z-10 sm:text-xl"}))
    # password = forms.CharField(max_length=255, label='', widget=forms.TextInput(attrs={'title': 'Password', 'placeholder':'Password', "class":"textinput textInput form-control fbc-has-badge fbc-UID_1 appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-dark focus:outline-none focus:ring-primary focus:border-primary focus:z-10 sm:text-xl"}))
    # password2 = forms.CharField(max_length=255, label='', widget=forms.TextInput(attrs={'title': 'Confirm Password', 'placeholder':'Confirm Password', "class":"textinput textInput form-control fbc-has-badge fbc-UID_1 appearance-none rounded-b-xl relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-dark focus:outline-none focus:ring-primary focus:border-primary focus:z-10 sm:text-xl"}))

    def __init__(self, *args, **kwargs):
        super(UserSignupForm, self).__init__(*args, **kwargs)
        self.fields['email'].label = ""
        self.fields['password1'].label = ""
        self.fields['password2'].label = ""
        self.fields['username'].label = ""
        self.fields['email'].widget = forms.EmailInput(
            attrs={'placeholder': 'Your Email', "hx-post":"/accounts/signup/check-email/", "hx-target":"#email-err", "hx-trigger":"keyup", 'class': 'textinput textInput form-control fbc-has-badge fbc-UID_1 appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-dark rounded-t-md focus:outline-none focus:ring-primary focus:border-primary focus:z-10 sm:text-xl'})
        self.fields['password1'].widget = forms.PasswordInput(
            attrs={'placeholder': 'Password', 'class': 'form-control fbc-has-badge fbc-UID_1 appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-dark focus:outline-none focus:ring-primary focus:border-primary focus:z-10 sm:text-xl'})
        self.fields['password2'].widget = forms.PasswordInput(
            attrs={'placeholder': 'Confirm Password', 'class': 'textinput textInput form-control fbc-has-badge fbc-UID_1 appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-dark rounded-b-md focus:outline-none focus:ring-primary focus:border-primary focus:z-10 sm:text-xl'})
        self.fields['username'].widget = forms.TextInput(
            attrs={'placeholder': 'Your Username', 'class': 'form-control fbc-has-badge fbc-UID_1 appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-dark focus:outline-none focus:ring-primary focus:border-primary focus:z-10 sm:text-xl', "hx-post":"/accounts/signup/check-username/", "hx-target":"#username-err", "hx-trigger":"keyup"})

    def save(self, request):
        user = super(UserSignupForm, self).save(request)
        user.name = self.cleaned_data['name']
        user.save()
        return user


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = [
            'name',
            'phone',
            'wallet_address',
            'eth_address',
            'ltc_address',
            'dash_address',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = ""
        self.fields['phone'].label = ""
        self.fields['wallet_address'].label = ""
        self.fields['eth_address'].label = ""
        self.fields['ltc_address'].label = ""
        self.fields['dash_address'].label = ""
        self.fields['name'].widget = forms.TextInput(
            attrs={'placeholder': 'User Name', 'class': 'imageinput textInput w-full text-dark placeholder:text-dark rounded-md font-bold text-sm border-primary outline-1 outline-primary bg-slate-400'})
        self.fields['phone'].widget = forms.TextInput(
            attrs={'placeholder': 'User Phone', 'class': 'imageinput textInput w-full text-dark placeholder:text-dark rounded-md font-bold text-sm border-primary outline-1 outline-primary bg-slate-400'})
        self.fields['wallet_address'].widget = forms.TextInput(
            attrs={'placeholder': 'BTC Wallet Address', 'class': 'w-full text-dark placeholder:text-dark rounded-md font-bold text-sm border-primary outline-1 outline-primary bg-slate-400'})
        self.fields['eth_address'].widget = forms.TextInput(
            attrs={'placeholder': 'ETH Wallet Address', 'class': 'w-full text-dark placeholder:text-dark rounded-md font-bold text-sm border-primary outline-1 outline-primary bg-slate-400'})
        self.fields['ltc_address'].widget = forms.TextInput(
            attrs={'placeholder': 'LTC Wallet Address', 'class': 'w-full text-dark placeholder:text-dark rounded-md font-bold text-sm border-primary outline-1 outline-primary bg-slate-400'})
        self.fields['dash_address'].widget = forms.TextInput(
            attrs={'placeholder': 'DASH Wallet Address', 'class': 'w-full text-dark placeholder:text-dark rounded-md font-bold text-sm border-primary outline-1 outline-primary bg-slate-400'})


class KYCForm(forms.ModelForm):

    class Meta:
        model = KYCVerify
        fields = [
            # 'id_type',
            'pass_front', 'pass_back'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pass_front'].label = "ID Front"
        self.fields['pass_back'].label = "ID Back"
        # self.fields['id_type'].label = "ID Type"
        self.fields['pass_front'].widget = forms.ClearableFileInput(
            attrs={'placeholder': 'International Passport Front', 'class': 'imageinput textInput w-full text-dark placeholder:text-dark rounded-md font-bold text-sm border-primary outline-1 outline-primary bg-slate-400'})
        self.fields['pass_back'].widget = forms.ClearableFileInput(
            attrs={'placeholder': 'International Passport Back', 'class': 'w-full text-dark placeholder:text-dark rounded-md font-bold text-sm border-primary outline-1 outline-primary bg-slate-400'})
        # self.fields['id_type'].widget = forms.Select(
        #     attrs={'placeholder': 'ID Type', 'class': 'w-full md:w-min text-dark placeholder:text-dark rounded-md font-bold text-sm border-primary outline-1 outline-primary bg-slate-400'})
        # w-full md:w-min text-dark placeholder:text-dark rounded-md font-bold text-sm border-primary outline-1 outline-primary bg-slate-400

class ResetUserPassword(ResetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(ResetUserPassword, self).__init__(*args, **kwargs)
        self.fields['email'].label = ""
        self.fields['email'].widget = forms.EmailInput(
            attrs={'placeholder':'Email Address', 'class': 'textinput textInput form-control fbc-has-badge fbc-UID_1 appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-dark rounded-md focus:outline-none focus:ring-primary focus:border-primary focus:z-10 sm:text-xl'})


class UserSocialSignupForm(SocialSignupForm):
    """
    Renders the form when user has signed up using social accounts.
    Default fields will be added automatically.
    See UserSignupForm otherwise.
    """
