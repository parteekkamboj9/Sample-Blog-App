from django.urls import path

from myApp import views

urlpatterns = [
    path("", views.index, name=""),
    path("add-blog", views.add_blog, name="add-blog"),
    path("blog/<b_id>", views.blog_details, name="blog"),
    path('add-comment/<b_id>', views.add_comment),
    path("search", views.index, name="search"),

    # Auth
    path("login", views.login_view, name="login"),
    path("register", views.register_view, name="register"),
    path("logout", views.logout_view, name="logout"),

    # Blogs
    # path('blog-details/', views.blog_details),
    # path('blog-details/<int:id>/', views.blog_details),
    # path('blog-grid/', views.blog_grid),
    # path('blog-list/', views.blog_list),
    # path('add-comment/<int:id>/', views.add_comment),

]
