from django.urls import path

from .views import DetailView, IndexView

urlpatterns = [
    path("", IndexView.as_view(), name="user_list"),
    path("<str:id>", DetailView.as_view(), name="user_detail"),
]
