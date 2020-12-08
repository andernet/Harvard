from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_listing", views.new_listing, name="new_listing"),
    path("new_bid", views.new_bid, name="new_bid"),
    path("new_comment", views.new_comment, name="new_comment"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("list_categories", views.list_categories, name="list_categories"),
    path("cat/<int:cat>", views.category, name="category"),
    path("<str:title>", views.listing, name="listing"),
    path("close/<int:id>", views.close_listing, name="close_listing")
]
