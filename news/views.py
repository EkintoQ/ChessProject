from django.shortcuts import render
from django.views import View

from news.models import Article


class HomeView(View):
    def get(self, request, *args, **kwargs):

        articles = Article.objects.all()[:3]

        return render(request, "chess_engine/home.html", {"articles": articles})


class NewsView(View):
    def get(self, request, *args, **kwargs):

        articles = Article.objects.all()

        return render(request, "news/news.html", {"articles": articles})
