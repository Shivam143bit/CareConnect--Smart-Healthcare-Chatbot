from django.urls import path
from .views import ChatPageView, ChatApiView

urlpatterns = [
    path("", ChatPageView.as_view(), name="chat_page"),   # loads chat.html
    path("api/", ChatApiView.as_view(),name="chat_api"),  # AJAX endpoint
]
