from django.shortcuts import render,redirect
from django.http import HttpResponse,Http404,HttpResponseRedirect
from .forms import ProfileForm,NewsLetterForm,ImageForm,CommentForm
from .email import send_welcome_email
from django.contrib.auth.decorators import login_required
from .models import Profile,Image,Comments

from django.contrib.auth.models import User

# Create your views here.
@login_required(login_url='/accounts/login/')
def welcome(request):
    images=Image.objects.all() 
    return render(request, 'index.html',{"images":images})
@login_required(login_url='/accounts/login/')
def prof(request,id):
    user = User.objects.get(id = id)
    profiles = Profile.objects.get(user=user)
    
    return render(request, 'all-instagram/profile.html',{"profiles":profiles},{"user":user})

@login_required(login_url='/accounts/login/')
def comm(request,id):
        image = Image.objects.get(id=id)
        comments = Comments.objects.filter(image=image)
        # print(comments)
        return render(request,'new-comment.html',{"image":image,"comments":comments})
@login_required(login_url='/accounts/login/')
def profile(request):
    current_user =request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
             profile = form.save(commit=False)
             profile.user = current_user
             profile.save()
        return redirect("home")
       
    else:
            form = ProfileForm()
    return render(request, 'new_profile.html',{"form":form})
@login_required(login_url='/accounts/login/')
def image(request):
    current_user = request.user
    if request.method =='POST':
        form =  ImageForm(request.POST,request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.user = current_user
            image.save()
        return redirect("home")    
    else:  
            form = ImageForm()
    return render(request,'new-image.html',{"form":form})
def comments(request,id):
        current_user = request.user
        post = Image.objects.get(id=id)
        comments = Comments.objects.filter(image=post)
        # print(comments)
        if request.method == 'POST':
                form = CommentForm(request.POST,request.FILES)
                if form.is_valid():
                        comment = form.cleaned_data['comment']
                        new_comment = Comments(comment = comment,user =current_user,image=post)
                        new_comment.save()
                    
                
        else:
                    form = CommentForm()
        return render(request, 'new-comment.html', {"form":form,'post':post,'user':current_user,'comments':comments})


def email(request):
    date = dt.date.today()
    news = Profile.todays_news()
    if request.method == 'POST':
        form = NewsLetterForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['your_name']
            email = form.cleaned_data['email']
            recipient = NewsLetterRecipients(name = name,email =email)
            recipient.save()
            send_welcome_email(name,email)
            HttpResponseRedirect('email')
    else:
        form = NewsLetterForm()
    return render(request, 'all-instagram/inst.html', {"date": date,"news":news,"letterForm":form})