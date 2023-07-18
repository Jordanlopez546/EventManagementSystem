from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from .models import *
from django.db.models import Q
# Create your views here.


@login_required(login_url='login')
def index(request):

    try:

        events = Event.objects.all()

        search_query = request.GET.get('search', '')

        if search_query:
            events = events.filter(
                Q(event_name__icontains=search_query) |
                Q(event_guest_speakers__icontains=search_query) |
                Q(event_time__icontains=search_query) |
                Q(event_agenda__icontains=search_query) |
                Q(event_location__icontains=search_query)
            )

        event_present = len(events) > 0

        context =  {
            'events':events,
            'event_present':event_present,
            'search_query':search_query
        }

        return render(request, 'index.html', context)

    except:
        return render(request, 'error.html')




@login_required(login_url='login')
def added_event(request):

    try:

        search_query = request.GET.get('search', '')
    
        user_profile = UserProfile.objects.get(user=request.user)
        events = Event.objects.filter(event_organizer=user_profile)

        if search_query:
            events = events.filter(
                Q(event_name__icontains=search_query) |
                Q(event_guest_speakers__icontains=search_query) |
                Q(event_time__icontains=search_query) |
                Q(event_agenda__icontains=search_query) |
                Q(event_location__icontains=search_query)
            )

        event_present = len(events) > 0

        context =  {
            'events':events,
            'event_present':event_present
        }

        return render(request, 'added_event.html', context)

    except:
        return render(request, 'error.html')




@login_required(login_url='login')
def add_event(request):

    try:

        user_profile = UserProfile.objects.get(user=request.user)

        if request.method == "POST":
            event_name = request.POST['event_name']
            event_date = request.POST['event_date']
            event_time = request.POST['event_time']
            event_location = request.POST['event_location']
            event_speaker = request.POST['event_speaker']
            event_price = request.POST['event_price']
            event_agenda = request.POST['event_agenda']

            new_event = Event.objects.create(
                event_organizer=user_profile,
                event_name=event_name,
                event_date=event_date,
                event_time=event_time,
                event_location=event_location,
                event_agenda=event_agenda,
                event_guest_speakers=event_speaker,
                event_ticket_price=event_price,
            )
            new_event.event_registered_count += 1
            new_event.save()

            messages.info(request, 'Event Added.')
            return redirect('index')
    
        else:
            return render(request, 'add_event.html')
        
    except:
        return render(request, 'error.html')




@login_required(login_url='login')
def delete_event(request):
    
    try:

        if request.method == "POST":
            event_id = request.POST.get('event_id')
            user_profile = UserProfile.objects.get(user=request.user)

            if Event.objects.filter(pk=event_id, event_organizer=user_profile).exists():
                event_delete = Event.objects.get(pk=event_id, event_organizer=user_profile)
                event_delete.event_registered_count = 0
                event_delete.delete()

                messages.info(request, 'Event Deleted Successfully.')
            else:
                messages.info(request, "You didn't create this Event.")

        return redirect('added_event')

    except:
        return render(request, 'error.html')




@login_required(login_url='login')
def registered_event(request):

    try:

        search_query = request.GET.get('search', '')
        user_profile = UserProfile.objects.get(user=request.user)
        events = EventRegistration.objects.filter(user=user_profile)

        if search_query:
            events = events.filter(
                Q(event__event_name__icontains=search_query) |
                Q(event__event_guest_speakers__icontains=search_query) |
                Q(event__event_time__icontains=search_query) |
                Q(event__event_agenda__icontains=search_query) |
                Q(event__event_location__icontains=search_query)
            )

        event_present = len(events) > 0

        context =  {
            'events':events,
            'event_present':event_present
        }

        return render(request, 'registered_event.html', context)

    except:
        return render(request, 'error.html')




@login_required(login_url='login')
def event_registration(request):
    
    try:

        if request.method == "POST":
            event_id = request.POST.get('event_id')
            user_profile = UserProfile.objects.get(user=request.user)

            if EventRegistration.objects.filter(event_id=event_id, user=user_profile).exists():
                messages.info(request, "Event Registered Already.")
                return redirect('registered_event')
        
            else:
                event = Event.objects.get(pk=event_id)

                registered_event = EventRegistration(
                    event=event,
                    user=user_profile,
                )

                registered_event.events_registered_count += 1
                registered_event.save()

                event.event_registered_count += 1
                event.save()

                messages.info(request, "Event Registered.")

        return redirect('registered_event') 
    
    except:
        return render(request, 'error.html')




@login_required(login_url='login')
def event_unregistration(request):
    
    try:

        if request.method == "POST":
            event_id = request.POST.get('event_id')
            user_profile = UserProfile.objects.get(user=request.user)
            event = Event.objects.get(pk=event_id)

            if EventRegistration.objects.filter(user=user_profile, event_id=event_id).exists():
                event_delete = EventRegistration.objects.get(user=user_profile, event_id=event_id)
                event_delete.events_registered_count -= 1
                event_delete.delete()

                event.event_registered_count -= 1
                event.save()
                messages.info(request, 'Event Unregistered Successfully.')

            else:
                messages.info(request, "You didn't register for this Event.")

        return redirect('index')

    except:
        return render(request, 'error.html')




def signup(request):

    try:

        if request.method == "POST":
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            password2 = request.POST['password2']

            if password == password2:

                if User.objects.filter(username=username).exists():
                    messages.info(request, 'Username already taken. Try another.')
                    return redirect('signup')
            
                elif User.objects.filter(email=email).exists():
                    messages.info(request, 'Email already taken. Try another.')
                    return redirect('signup')
            
                else:
                    new_user = User.objects.create_user(username=username, email=email, password=password)
                    new_user.save()

                    login_user = auth.authenticate(username=username, password=password)
                    auth.login(request, login_user)

                    user_model = User.objects.get(username=username)
                    new_profile = UserProfile.objects.create(
                        user=user_model,
                        id_user=user_model.id,
                        email=email
                    )
                    new_profile.save()

                    messages.info(request, f'Welcome {username}.')
                    return redirect('setting')
            
            else:
                messages.info(request, 'Password not the same.')
                return redirect('signup')
    
        else:
            return render(request, 'register.html')

    except:
        return render(request, 'error.html')




def login(request):

    try:

        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']

            user = auth.authenticate(username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect('index')
        
            else:
                messages.info(request, "Invalid Credentials.")
                return redirect('login')

        else:
            return render(request, 'login.html')
        
    except:
        return render(request, 'error.html')




@login_required(login_url='login')
def logout(request):

    try:

        auth.logout(request)
        return redirect('login')
    
    except:
        return render(request, 'error.html')




@login_required(login_url='login')
def setting(request):

    try:

        user_profile = UserProfile.objects.get(user=request.user)

        if request.method == "POST":

            if request.FILES.get('image') == None:
                image = user_profile.profileimg
                bio = request.POST['bio']
                address = request.POST['address']
                phone = request.POST['phone']
            
                user_profile.profileimg = image
                user_profile.bio = bio
                user_profile.address = address
                user_profile.phone_number = phone
                user_profile.save()

        
            if request.FILES.get('image') != None:
                image = request.FILES.get('image')
                bio = request.POST['bio']
                address = request.POST['address']
                phone = request.POST['phone']
            
                user_profile.profileimg = image
                user_profile.bio = bio
                user_profile.address = address
                user_profile.phone_number = phone
                user_profile.save()

        
            messages.info(request, f'{user_profile.user.username}, your Profile is updated.')
            return redirect('index')

        else:
            return render(request, 'setting.html', {'user_profile':user_profile})

    except:
        return render(request, 'error.html')
    
