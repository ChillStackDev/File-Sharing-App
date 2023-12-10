from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render, redirect,get_object_or_404
from .forms import FileUploadForm
from .models import UploadedFile
from django.http import HttpResponse
from django.conf import settings
import os


# Create your views here.
def index(request):
    if request.method == 'POST':
        print("call")
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            print("enter")
            new_file = form.save(commit=False)
            new_file.user = request.user
            new_file.save()
            print("save")
            return redirect('index') 
    else:
        print("else")
        form = FileUploadForm()
    user_files = UploadedFile.objects.filter(user=request.user.id)
    all_users = User.objects.exclude(id=request.user.id)
    recieved_files = UploadedFile.objects.filter(shared_with=request.user.id)
    shared_by_me = UploadedFile.objects.filter(user=request.user.id, shared_with__isnull=False).exclude(shared_with=request.user.id).distinct()
    return render(request, 'index.html', {'form': form,'user_files': user_files,'all_users':all_users,'recieved_files': recieved_files,'shared_by_me':shared_by_me})
    
def search(request):
    
    query = request.GET.get('query')
    users = User.objects.filter(username__icontains=query)
    user_files = UploadedFile.objects.filter(user__username__icontains=query)
    return render(request, 'search.html', {'users': users, 'user_files': user_files, 'query': query})


def share_file(request, file_id):
    print("call;;;;")
    uploaded_file = get_object_or_404(UploadedFile, id=file_id)
    if request.method == 'POST':
        print("caldedecevevvrtv")
        user_to_share_id = request.POST.get('user_to_share')
        user = User.objects.get(id=user_to_share_id)
        uploaded_file.shared_with.add(user)
        uploaded_file.save()
        messages.success(request, 'File Successfully Shared!!')
        
    else:
         messages.error(request, 'Error In Sharing File!!') 
         
    return redirect('/')
    




def download_file(request, file_id):
    uploaded_file = get_object_or_404(UploadedFile, id=file_id)
    file_path = os.path.join(settings.MEDIA_ROOT, str(uploaded_file.file))
    with open(file_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/force-download')
        response['Content-Disposition'] = f'attachment; filename="{uploaded_file.file.name}"'
        return response











def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
       
        password = request.POST.get('password')
        
        if not User.objects.filter(username=username).exists():
            
            messages.error(request, 'Username does not exists!!!')
            return redirect('/login/')
        
        user=authenticate(username=username,password=password)
        
        if user is None:
            messages.error(request, 'Invalid Password!!!')
            return redirect('/login/')
        else:
            login(request,user)
            return redirect('/')
            
    return render(request,'login.html')

def logout_page(request):
    logout(request)
    return redirect('/')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            
            messages.error(request, 'Username or email already exists!!!')
            return redirect('/register/')
        
        user=User.objects.create(username=username,email=email)
        user.set_password(password)
        user.save()
        messages.success(request, 'Registration successful. You can now log in.')
        return redirect('/register/')
    return render(request, 'register.html')



