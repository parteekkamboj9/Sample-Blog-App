from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt

from myApp import models
from myApp.forms import RegisterForm


# Create your views here.


@csrf_exempt
def index(request):
    search = request.GET.get('search', None)
    if search:
        posts = models.BlogDb.objects.filter(
            Q(title__icontains=search) |
            Q(category__name__icontains=search) |
            Q(meta_keyword__icontains=search) |
            Q(meta_description__icontains=search) |
            Q(tags__name__icontains=search)
        ).order_by("-id")  # fetching all post objects from database
    else:
        posts = models.BlogDb.objects.all().order_by("-id")  # fetching all post objects from database
    tags = models.Tag.objects.all()[:20]
    blog_categories = models.BlogCategoryDb.objects.all()[:5]
    latest_post = posts[:5]
    p = Paginator(posts, 5)  # creating a paginator object
    # getting the desired page number from url
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)

    context = {'page_obj': page_obj, 'blog_categories': blog_categories, 'latest_post': latest_post, "tags": tags}
    # sending the page object to index.html
    return render(request, 'posts.html', context)
    # template_name = "posts.html"
    # queryset = models.BlogDb.objects.all()


@login_required
@csrf_exempt
def add_blog(request):
    if request.method == "POST":
        title = request.POST.get('title')
        category_id = request.POST.get('category')
        blog_type = request.POST.get('type')
        description = request.POST.get('description')
        tags = str(request.POST.get('tags', ""))
        image = request.FILES.get('image')
        blog = models.BlogDb(
            title=title,
            category=models.BlogCategoryDb.objects.get(id=int(category_id)),
            type=blog_type,
            description=description,
            image=image,
            user=request.user
        )
        blog.save()
        print(tags, "------t")
        tags = tags.split(",")
        for tag_name in tags:
            if tag_name:
                tag, _ = models.Tag.objects.get_or_create(name=tag_name.strip())
                blog.tags.add(tag.id)
        messages.success(request, 'Blog post created successfully!')
        return redirect(f'/blog/{blog.id}')

    categories = models.BlogCategoryDb.objects.all()
    return render(request, "add-blog.html", {'categories': categories})


@csrf_exempt
def login_view(request):
    if request.method == 'POST':

        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            username = models.User.objects.get(email=email).username
        except:
            messages.error(request, "Invalid email address")
            return redirect('/login')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Hi ,Welcome to Dashboard.')
            return redirect('/')
        else:
            messages.error(request, 'Invalid email or password!!!')
            return redirect("/login")
    return render(request, "login.html")


@csrf_exempt
def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            print("-----------valid")
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')

            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, "Your signup was successful")
                return redirect("/")
            else:
                messages.success(request, "Your signup was successful, Please try to login.")
                return redirect("/login")
        messages.error(request, 'Invalid information ,Please try again.')
        return redirect('/register')
    else:
        return render(request, "register.html", locals())


def logout_view(request):
    logout(request)
    messages.success(request, 'Log Out Successfully!')
    return redirect('/login')


def blog_details(request, b_id):
    try:
        posts = models.BlogDb.objects.all().order_by("-id")
        blog = posts.get(id=b_id)
        comments = models.BlogCommentsDb.objects.filter(blog_id=b_id)
        tags = blog.tags.all()[:20]
        blog_categories = models.BlogCategoryDb.objects.all()[:5]
        latest_post = posts[:5]
    except:
        return redirect('/')
    return render(request, "blog.html", locals())


@login_required
@csrf_exempt
def add_comment(request, b_id=False):
    comment = request.POST.get('comment')
    if b_id and comment:
        if request.method == "POST":
            instance = models.BlogCommentsDb(
                blog=models.BlogDb.objects.get(id=b_id),
                user=request.user,
                comment=request.POST.get('comment')
            )
            instance.save()
        return redirect(f"/blog/{b_id}")
    return redirect("/")
