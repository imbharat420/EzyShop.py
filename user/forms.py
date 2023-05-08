from django import forms
from user.models import User,UserProfile
# from django.contrib.auth.models import User
class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter Password',
        'class': 'form-control',
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password'
    }))

    class Meta:
        model = User
        fields = ['name','username', 'email','phone', 'username', 'password']
    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        if User.objects.filter(username=cleaned_data["username"]).exists():
            raise forms.ValidationError("The username is taken, please try another one")
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "Password does not match!"
            )
            
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Enter Username'
        self.fields['name'].widget.attrs['placeholder'] = 'Enter name'
        self.fields['phone'].widget.attrs['placeholder'] = 'Enter Phone Number'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email Address'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            

class UserForm(forms.ModelForm): 
    class Meta:
        model = User
        fields = ('name','email', 'phone')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Enter name'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter email'
        self.fields['phone'].widget.attrs['placeholder'] = 'Enter phone'
        
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class UserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False, error_messages = {'invalid':("Image files only")}, widget=forms.FileInput)
    class Meta:
        model = UserProfile
        fields = ('address_line_1', 'address_line_2', 'city', 'state', 'country', 'profile_picture')

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['address_line_1'].widget.attrs['placeholder'] = 'Enter address_line_1'
        self.fields['address_line_2'].widget.attrs['placeholder'] = 'Enter address_line_2'
        self.fields['city'].widget.attrs['placeholder'] = 'Enter city'
        self.fields['state'].widget.attrs['placeholder'] = 'Enter state'
        self.fields['country'].widget.attrs['placeholder'] = 'Enter country'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'