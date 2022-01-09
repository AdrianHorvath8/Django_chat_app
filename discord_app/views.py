from django.shortcuts import render,redirect

from discord_app.forms import RoomForm
from .models import Room

def home(request):
    rooms=Room.objects.all()
    context={"room":rooms}
    return render(request,"discord_app/home.html",context)

def room(request,pk):
    room=Room.objects.get(id=pk)
    context={"room":room}
    return render(request,"discord_app/room.html",context)

def create_room(request):
    form=RoomForm()
    if request.method== "POST":
        form= RoomForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect("home")

    context={"form":form}
    return render(request,"discord_app/room_form.html",context)

def edit_room(request,pk):
    room=Room.objects.get(id=pk)
    form=RoomForm(instance=room)
    if request.method=="POST":
        form= RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect("home")

    context={"form":form}

    return render(request,"discord_app/room_form.html",context)


def delete_room(request,pk):
    room=Room.objects.get(id=pk)
    if request.method=="POST":
        room.delete()
        return redirect("home")
    return render(request,"discord_app/delete.html",{"obj":room})