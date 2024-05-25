from django.core.management.base import BaseCommand
import requests
from bs4 import BeautifulSoup

from news.models import Article


# from io import StringIO
#
# out = StringIO()
#
# call_command('scrap_news', stdout=out)
# command = CommandClass(stdout=out)
# command.handle()


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    # def add_arguments(self, parser):
    #     parser.add_argument("poll_ids", nargs="+", type=int)

    def handle(self, *args, **options):
        url = "https://www.chess.com/news"
        response = requests.get(url, timeout=30)
        soup = BeautifulSoup(response.text, "html.parser")
        article_titles = soup.find_all("a", class_="post-preview-title")
        article_dates = soup.find_all("span", class_="post-preview-meta-content")
        article_bodies = soup.find_all("p", class_="post-preview-excerpt")
        article_image_url = soup.find_all("img", class_="post-preview-thumbnail")

        for title, date, body, image_url in zip(
            article_titles, article_dates, article_bodies, article_image_url
        ):
            title_text = title.text.strip()
            date_str = date.text.strip()
            body_text = body.text.strip()
            src = image_url.attrs.get("src")
            chess_url = title.attrs.get("href")

            article = Article(
                title=title_text,
                date=date_str,
                body=body_text,
                image_url=src,
                url=chess_url,
            )
            article.save()

    def get_article_links(self):
        ...

    def get_article_data(self):
        ...
