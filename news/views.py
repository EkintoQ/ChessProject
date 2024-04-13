import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
from django.views import View


class NewsView(View):
    template_name = "chess_engine/home.html"

    def get(self, request, *args, **kwargs):
        url = "https://www.chess.com/news"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        article_headers = soup.find_all("a", class_="post-preview-title")
        article_bodys = soup.find_all("p", class_="post-preview-excerpt")
        # article_imgs = soup.find_all("p", class_="post-preview-image")
        headers = []
        for data in article_headers:
            headers.append(data.get_text(strip=True))
        bodys = []
        for data in article_bodys:
            bodys.append(data.get_text(strip=True))
        print(headers)
        return render(
            request,
            self.template_name,
            {"news_data": ""},
        )
