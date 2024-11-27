from django . shortcuts import render,redirect
from django.contrib.auth.models import User
from todo.models import TODOO
from . import models
from django.contrib.auth.decorators import login_required


from django.contrib.auth import login, authenticate,logout

def signup(request):
    if request.method=="POST":
        fnm=request.POST.get('fnm')
        emailid=request.POST.get('email')
        pwd=request.POST.get('pwd')
        print(fnm,emailid,pwd)

        my_user=User.objects.create_user(fnm,emailid,pwd)
        my_user.save()
        return redirect('/login')

    return render(request,'signup.html')

def loginn(request):
    if request.method=="POST":
        fnm=request.POST.get('fnm')
        
        pwd=request.POST.get('pwd')
        print(fnm,pwd)
        userr=authenticate(request,username=fnm,password=pwd)
        if userr is not None:
            login(request,userr)
            return redirect('/todopage')
        else:
            return redirect('/login')
    return render(request,'login.html')

@login_required(login_url="/loginn")
def todo(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            obj = models.TODOO(title=title, user=request.user)
            obj.save()
        return redirect('/todopage')  # Redirect without passing context

    # Fetch todos for the logged-in user, ordered by the most recent date
    res = models.TODOO.objects.filter(user=request.user).order_by('-date')
    return render(request, 'todo.html', {'res': res})

def edit_todo(request,srno):
    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            obj = models.TODOO.objects.get(srno=srno)
            obj.title=title
            obj.save()
        return redirect('/todopage',{"obj":obj})  # Redirect without passing context

    obj = models.TODOO.objects.get(srno=srno)
    return render(request, 'todo.html')
    

def delete_todo(request,srno):
    obj=models.TODOO.objects.get(srno=srno)
    obj.delete()
    return redirect('/todopage')
