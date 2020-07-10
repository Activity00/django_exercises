from django.urls import path

from ranking.views import RankingView

app_name = 'ranking'
urlpatterns = [
    path('', RankingView.as_view()),
]
