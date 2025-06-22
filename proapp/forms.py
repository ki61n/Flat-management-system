from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import UserProfile 
from .models import Flat, FlatImage,ProgramRegistration


class UserRegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Confirm Password')

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password:
            if password != confirm_password:
                raise ValidationError("Passwords do not match.")

        # Add additional password validation rules here (e.g., length, complexity)
        if password and len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        
        return cleaned_data

    # Ensure email is unique
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with that email already exists.")
        return email

    # Ensure username is unique
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("A user with that username already exists.")
        return username

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name','address', 'phone', 'id_proof', 'profile_picture']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'id_proof': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

    # Validate phone number format (example: must be digits and 10 characters long)
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone.isdigit():
            raise ValidationError("Phone number must contain only digits.")
        if len(phone) != 10:
            raise ValidationError("Phone number must be 10 digits long.")
        return phone


     # Validation for address
    def clean_address(self):
        address = self.cleaned_data.get('address')
        if not address or len(address) < 10:
            raise ValidationError("Address must be at least 10 characters long.")
        return address

    # Validation for id_proof
    def clean_id_proof(self):
        id_proof = self.cleaned_data.get('id_proof')
        if not id_proof:
            raise ValidationError("Please upload a valid ID proof.")
        # Optional: Add file size or type validation if needed
        if id_proof.size > 10 * 1024 * 1024:  # Example: Max size 2MB
            raise ValidationError("ID proof file size should not exceed 2MB.")
        return id_proof

    # Validation for profile_picture
    def clean_profile_picture(self):
        profile_picture = self.cleaned_data.get('profile_picture')
        if not profile_picture:
            raise ValidationError("Please upload a profile picture.")
        # Optional: Add file size or type validation if needed
        if profile_picture.size > 10 * 1024 * 1024:  # Example: Max size 2MB
            raise ValidationError("Profile picture file size should not exceed 2MB.")
        return profile_picture




#   form for flat registration : admin



class FlatForm(forms.ModelForm):
    class Meta:
        model = Flat
        fields = ['flat_id', 'flat_number', 'hall', 'bedroom', 'bathroom', 'kitchen','type_of_flat', 'description','rent_amount','buy_amount']
        widgets = {
            'flat_id': forms.TextInput(attrs={'class': 'form-control'}),
            'flat_number': forms.TextInput(attrs={'class': 'form-control'}),
            'hall': forms.NumberInput(attrs={'class': 'form-control'}),
            'bedroom': forms.NumberInput(attrs={'class': 'form-control'}),
            'bathroom': forms.NumberInput(attrs={'class': 'form-control'}),
            'kitchen': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'flat_id': 'Flat ID',
            'flat_number': 'Flat Number',
            'hall': 'Hall',
            'bedroom': 'Bedroom',
            'bathroom': 'Bathroom',
            'kitchen': 'Kitchen',
        }


class FlatImageForm(forms.Form):
    images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)
    labels = {
                'flat_id': 'Flat ID',
    } 


class ProgramRegistrationForm(forms.ModelForm):
    class Meta:
        model = ProgramRegistration
        fields = ['program_reg_fee']
        widgets = {
            'program_reg_fee': forms.TextInput(attrs={'class': 'form-control'}),
        }