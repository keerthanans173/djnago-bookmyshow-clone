from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg
from django.utils import timezone


# -----------------------
# Genre Model
# -----------------------
class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# -----------------------
# Language Model
# -----------------------
class Language(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


# -----------------------
# Cast Model
# -----------------------
class CastMember(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    image = models.ImageField(upload_to="cast/", blank=True, null=True)

    def __str__(self):
        return self.name


# -----------------------
# Movie Model
# -----------------------
class Movie(models.Model):

    CERTIFICATE_CHOICES = [
        ('U', 'U'),
        ('UA', 'UA'),
        ('A', 'A'),
    ]

    name = models.CharField(max_length=255)

    image = models.ImageField(upload_to="movies/")

    trailer_url = models.URLField(blank=True)

    genres = models.ManyToManyField(Genre, related_name="movies")

    languages = models.ManyToManyField(Language)

    cast_members = models.ManyToManyField(CastMember)

    duration = models.PositiveIntegerField(help_text="Duration in minutes")

    certificate = models.CharField(
        max_length=2,
        choices=CERTIFICATE_CHOICES,
        default='U'
    )

    release_date = models.DateField()

    description = models.TextField(blank=True, null=True)

    average_rating = models.FloatField(default=0)

    def __str__(self):
        return self.name

    def update_rating(self):
        avg = self.reviews.aggregate(Avg("rating"))["rating__avg"]
        self.average_rating = avg if avg else 0
        self.save()


# -----------------------
# Multiple Posters
# -----------------------
class MovieImage(models.Model):

    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name="gallery"
    )

    image = models.ImageField(upload_to="movie_gallery/")

    def __str__(self):
        return self.movie.name


# -----------------------
# Theater
# -----------------------
class Theater(models.Model):

    name = models.CharField(max_length=255)

    city = models.CharField(max_length=100)

    address = models.TextField()

    def __str__(self):
        return self.name


# -----------------------
# Show Schedule
# -----------------------
class Show(models.Model):

    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name="shows"
    )

    theater = models.ForeignKey(
        Theater,
        on_delete=models.CASCADE,
        related_name="shows"
    )

    show_time = models.DateTimeField()

    ticket_price = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.movie.name} - {self.theater.name}"


# -----------------------
# Seat
# -----------------------
class Seat(models.Model):

    show = models.ForeignKey(
        Show,
        on_delete=models.CASCADE,
        related_name="seats"
    )

    seat_number = models.CharField(max_length=10)

    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return self.seat_number


# -----------------------
# Booking
# -----------------------
class Booking(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE
    )

    theater = models.ForeignKey(
        Theater,
        on_delete=models.CASCADE
    )

    show = models.ForeignKey(
        Show,
        on_delete=models.CASCADE
    )

    seat = models.OneToOneField(
        Seat,
        on_delete=models.CASCADE
    )

    booked_at = models.DateTimeField(auto_now_add=True)

    watched = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.movie.name}"


# -----------------------
# Review
# -----------------------
class Review(models.Model):

    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    rating = models.IntegerField()

    review = models.TextField()

    verified_viewer = models.BooleanField(default=False)

    reported = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('movie', 'user')

    def save(self, *args, **kwargs):

        booking = Booking.objects.filter(
            user=self.user,
            movie=self.movie,
            watched=True
        ).exists()

        self.verified_viewer = booking

        super().save(*args, **kwargs)

        self.movie.update_rating()

    def __str__(self):
        return f"{self.user.username} - {self.movie.name}"