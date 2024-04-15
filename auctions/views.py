from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Auction, Bid
from .utils import options
from .verifications import verify_listing
from .models_handler import save_auction, create_bid

def index(request):
    listings = Auction.objects.exclude(author=request.user.id).filter(status=0)

    return render(request, "auctions/index.html", {
        "listings": listings
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
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def detailed_listing(request, listing_id):
    listing = Auction.objects.get(pk=listing_id)
    higher_bid = Bid.objects.filter(auction_id=listing_id).order_by("-amount")[0]
    return render(request, "auctions/detailed-listing.html", {
        "listing": listing,
        "is_author": listing.author.id == request.user.id,
        "on_watchlist": len(listing.watchlist.filter(id=request.user.id)) == 1,
        "higher_bid": higher_bid,
    })

@login_required
def create_listing(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        cover = request.FILES["cover"]
        initial_bid = int(request.POST["initial_bid"])
        category = request.POST["category"]

        response = verify_listing(title, description, initial_bid, category, cover)
        if not response["success"]:
            return render(request, "auctions/create-listing.html", {
                "options": options,
                "message": response["message"]
            })
        
        save_auction(title, description, initial_bid, category, cover, User(request.user.id))

        return HttpResponseRedirect(reverse("index"))
        

    return render(request, "auctions/create-listing.html", {
        "options": options
    })

@login_required
def bid(request, listing_id):
    if request.method == "POST":
        bid_amount = float(request.POST["bid-amount"])
        higher_bid = Bid.objects.filter(auction_id=listing_id).order_by("-amount")[0]

        #verification

        create_bid(Auction.objects.get(pk=listing_id), User.objects.get(pk=request.user.id), bid_amount)
        return HttpResponseRedirect(reverse("see listing", args=[listing_id]))



@login_required
def add_watchlist(request, listing_id):
    listing = Auction.objects.get(pk=listing_id)
    listing.watchlist.add(User.objects.get(pk= request.user.id))

    return HttpResponseRedirect(reverse("see listing", args=[listing_id]))

@login_required
def remove_watchlist(request, listing_id):
    listing = Auction.objects.get(pk=listing_id)
    listing.watchlist.remove(User.objects.get(pk= request.user.id))

    return HttpResponseRedirect(reverse("see listing", args=[listing_id]))

@login_required
def close_auction(request, listing_id):
    listing = Auction.objects.get(pk=listing_id)
    higher_bid = Bid.objects.filter(auction_id=listing_id).order_by("-amount")[0]
    
    listing.status = 1
    listing.winner = higher_bid.author
    listing.save()

    return HttpResponseRedirect(reverse("see listing", args=[listing_id]))

