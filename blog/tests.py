from django.test import TestCase
from django.urls import reverse
from datetime import datetime, timedelta

import random

from .models import Article
# Create your tests here.

def create_article(body=None, date=None, visible=True):
    article_titles = ['test title 0', 'test title 1', 'test title 2', 'test title 3']
    article_bodies = ['test body 0', 'test body 1', 'test body 2', 'test body 3']
    article_authors = ['test author 0', 'test author 1', 'test author 2', 'test author 3']

    
    return Article.objects.create(
        title=random.choice(article_titles),
        body=body or random.choice(article_bodies),
        authors=random.choice(article_authors),
        date=date or datetime.now(),
        visible=visible
    )

class ArticlesViewTest(TestCase):
    """
    Testing the articles view
    """

    def test_no_articles(self):
        """
        When there are no articles, webpage should display the message 'No articles available'
        """
        response = self.client.get(reverse("blog:articles"))
        self.assertContains(response, "No articles available")

    def test_one_visible_article(self):
        """
        Visible article should be shown on the articles page
        """

        article = create_article()

        response = self.client.get(reverse("blog:articles"))
        self.assertQuerySetEqual(response.context["articles"], [article])
        # self.assertContains(response, "No articles available")
        self.assertContains(response, article.title)
        self.assertContains(response, article.date.strftime("%b. %d, %Y"))

    def test_one_invisible_article(self):
        """
        Invisible article should not be shown on articles page
        """

        articles = create_article(visible=False)

        response = self.client.get(reverse("blog:articles"))
        self.assertContains(response, "No articles available")
        self.assertQuerySetEqual(response.context["articles"], [])

    def test_multiple_visible_articles(self):
        """
        10 visible articles are shown in articles page
        """

        articles = [create_article() for i in range(10)]
        response = self.client.get(reverse("blog:articles"))

        self.assertQuerySetEqual(response.context['articles'], articles, ordered=False)

    def test_multiple_invisible_articles(self):
        """
        10 visible articles are shown in articles page
        """

        articles = [create_article(visible=False) for i in range(10)]
        response = self.client.get(reverse("blog:articles"))

        self.assertQuerySetEqual(response.context['articles'], [])
        self.assertContains(response, "No articles available")

    def test_mixed_articles(self):
        """
        With a mix of invisble and visible articles, only visible ones should show up
        """

        articles = [create_article(visible=(i%2==0)) for i in range(10)]
        visible_articles = [article for article in articles if article.visible]
        response = self.client.get(reverse("blog:articles"))

        self.assertQuerySetEqual(response.context['articles'], visible_articles, ordered=False)

    def test_past_article(self):
        """
        Testing past article - should show on page
        """

        article = create_article(date=datetime.now() + timedelta(days=-3))
        response = self.client.get(reverse("blog:articles"))
        self.assertQuerySetEqual(response.context['articles'], [article])

    def test_current_article(self):
        """
        Testing current article (article from current day) - should show on page
        """

        article = create_article(date=datetime.now())
        response = self.client.get(reverse("blog:articles"))
        self.assertQuerySetEqual(response.context['articles'], [article])
    
    def test_future_article(self):
        """
        Testing future article - should not show on page
        """

        article = create_article(date=datetime.now() + timedelta(days=3))
        response = self.client.get(reverse("blog:articles"))
        self.assertQuerySetEqual(response.context['articles'], [])
        self.assertContains(response, "No articles available")


class SpecificArticleViewTest(TestCase):
    def test_visible_article(self):
        """
        Testing a regular visible article
        """

        article = create_article()

        response = self.client.get(reverse("blog:article", args=[article.id]))
        self.assertContains(response, article.title)
        self.assertContains(response, article.body)
        self.assertContains(response, article.date.strftime("%b. %d, %Y"))

    def test_visible_article(self):
        """
        Testing an invisible article - should still show up
        """

        article = create_article(visible=False)

        response = self.client.get(reverse("blog:article", args=[article.id]))
        self.assertContains(response, article.title)
        self.assertContains(response, article.body)
        self.assertContains(response, article.date.strftime("%b. %d, %Y"))

    def test_image_in_body(self):
        """
        Testing if img tags show up when using the '$img.' symbol in body
        """

        article = create_article(body="$img.wow.png")

        response = self.client.get(reverse("blog:article", args=[article.id]))
        self.assertContains(response, '<img src=/static/images/wow.png alt="image">')

    def test_missing_article(self):
        """
        Missing article should return 404
        """

        response = self.client.get(reverse("blog:article", args=[1]))
        self.assertEqual(response.status_code, 404)

    def test_future_article(self):
        """
        Future article should return 404
        """

        article = create_article(date=datetime.now() + timedelta(days=3))
        response = self.client.get(reverse("blog:article", args=[article.id]))
        self.assertEqual(response.status_code, 404)

    def test_past_article(self):
        """
        Past article should show
        """

        article = create_article(date=datetime.now() + timedelta(days=-3))
        response = self.client.get(reverse("blog:article", args=[article.id]))
        self.assertEqual(response.context['article'], article)
        self.assertContains(response, article.title)
        self.assertContains(response, article.body)
    
    def test_current_article(self):
        """
        Current article (today) should show
        """

        article = create_article(date=datetime.now())
        response = self.client.get(reverse("blog:article", args=[article.id]))
        self.assertEqual(response.context['article'], article)
        self.assertContains(response, article.title)
        self.assertContains(response, article.body)
    





        