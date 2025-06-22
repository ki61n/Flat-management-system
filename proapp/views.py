from django.shortcuts import render, redirect,HttpResponse,get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserProfileForm
from proapp.models import *
from django.contrib.auth import logout 
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from .forms import UserProfileForm,FlatForm,FlatImageForm
import os
from .models import UserProfile
from django.utils import timezone
from .models import Flat, Payment
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.db.models import Q  # Import Q for complex queries
from .models import ProgramRegistration
from .forms import ProgramRegistrationForm

def index(request):
    return render(request, 'index.html')

def properties(request):
    return render(request, 'properties.html')

def property_details(request):
    return render(request, 'property_details.html')

def contact(request):
    return render(request, 'contact.html')



def login_page(request):
    return render(request, 'login.html')


def register(request):
    return render(request,'register.html')
    
        




def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])  # Hash the password
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user  # Link the profile to the user
            profile.save()

            messages.success(request, 'Registration successful.')
            return redirect('login')  # Redirect to login page or wherever you want

        else:
            messages.error(request, 'Please correct the errors below.')

    else:
        user_form = UserRegistrationForm()
        profile_form = UserProfileForm()

    return render(request, 'register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

def success(request):
    return render(request, 'sucess.html')



@login_required
def admin_dashboard(request):
    if request.user.is_superuser:
        return render(request, 'adminpanel/index.html')
   # else:
   #     return redirect('user_dashboard')  # If the user is not an admin, redirect to user dashboard

@login_required
def dashboard(request):
    return render(request, 'userpanel/dashboard.html')




def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Log in the user using the correct `auth_login` function
            auth_login(request, user)

            # Check if the user is a superuser
            if user.is_superuser:
                return redirect('admin_dashboard')
            else:
                return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')



def logout_view(request):
    auth_logout(request)  # Logs out the user
    return redirect('index')  # Redirect to the index page after logout



def user_list(request):
    users = User.objects.all()  # Fetch all users
    return render(request, 'adminpanel/user_list.html', {'users': users})

def admin_home(request):
    return render(request, 'adminpanel/index.html')


# Edit User View
def edit_user(request, id):
    user = get_object_or_404(User, id=id)  # Get the user or return a 404 if not found

    if request.method == 'POST':
        # Handle form submission for editing user
        user_form = UserProfileForm(request.POST, instance=user)
        if user_form.is_valid():
            user_form.save()
            return redirect('user_list')  # Redirect to the users list page after successful edit
    else:
        user_form = UserProfileForm(instance=user)

    return render(request, 'adminpanel/edit_user.html', {'user_form': user_form})

# Delete User View
def delete_user(request, id):
    user = get_object_or_404(User, id=id)  # Get the user or return a 404 if not found

    if request.method == 'POST':
        # If confirmation is given, delete the user
        user.delete()
        return redirect('user_list')  # Redirect to the users list page after successful deletion

    return render(request, 'adminpanel/confirm_delete.html', {'user': user})



def admin_flat(request):
    return render(request, 'adminpanel/admin_flat.html')

#flatt
def add_flat(request):
    # Logic for adding a flat
    return render(request, 'adminpanel/add_flat.html')

def list_flats(request):
    flats = Flat.objects.all()
    return render(request, 'adminpanel/list_flats.html', {'flats': flats})

def manage_flats(request):
    # Logic to manage flats
    flats = Flat.objects.all()
    return render(request, 'adminpanel/manage_flat.html', {'flats': flats})

def sold_flats(request):
    # Logic to display sold flats
  #  sold_flats = Flat.objects.filter(status='sold')
    completed_payments = Payment.objects.filter(buy_status='completed')
    return render(request, 'adminpanel/sold_flat.html', {'payments': completed_payments})
  



def rented_flats(request):
    # Logic to display rented flats
   # rented_flats = Flat.objects.filter(status='rented')
    completed_payments = Payment.objects.filter(rent_status='completed')
    return render(request, 'adminpanel/rented_flat.html', {'payments': completed_payments})
  
   # return render(request, 'adminpanel/rented_flats.html', {'rented_flats': rented_flats})


#  flat registration

def add_flat(request):
    if request.method == 'POST':
        flat_form = FlatForm(request.POST, request.FILES)
        flat_image_form = FlatImageForm(request.POST, request.FILES)

        if flat_form.is_valid() and flat_image_form.is_valid():
            flat = flat_form.save()  # Save the flat data
            
            # Handle the uploaded images
            images = request.FILES.getlist('images')  # Get the list of uploaded images

            for image in images:
                flat_image = FlatImage(flat=flat, image=image)
                flat_image.save()  # Save each image associated with the flat

            return redirect('add_flat')  # Redirect to success page or wherever you want
    else:
        flat_form = FlatForm()
        flat_image_form = FlatImageForm()

    return render(request, 'adminpanel/add_flat.html', {
        'form': flat_form,
        'flat_image_form': flat_image_form
    })

def edit_flat(request, id):
    flat = get_object_or_404(Flat, id=id)  # Fetch the flat instance
    
    if request.method == 'POST':
        form = FlatForm(request.POST, instance=flat)  # Bind form with existing flat data
        if form.is_valid():
            form.save()  # Save the changes
            return redirect('manage_flats')  # Redirect after saving
    else:
        form = FlatForm(instance=flat)  # Create a form with existing flat data

    return render(request, 'adminpanel/edit_flat.html', {'form': form, 'flat': flat})  # Render the template

# View to delete a flat

def delete_flat(request, id):
    flat = get_object_or_404(Flat, id=id)
    flat.delete()
    return redirect('manage_flats')
   # return render(request, 'adminpanel/delete_flat.html', {'flat': flat})


def view_flat(request, flat_id):
    # Retrieve the flat object based on the flat_id
    flat = get_object_or_404(Flat, flat_id=flat_id)
    images = flat.images.all()  # Get all images related to this flat
    
    context = {
        'flat': flat,
        'images': images,
    }
    
    return render(request, 'adminpanel/view_flat.html', context)




#   user
 

@login_required
def my_profile(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    return render(request, 'userpanel/my_profile.html', {'user_profile': user_profile})





@login_required
def profile_view(request):
    # Get the user profile
    user_profile = get_object_or_404(UserProfile, user=request.user)
    
    # Retrieve the user's latest completed payment (either buy or rent is completed)
    payment = Payment.objects.filter(user=request.user).filter(
        Q(buy_status='completed') | Q(rent_status='completed')
    ).order_by('-date').first()
    
    # Get the flat associated with the completed payment, if it exists
    flat = payment.flat if payment else None
    
    context = {
        'user_profile': user_profile,
        'flat': flat,  # Pass the flat to the template
    }
    
    return render(request, 'userpanel/my_profile.html', context)




@login_required
def edit_profile(request):
    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()  # Save the updated profile
            return redirect('my_profile')  # Redirect to the profile page after saving
    else:
        form = UserProfileForm(instance=user_profile)  # Prepopulate the form with current data

    return render(request, 'userpanel/edit_profile.html', {'form': form, 'user_profile': user_profile})



def uview_flat(request, flat_id):
    flat = get_object_or_404(Flat, id=flat_id)
    return render(request, 'user_flat.html', {'flat': flat})


def user_flat_view(request):
   # flats = Flat.objects.prefetch_related('images').all()  # Fetch all Flat objects with related images
    #return render(request, 'userpanel/user_flat_view.html', {'flats': flats})
    flats = Flat.objects.filter(payment_status_flat=1)
    return render(request, 'userpanel/user_flat_view.html', {'flats': flats})


def flat_details(request, flat_id):
    flat = get_object_or_404(Flat, flat_id=flat_id)
    return render(request, 'userpanel/flat_details.html', {'flat': flat})

def rent_flat(request, flat_id):
    flat = get_object_or_404(Flat, flat_id=flat_id)
    return render(request, 'userpanel/rent_flat.html', {'flat': flat})

def buy_flat(request, flat_id):
    flat = get_object_or_404(Flat, flat_id=flat_id)
    return render(request, 'userpanel/buy_flat.html', {'flat': flat})

def rpayment(request, flat_id):
    # Fetch the flat details by ID
    flat = get_object_or_404(Flat, flat_id=flat_id)
    
    # Here, you might integrate a payment processing API, but for simplicity,
    # we'll just render the page with flat details and a "Pay Now" button.
    
    return render(request, 'userpanel/rpayment.html', {'flat': flat})

def bpayment(request, flat_id):
    # Fetch the flat details by ID
    flat = get_object_or_404(Flat, flat_id=flat_id)
    
    # Here, you might integrate a payment processing API, but for simplicity,
    # we'll just render the page with flat details and a "Pay Now" button.
    
    return render(request, 'userpanel/bpayment.html', {'flat': flat})


########################################################################################################################################
def payment_proof(request):
    return render(request, 'userpanel/payment_proof.html')
@login_required
def process_rent_payment(request, flat_id):
    try:
        # Retrieve the flat by its ID
        flat = Flat.objects.get(flat_id=flat_id)
    except Flat.DoesNotExist:
        # If the flat does not exist, raise a 404 error
        raise Http404("No Flat matches the given query.")
    
    # Process rent payment only if the flat exists
    payment = Payment.objects.create(
        user=request.user,
        flat=flat,
        rent_status='completed',  # Rent is confirmed
        buy_status='pending',  # Rent doesn't affect buy status
        date=timezone.now(),
        amount=flat.rent_amount  # Rent amount
    )
    
    # Redirect to a success page (you can change this URL as needed)
    return render(request, 'userpanel/payment_proof.html', {'payment': payment}) # Replace with your success page

@login_required
def process_buy_payment(request, flat_id):
    try:
        # Retrieve the flat by its ID
        flat = Flat.objects.get(flat_id=flat_id)
    except Flat.DoesNotExist:
        # If the flat does not exist, raise a 404 error
        raise Http404("No Flat matches the given query.")
        # Process buy payment
    payment = Payment.objects.create(
        user=request.user,
        flat=flat,
        rent_status='pending',  # Rent doesn't apply here
        buy_status='completed',  # Buy is confirmed
        date=timezone.now(),
        amount=flat.buy_amount  # Buy amount
    )
        
        # Redirect to success page or user dashboard
    return render(request, 'userpanel/payment_proof.html', {'payment': payment}) # Replace with your success page



def programs(request):
    return render(request,'adminpanel/admin_program.html') 



def add_program(request):
    return render(request,'adminpanel/add_program.html') 

def approve_program(request):
    return render(request,'adminpanel/approve_program.html')

def approved_programs(request):
    return render(request,'adminpanel/approved_programs.html')
def program_fees(request):
    return render(request,'adminpanel/program_fees.html')

def program_amount(request):
    return render(request,'program_fees.html') 

def program_fees(request):
    if request.method == 'POST':
        form = ProgramRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('program_fees')  # Redirect to the same page or another page if desired
    else:
        form = ProgramRegistrationForm()

    # Pass the form instance to the template
    return render(request, 'program_fees.html', {'form': form})