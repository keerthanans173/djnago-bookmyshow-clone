from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Count

from .models import (
    Movie,
    Show,
    Seat,
    Booking,
    Review
)


# ----------------------------
# Movie List
# ----------------------------
def movie_list(request):

    search = request.GET.get("search")

    if search:
        movies = Movie.objects.filter(name__icontains=search)
    else:
        movies = Movie.objects.all()

    trending = Movie.objects.order_by("-average_rating")[:5]

    latest = Movie.objects.order_by("-release_date")[:5]

    return render(request,
                  "movies/movie_list.html",
                  {
                      "movies": movies,
                      "trending": trending,
                      "latest": latest
                  })


# ----------------------------
# Movie Detail
# ----------------------------
def movie_detail(request, movie_id):

    movie = get_object_or_404(Movie, id=movie_id)

    shows = Show.objects.filter(movie=movie)

    reviews = Review.objects.filter(movie=movie)

    similar_movies = Movie.objects.filter(
        genres__in=movie.genres.all(),
        languages__in=movie.languages.all()
    ).exclude(id=movie.id).distinct()[:6]

    return render(request,
                  "movies/movie_detail.html",
                  {
                      "movie": movie,
                      "shows": shows,
                      "reviews": reviews,
                      "similar_movies": similar_movies
                  })


# ----------------------------
# Show List
# ----------------------------
def show_list(request, movie_id):

    movie = get_object_or_404(Movie, id=movie_id)

    shows = Show.objects.filter(movie=movie)

    return render(request,
                  "movies/show_list.html",
                  {
                      "movie": movie,
                      "shows": shows
                  })


# ----------------------------
# Seat Booking
# ----------------------------
@login_required(login_url="/login/")
def book_seats(request, show_id):

    show = get_object_or_404(Show, id=show_id)

    seats = Seat.objects.filter(show=show)

    if request.method == "POST":

        selected = request.POST.getlist("seats")

        if not selected:

            return render(request,
                          "movies/seat_selection.html",
                          {
                              "show": show,
                              "seats": seats,
                              "error": "Please select at least one seat."
                          })

        booked = []

        for seat_id in selected:

            seat = get_object_or_404(
                Seat,
                id=seat_id,
                show=show
            )

            if seat.is_booked:
                booked.append(seat.seat_number)
                continue

            try:

                Booking.objects.create(
                    user=request.user,
                    movie=show.movie,
                    theater=show.theater,
                    show=show,
                    seat=seat
                )

                seat.is_booked = True
                seat.save()

            except IntegrityError:
                booked.append(seat.seat_number)

        if booked:

            return render(request,
                          "movies/seat_selection.html",
                          {
                              "show": show,
                              "seats": seats,
                              "error": f"Already booked: {', '.join(booked)}"
                          })

        return redirect("profile")

    return render(request,
                  "movies/seat_selection.html",
                  {
                      "show": show,
                      "seats": seats
                  })


# ----------------------------
# Add Review
# ----------------------------
@login_required(login_url="/login/")
def add_review(request, movie_id):

    movie = get_object_or_404(Movie, id=movie_id)

    booking = Booking.objects.filter(
        user=request.user,
        movie=movie,
        watched=True
    ).exists()

    if not booking:
        return redirect("movie_detail", movie_id=movie.id)

    if request.method == "POST":

        rating = request.POST.get("rating")

        review_text = request.POST.get("review")

        review, created = Review.objects.get_or_create(
            movie=movie,
            user=request.user
        )

        review.rating = rating
        review.review = review_text
        review.save()

        return redirect("movie_detail", movie_id=movie.id)

    return redirect("movie_detail", movie_id=movie.id)


# ----------------------------
# Report Review
# ----------------------------
@login_required(login_url="/login/")
def report_review(request, review_id):

    review = get_object_or_404(
        Review,
        id=review_id
    )

    review.reported = True
    review.save()

    return redirect("movie_detail", movie_id=review.movie.id)