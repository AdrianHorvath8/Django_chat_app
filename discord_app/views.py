
from email import message
import imp
import re
from django.shortcuts import render,redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from discord_app.forms import RoomForm
from .models import Room, Topic, Message, User

def login_page(request):
    if request.user.is_authenticated:
        return redirect("home")

    page= "login"
    
    if request.method == "POST":
        username=request.POST.get("username").lower()
        password=request.POST.get("password")

        
        

        user=authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect("home")
        else:
            messages.error(request, 'Username or Password does not exist')
    context={"page":page}
    return render(request,"discord_app/login_register.html",context)


def lougout_user(request):
    logout(request)
    return redirect("home")

def register_page(request):
    form=UserCreationForm()
    if request.method == "POST":
        form=UserCreationForm(request.POST)
        if form.is_valid:
            user =form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            login(request,user)
            return redirect("home")
        else:
            messages.error(request,"Issue while registration")


    context={"form":form}
    return render(request,"discord_app/login_register.html",context)

def home(request):
    q=request.GET.get("q") if request.GET.get("q")!= None else ""
    rooms=Room.objects.filter(
        Q(topic__name__icontains=q)|
        Q(name__icontains=q)|
        Q(description__icontains=q)
    )

    room_count=rooms.count()
    topics=Topic.objects.all()
    activitys=Message.objects.filter(Q(room__topic__name__icontains=q))
    context={"room":rooms,"topics":topics,"room_count":room_count,"activitys":activitys}
    return render(request,"discord_app/home.html",context)

def room(request,pk):
    room=Room.objects.get(id=pk)
    room_message= room.message_set.all()
    participants=room.participants.all()

    if request.method=="POST":
        message=Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get("body")
        )
        room.participants.add(request.user)
        return redirect("room",pk=room.id)

    

    context={"room":room,"room_message":room_message,"participants":participants}
    return render(request,"discord_app/room.html",context)

@login_required(login_url="login")
def create_room(request):
    form=RoomForm()
    if request.method== "POST":        
        form= RoomForm(request.POST)
    if form.is_valid():
        room= form.save(commit=False)
        room.host=request.user
        room.save()
        return redirect("home")

    context={"form":form}
    return render(request,"discord_app/room_form.html",context)

def user_page(request,pk):
    user=User.objects.get(id=pk)
    rooms=user.room_set.all()
    topics=Topic.objects.all()
    activitys=user.message_set.all()
    



    context={"user":user,"topics":topics,"room":rooms,"activitys":activitys}
    return render(request,"discord_app/user_page.html",context)


@login_required(login_url="login")
def edit_room(request,pk):
    room=Room.objects.get(id=pk)
    form=RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse("You are not allowed here !!")

    if request.method=="POST":
        form= RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect("home")

    context={"form":form}

    return render(request,"discord_app/room_form.html",context)

@login_required(login_url="login")
def delete_room(request,pk):
    room=Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse("You are not allowed here !!")

    if request.method=="POST":
        room.delete()
        return redirect("home")
    return render(request,"discord_app/delete.html",{"obj":room})


@login_required(login_url="login")
def delete_message(request,pk):
    message=Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse("You are not allowed here !!")

    if request.method=="POST":
        message.delete()
        return redirect("home")
    return render(request,"discord_app/delete.html",{"obj":message})