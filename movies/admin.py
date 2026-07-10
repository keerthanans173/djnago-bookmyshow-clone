from django.contrib import admin
from .models import (
    Genre,
    Language,
    CastMember,
    Movie,
    MovieImage,
    Theater,
    Show,
    Seat,
    Booking,
    Review,
)


# -----------------------
# Inline for Multiple Movie Images
# -----------------------
class MovieImageInline(admin.TabularInline):
    model = MovieImage
    extra = 1


# -----------------------
# Movie Admin
# -----------------------
@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "certificate",
        "duration",
        "release_date",
        "average_rating",
    )

    search_fields = ("name",)

    list_filter = (
        "certificate",
        "genres",
        "languages",
    )

    filter_horizontal = (
        "genres",
        "languages",
        "cast_members",
    )

    inlines = [MovieImageInline]


# -----------------------
# Genre Admin
# -----------------------
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


# -----------------------
# Language Admin
# -----------------------
@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


# -----------------------
# Cast Admin
# -----------------------
@admin.register(CastMember)
class CastMemberAdmin(admin.ModelAdmin):
    list_display = ("name", "role")
    search_fields = ("name", "role")


# -----------------------
# Theater Admin
# -----------------------
@admin.register(Theater)
class TheaterAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "city",
        "address",
    )

    search_fields = (
        "name",
        "city",
    )


# -----------------------
# Show Admin
# -----------------------
@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    list_display = (
        "movie",
        "theater",
        "show_time",
        "ticket_price",
    )

    list_filter = (
        "movie",
        "theater",
    )


# -----------------------
# Seat Admin
# -----------------------
@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = (
        "show",
        "seat_number",
        "is_booked",
    )

    list_filter = (
        "show",
        "is_booked",
    )


# -----------------------
# Booking Admin
# -----------------------
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "movie",
        "theater",
        "show",
        "seat",
        "watched",
        "booked_at",
    )

    list_filter = (
        "movie",
        "theater",
        "watched",
    )

    search_fields = (
        "user__username",
        "movie__name",
    )


# -----------------------
# Review Admin
# -----------------------
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "movie",
        "user",
        "rating",
        "verified_viewer",
        "reported",
        "created_at",
    )

    list_filter = (
        "rating",
        "verified_viewer",
        "reported",
    )

    search_fields = (
        "movie__name",
        "user__username",
    )