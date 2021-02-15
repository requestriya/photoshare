from django.shortcuts import render, HttpResponseRedirect, redirect
from .models import Category, Photo
from .forms import LoginForm, SignUpForm, EditUserChangeForm
from django.contrib.auth import authenticate, login, logout
# Create your views here.
def home(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = LoginForm(request=request, data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)
                    return HttpResponseRedirect('/gallery/')
                else:
                    return HttpResponseRedirect('/')
        else:
            form = LoginForm()
        return render(request, 'photo/user_login.html', {'form':form})
    else:
        return HttpResponseRedirect('/gallery/')

def user_signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect('/gallery/') 
    else:
        form = SignUpForm()
    return render(request, 'photo/user_signup.html', {'form':form})

def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')
def photo_delete(request, pk):
    if request.user.is_authenticated:
        deldata = Photo.objects.get(id=pk)
        deldata.delete()
        return HttpResponseRedirect('/gallery/')
    else:
        return HttpResponseRedirect('/')

def gallery(request):
    if request.user.is_authenticated:
        category = request.GET.get('category')
        user = request.user
        if category == None:
            photos= Photo.objects.filter(user=user)
        else:
            photos = Photo.objects.filter(category__name=category, user=user)

        categories=Category.objects.filter(user=user)
        return render(request, 'photo/gallery.html', {'categories': categories, 'photos':photos})
    else:
        return redirect('homepage')

def ViewPhoto(request, pk):
    if request.user.is_authenticated:
        photo = Photo.objects.get(id=pk)
        return render(request, 'photo/photo.html', {'photo':photo})
    else:
        return redirect('homepage')

def AddPhoto(request):
    if request.user.is_authenticated:
        user=request.user
        categories=Category.objects.filter(user=user)

        if request.method == 'POST':
            data = request.POST
            image = request.FILES.get('image')
            
            if data['category'] != 'none':
                category=Category.objects.get(id=data['category'])
            elif data['category_new'] != '':
                category, created = Category.objects.get_or_create(name=data['category_new'], user=user)
            else:
                category=None
            
            photo = Photo.objects.create(
                category=category,
                description=data['description'],
                image=image,
                user=request.user,
            )
            return redirect('gallery')
        return render(request, 'photo/add.html',{'categories': categories})
    else:
        return redirect('homepage')