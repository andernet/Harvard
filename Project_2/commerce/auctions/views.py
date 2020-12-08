from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django import forms
from django.db.models import Max
from datetime import datetime

from .models import User
from .models import Category
from .models import Listing
from .models import WatchList
from .models import Bid
from .models import Comment


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all(),
        "title": "Active Listings"
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            watchList = WatchList()
            watchList.save()
            user = User.objects.create_user(username, email, password, watch_list=watchList)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required(login_url='/login')
def new_listing(request):
    if request.method == "POST":
        form = NewListingForm(request.POST)
        if form.is_valid():
            new_listing = Listing(user=request.user, title=request.POST["title"], description=request.POST["description"], start_bid=request.POST["startBid"], current_price=request.POST["startBid"])
            if request.POST["category"] != "":
                new_listing.category = Category.objects.get(id=request.POST["category"])
                new_listing.dateTime = datetime.now()
            if request.POST["image"] != "":
                new_listing.image = request.POST["image"]
            new_listing.save()
            return index(request)
        else:
            return render(request, "auctions/new_listing.html", {
                "form": form
            })
    else:
        return render(request, "auctions/new_listing.html", {
            "form": NewListingForm()
        })

@login_required(login_url='/login')
def new_bid(request):
    if request.method == "POST":
        form = NewBidForm(request.POST) 
        if form.is_valid(): 
            error = ""
            if float(request.POST["bid"]) > Listing.objects.get(id=request.POST["listing_id"]).current_price:
                new_bid = Bid(user=request.user, listing=Listing.objects.get(id=request.POST["listing_id"]), value=request.POST["bid"])
                new_bid.save()
                l = Listing.objects.get(id=request.POST["listing_id"])
                l.current_price = request.POST["bid"]
                l.save()
            else:
                error = "The value must be greater than the current price"  
        else:
            error = "Input a valid format (00.00)"
        return listing(request, Listing.objects.get(id=request.POST["listing_id"]).title, error)

@login_required(login_url='/login')
def watchlist(request):
    # get the listings from the User's watchlist
    l = Listing.objects.filter(watchListings__id=request.user.watch_list.id)
    return render(request, "auctions/index.html", {
        "listings": l,
        "title": "Watchlist"
    })

def listing(request, title, error=""):
    try:
        l = Listing.objects.get(title=title)
    except Listing.DoesNotExist:  # the request is to add a item to user's watchlist
        l = Listing.objects.get(id=title)
        if request.user.watch_list not in l.watchListings.all():
            l.watchListings.add(request.user.watch_list)
        else:
            l.watchListings.remove(request.user.watch_list)
    if l is not None:
        w = False
        if request.user.watch_list in l.watchListings.all():
            w = True
        # get the greater bid of the listing
        try:
            gr_bid = Bid.objects.filter(listing=l).order_by('-value')[0]
        except IndexError:
            gr_bid = l.current_price
        # get the comments of the listing
        comments = Comment.objects.filter(listing=l)
        return render(request, "auctions/listing.html", {
        "listing": l,
        "comments": comments,
        "gr_bid": gr_bid,
        "w": w,  # if true, the listing already is in a watchlist
        "bid_form": NewBidForm(),
        "comment_form": NewCommentForm(),
        "error": error
    })
    else:
        return index("error!")

def list_categories(request):
    cats = Category.objects.all()
    return render(request,"auctions/list_categories.html", {
        "cats":cats
    })

def category(request, cat):
    listings = Listing.objects.filter(category=cat)
    cat = Category.objects.get(id=cat)
    return render(request, "auctions/index.html", {
        "listings": listings,
        "title": f"Category: {cat.name}"
    })

def listing_by_category(request, cat):
    l = Listing.filter(category__id=cat)


@login_required
def new_comment(request):
    if request.method == "POST":
        form = NewCommentForm(request.POST)
        if form.is_valid():
            l = Listing.objects.get(id=request.POST["listing_id"])
            comment = Comment(text=request.POST["comment"], user=request.user, listing=l)
            comment.save()
    return listing(request, l.title, "")

@login_required
def close_listing(request, id):
    try:
        l = Listing.objects.get(id=id)
    except Listing.DoesNotExist:
        return HttpResponse("Listing not find")
    win_bid = Bid.objects.filter(listing=l).order_by('-value')[0]
    l.active = False
    l.save()
    w = False
    if request.user.watch_list in l.watchListings.all():
        w = True
    return render(request, "auctions/listing.html", {
    "listing": l,
    "w": w,  # if true, the listing already is in a watchlist
    "bid_form": NewBidForm(),
    "comment_form": NewCommentForm(),
    "error": ""
    })

class NewListingForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Title'}))
    description = forms.CharField(widget=forms.Textarea())
    startBid = forms.DecimalField(label="Start Bid", max_digits=10, decimal_places=2, localize=True)
    image = forms.URLField(label="Image's URL", required=False)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False)

class NewBidForm(forms.Form):
    bid = forms.DecimalField(widget=forms.TextInput(attrs={'placeholder': 'Bid Value'}))

class NewCommentForm(forms.Form):
    comment = forms.CharField(label=False,widget=forms.Textarea(attrs={'placeholder': 'Input a new comment'}))