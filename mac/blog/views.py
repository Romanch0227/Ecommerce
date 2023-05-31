from django.shortcuts import render
from .models import Blog_post
from django.http import HttpResponse

# Create your views here.
def index(request):
    mypost=Blog_post.objects.all()

    return render(request,'blog/index.html',{'mypost':mypost})

def POST(request,id):
    post=Blog_post.objects.filter(post_id=id)[0]
    print(post)
    return render(request,'blog/blogpost.html',{'post':post})
