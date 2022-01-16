
import imp
from django.shortcuts import render,redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from django.contrib import messages
from discord_app.forms import RoomForm
from .models import Room, Topic

def login_page(request):
    if request.user.is_authenticated:
        return redirect("home")
    
    if request.method == "POST":
        username=request.POST.get("username")
        password=request.POST.get("password")

        
        

        user=authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect("home")
        else:
            messages.error(request, 'Username or Password does not exist')
    context={}
    return render(request,"discord_app/login_register.html",context)


def lougout_user(request):
    logout(request)
    return redirect("home")

def home(request):
    q=request.GET.get("q") if request.GET.get("q")!= None else ""
    rooms=Room.objects.filter(
        Q(topic__name__icontains=q)|
        Q(name__icontains=q)|
        Q(description__icontains=q)
    )

    room_count=rooms.count()
    topics=Topic.objects.all()
    context={"room":rooms,"topics":topics,"room_count":room_count}
    return render(request,"discord_app/home.html",context)

def room(request,pk):
    room=Room.objects.get(id=pk)
    context={"room":room}
    return render(request,"discord_app/room.html",context)

@login_required(login_url="login")
def create_room(request):
    form=RoomForm()
    if request.method== "POST":
        form= RoomForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect("home")

    context={"form":form}
    return render(request,"discord_app/room_form.html",context)

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