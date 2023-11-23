from django.shortcuts import render, get_object_or_404

from .models import Article

# Create your views here.
def index(request):
    articles = Article.objects.all()
    return render(request, "blog/index.html", {"articles": articles})

def article(request, article_id):
    current_article = get_object_or_404(Article, pk=article_id)
    paragraphs = current_article.body.split("\r\n")
    edited_paragraphs = ["#br" if paragraph=="" else paragraph for paragraph in paragraphs]
    return render(request, "blog/article.html", {"title": current_article.title, "paragraphs": edited_paragraphs})