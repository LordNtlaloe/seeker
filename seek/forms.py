from django.forms import ModelForm
from .models import Business, Category, Product, Socials, Hours, User
from django.contrib.auth.forms import UserCreationForm



class UserRegisrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'first_name', 
            'last_name',
            'username',
            'bio', 
            'email', 
            'address', 
            'phone_number',
            'profile_picture',
            'password1',
            'password2'
        ]
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field in self.fields:
                self.fields[field].widget.attrs['class'] = 'form-control'

class BusinessForm(ModelForm):
    class Meta:
        model = Business
        fields = "__all__"
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
        exclude = ['business']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'


class SocialsForm(ModelForm):
    class Meta:
        model = Socials
        fields = "__all__"
        exclude = ['business']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'


class HoursForm(ModelForm):
    class Meta:
        model = Hours
        fields = "__all__"
        exclude = ['business']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name', 
            'last_name',
            'bio', 
            'email', 
            'address', 
            'phone_number',
            'profile_picture'
        ]
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for myField in self.fields:
                self.fields[myField].widget.attrs['class'] = 'form-control'
