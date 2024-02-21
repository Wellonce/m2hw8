from django.urls import path

from apps.books.views import BookListView, BookDetailView, AddReviewView, review_delete, review_update

app_name = "books"

urlpatterns = [
    path('', BookListView.as_view(), name="book-list"),
    path('<slug:slug>/', BookDetailView.as_view(), name="book-detail"),
    path('<int:pk>', AddReviewView.as_view(), name="add-review"),
    path('review-delete/<int:pk>', review_delete, name="review-delete"),
    path('review-update/<int:pk>', review_update, name="review-update"),

]
