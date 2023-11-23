from django.urls import path

from . import views

app_name = "blog"
urlpatterns = [
    path("", views.home, name="home"),
    path("articles", views.articles, name="articles"),
    path("article/<int:article_id>", views.article, name="article"),
    path("find", views.find, name="find")
]