from django.shortcuts import render
from django.views import View


class News(View):
    template_name = "users/profile.html"

    def get(self, request, *args, **kwargs):

        return render(
            request,
            self.template_name,
            {"news_data": ""},
        )
