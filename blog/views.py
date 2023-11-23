from django.shortcuts import render, get_object_or_404

from .models import Article

# Create your views here.
def home(request):
    return render(request, "blog/home.html")

def articles(request):
    articles = Article.objects.all()
    return render(request, "blog/articles.html", {"articles": articles})

def article(request, article_id):
    current_article = get_object_or_404(Article, pk=article_id)
    paragraphs = current_article.body.split("\r\n")
    edited_paragraphs = ["#br" if paragraph=="" else paragraph for paragraph in paragraphs]
    return render(request, "blog/article.html", {"article": current_article, "paragraphs": edited_paragraphs})

def find(request):
    return render(request, "blog/find.html")

def custom404(request, exception):
    return render(request, "blog/404.html", status=404)