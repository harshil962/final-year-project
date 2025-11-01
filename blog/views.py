from django.shortcuts import render
from .models import Blogpost

# Create your views here.

def index(request):
    myposts = Blogpost.objects.all()
    print(myposts)
    return render(request,'blog/index.html',{'myposts':myposts})

def blogpost(request, myid=None):
    post = None
    if myid:
        try:
            post = Blogpost.objects.get(post_id=myid)
        except Blogpost.DoesNotExist:
            post = None
    return render(request, 'blog/blogpost.html', {'post': post})
