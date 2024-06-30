from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Room, Topic, Message, User
from .forms import RoomForm, UserForm, MyUserCreationForm
from django.db.models import Q
# from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required  #for restricted pages to user
# from django.contrib.auth.forms import UserCreationForm

# Create your views here.
#these are the functions or classes which happen when someone goes to a url or route


# rooms = [
#   {'id':1, 'name': 'Lets learn python'},
#   {'id':2, 'name': 'Design with me'},
#   {'id':3, 'name': 'Frontend devs'},
# ]


def loginPage(request):

  page = 'login'

  # if user is already logged in, then donot show him login btn, ie cannot relogin
  if request.user.is_authenticated:
    return redirect('home')

  if request.method == 'POST':
    # get username and pw
    email = request.POST.get('email').lower()
    password = request.POST.get('password')

    try: #check is the user exists
      user = User.objects.get(email=email)
    except:
      # give flash messages
      messages.error(request, 'User does not exist')

    #once we know user exists, make sure username and pw are correct
    user = authenticate(request, email=email, password=password)
    if user is not None:
      login(request, user)  #creates a session in DB and browser
      return redirect('home')
    
    else:
      messages.error(request, 'Username or password does not exist')

  context = {'page':page}
  return render(request, 'base/login_register.html', context)


def logoutUser(request):
  logout(request)
  return redirect('home')


# def registerPage(request):
#   form = MyUserCreationForm()

#   if request.method == 'POST':   # pass the user data
#     form = MyUserCreationForm(request.POST)  #put that into userCreationForm
#     if form.is_valid():    #check if form is valid
#       # saving the form so that we could access the user
#       user = form.save(commit=False)
#       user.username = user.username.lower()    #clean username
#       user.save()                 #save the user
#       login(request, user)        #login the user
#       return redirect('home')
    
#     else:
#       messages.error(request, 'An error occured during registration')

#   return render(request, 'base/login_register.html', {'form': form})


def registerPage(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')

    return render(request, 'base/login_register.html', {'form': form})



def home(request):
  # the q value passed in th url file
  # if value of q is not specified, ie initial load, no q vaue specified, then q is ""
  q = request.GET.get('q') if request.GET.get('q')!= None else ""
  # query = ModelName.objects.method()
  # this rooms variable is overridding the above rooms array
  rooms = Room.objects.filter(
    Q(topic__name__icontains=q) |
    Q(name__icontains=q) |
    Q(description__icontains=q)
    ) 
  # we goto topic model and query upwards to name
  # contains checks if q value has some of the letters from actual string, ie even 'Py' value will give results for python
  # i in icontains is for ignore lowercase uppercase of string  

  topics = Topic.objects.all()[0:5]
  room_count = rooms.count()  # gives count of rooms in the page
  room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

  context = {'rooms': rooms, 'topics':topics, 'room_count':room_count, 
             'room_messages': room_messages}
  return render(request, 'base/home.html', context)

def room(request, pk):
  # query = ModelName.objects.method()
  # method = get, to get unique values
  room = Room.objects.get(id = pk)
  room_messages = room.message_set.all()
  # from the model "Message", get all the child objects from the room
  
  participants = room.participants.all()

  if request.method == "POST":
    # whenever posting msg, set the user, room and body in "Message" model 
    message = Message.objects.create(
      user=request.user,
      room=room,
      body=request.POST.get('body')  #this body is passed form "name=body" from room.html
    )
    room.participants.add(request.user)  #if user want to be participant of the room
    return redirect('room', pk=room.id)
  
  context = {'room': room, 'room_messages': room_messages, 'participants':participants}
  return render(request, 'base/room.html', context)


# user profile page
def userProfile(request, pk):
  user = User.objects.get(id=pk)
  rooms = user.room_set.all()   #we can get children of the specific object by modelname "room" and set.all
  room_messages = user.message_set.all()
  topics = Topic.objects.all()
  context = {'user': user, 'rooms':rooms, 'room_messages':room_messages, 'topics':topics}
  return render(request, 'base/profile.html', context)

# user can create room only if he is logged in, if not he is redirected to login page
@login_required(login_url='login')
def createRoom(request):
  form = RoomForm()
  topics = Topic.objects.all()
  if request.method == 'POST':
    topic_name = request.POST.get('topic')
    topic, created = Topic.objects.get_or_create(name=topic_name)
    
    Room.objects.create(
      host=request.user, 
      topic=topic, 
      name=request.POST.get('name'), 
      description=request.POST.get('description')
    )
    
    
    # form = RoomForm(request.POST)
    # if form.is_valid():
    #   room = form.save(commit=False)
    #   room.host = request.user
    #   room.save()
    
    return redirect('home')
    # here home is name 'name' from the urls file
  context = {'form': form, 'topics':topics}
  return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def updateRoom(request, pk):
  room = Room.objects.get(id = pk)
  form = RoomForm(instance=room) #form will be prefilled with room value, since we are updating it 
  topics = Topic.objects.all()

  # if you are a different user other than owner of the room, you cannot edit it
  if request.user != room.host:
    return HttpResponse("You are not allowed here")

  if request.method == 'POST':
    topic_name = request.POST.get('topic')
    topic, created = Topic.objects.get_or_create(name=topic_name)
    room.name=request.POST.get('name')
    room.topic=topic
    room.description=request.POST.get('description')
    room.save()
    return redirect('home')
  
  context = {'form': form, 'topics':topics}
  return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def deleteRoom(request, pk):
  room = Room.objects.get(id = pk)

  # if you are a different user other than owner of the room, you cannot delete it
  if request.user != room.host:
    return HttpResponse("You are not allowed here")

  if request.method == 'POST':
    room.delete()
    return redirect('home')
  return render(request, 'base/delete.html', {'obj':room})
  # 'room' in render is from(referencing) delete template html page


@login_required(login_url='login')
def deleteMessage(request, pk):
  message = Message.objects.get(id = pk)

  if request.user != message.user:
    return HttpResponse("You are not allowed here")

  if request.method == 'POST':
    message.delete()
    return redirect('home')
  return render(request, 'base/delete.html', {'obj':message})


@login_required(login_url='login')
def updateUser(request):
  user = request.user
  form = UserForm(instance=user)

  if request.method == 'POST':
    form = UserForm(request.POST, request.FILES, instance=user)
    if form.is_valid():
      form.save()
      return redirect('user-profile', pk=user.id)


  return render(request, 'base/update-user.html', {'form':form})


def topicsPage(request):
  q = request.GET.get('q') if request.GET.get('q')!= None else ""
  topics = Topic.objects.filter(name__icontains=q)
  return render(request, 'base/topics.html', {'topics':topics})

def activityPage(request):
  room_messages = Message.objects.all()
  return render(request, 'base/activity.html', {'room_messages':room_messages})