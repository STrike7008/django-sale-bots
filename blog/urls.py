from django.urls import path
from . import views

urlpatterns = [
    path("", views.blog, name="blog"),
    path("post/<slug:title>/", views.blog_post, name="post"),
    path("category/<str:name>/", views.blog_category, name="category"),
    path("search/", views.blog_search, name="blog_search"),
]