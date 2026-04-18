from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('books/', views.books),
    path('books/<int:id>/', views.book_detail),
    path('books/<int:id>/recommend/', views.recommend_books),
    path('upload-book/', views.upload_book),
    path('load-rag/', views.load_rag),
    path('ask-question/', views.ask_question),
]