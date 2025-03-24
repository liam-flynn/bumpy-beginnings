from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserForm, SiteUserForm, UpdateUserForm, PasswordUpdateForm
from .models import SiteUser
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)

        if user_form.is_valid():
            # check to make sure the username isn't already in use
            username = user_form.cleaned_data['username']
            if User.objects.filter(username=username).exists():
                user_form.add_error('username', 'A user with that username already exists.')
            else:
                try:
                    # save the new user
                    user = user_form.save(commit=False)
                    user.set_password(user.password)
                    user.save()
                    registered = True
                    messages.success(request, "Registration successful! Please log in.")
                    return redirect('login') 
                except ValidationError as e:
                    user_form.add_error(None, str(e))
        else:
            print(f"Validation errors: {user_form.errors}")
    else:
        user_form = UserForm()

    return render(request, 'register.html', {
        'user_form': user_form,
        'registered': registered,
    })


@login_required(login_url='/login')
def get_details(request):
    user = request.user
    # Redirect authenticated users with SiteUser data back to the homepage
    if SiteUser.objects.filter(user=user).exists() or user.is_staff:
        return redirect('homepage')

    # If not yet created a SiteUser profile, link them to the form
    if request.method == 'POST':
        details_form = SiteUserForm(data=request.POST)
        if details_form.is_valid():
            siteUser = details_form.save(commit=False)
            siteUser.user = user
            siteUser.save()
            # Redirect to the homepage after saving
            return redirect('homepage') 
    else:
        details_form = SiteUserForm()

    context = {'details_form': details_form}
    return render(request, 'provideDetails.html', context)



def homepage(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'homepage.html')

# help from https://docs.djangoproject.com/en/5.1/topics/auth/default/
def user_login(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]

        if not username or not password:
            if not username:
                messages.error(request, "Username is required.")
            if not password:
                messages.error(request, "Password is required.")
            return render(request, 'login.html')
        
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('get_details')
        else:
            messages.error(request, "Invalid login. Please try again.")
            return render(request, 'login.html')     
    else:
        return render(request, 'login.html')



def user_logout(request):
    logout(request)
    return redirect('homepage')


@user_passes_test(lambda user: user.is_staff, login_url='/login/')
def manage_mod_privileges(request):
    # get the search query from GET or POST.
    query = request.GET.get('q') or request.POST.get('q', '')
    users = User.objects.filter(
        Q(username__icontains=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query)
    ).order_by('username')

    # add pagination.
    paginator = Paginator(users, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        action = request.POST.get('action')
        try:
            user = User.objects.get(pk=user_id)
            site_user, created = SiteUser.objects.get_or_create(user=user)
            # "grant" sets "isForumMod" to True
            if action == 'grant':
                site_user.isForumMod = True
                site_user.save()
                messages.success(request, f"{user.username} has been granted moderator privileges.")
            # "remove" sets "isForumMod" to False
            elif action == 'remove':
                site_user.isForumMod = False
                site_user.save()
                messages.success(request, f"Moderator privileges removed for {user.username}.")
        except User.DoesNotExist:
            messages.error(request, "User does not exist.")
        
        return render(request, 'manage_mod_privileges.html', {'page_obj': page_obj, 'query': query})

    return render(request, 'manage_mod_privileges.html', {'page_obj': page_obj, 'query': query})


@user_passes_test(lambda user: user.is_staff, login_url='/login/')
def cms_dashboard(request):
    return render(request, 'cms.html')

@login_required
def profile_update(request):
    user = request.user
    site_user = get_object_or_404(SiteUser, user=user)

    if request.method == "POST":
        user_form = UpdateUserForm(request.POST, instance=user)
        site_user_form = SiteUserForm(request.POST, instance=site_user)
        password_form = PasswordUpdateForm(request.POST)

        if user_form.is_valid() and site_user_form.is_valid() and password_form.is_valid():
            # update user and profile details.
            user_form.save()
            site_user_form.save()
            
            # Uudate the password only if provided.
            new_password = password_form.cleaned_data.get("password")
            if new_password:
                user.set_password(new_password)
                user.save()
                # update the session hash so the user remains logged in.
                update_session_auth_hash(request, user)
            
            messages.success(request, "Your profile has been updated successfully!")
            return redirect('homepage')
    else:
        user_form = UpdateUserForm(instance=user)
        site_user_form = SiteUserForm(instance=site_user)
        password_form = PasswordUpdateForm()

    context = {
        'user_form': user_form,
        'site_user_form': site_user_form,
        'password_form': password_form,
    }
    return render(request, "profile_update.html", context)