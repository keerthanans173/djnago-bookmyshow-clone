from django.urls import path
from . import views

app_name = "movies"

urlpatterns = [
    # Movie List
    path("", views.movie_list, name="movie_list"),

    # Movie Details
    path("movie/<int:movie_id>/", views.movie_detail, name="movie_detail"),

    # Show List for a Movie
    path("movie/<int:movie_id>/shows/", views.show_list, name="show_list"),

    # Book Seats
    path("show/<int:show_id>/book/", views.book_seats, name="book_seats"),

    # Add/Edit Review
    path("movie/<int:movie_id>/review/", views.add_review, name="add_review"),

    # Report Review
    path("review/<int:review_id>/report/", views.report_review, name="report_review"),
]