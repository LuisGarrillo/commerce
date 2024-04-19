from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Auction, Bid, Comment
from .utils import options, genders
from .verifications import verify_listing, verify_bid, verify_comment
from .models_handler import save_auction, create_bid, create_comment

def index(request, category = None):
    listings = Auction.objects.exclude(author=request.user.id)
    if category:
        listings = listings.filter(category=category)
    
    listings = listings.filter(status=0)
    
    return render(request, "auctions/index.html", {
        "listings": listings,
        "options": options
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
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        birthday = request.POST["birthday"]
        gender = request.POST["gender"]
        cellphone_number = request.POST["cellphone"]

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
        return render(request, "auctions/register.html", {
            "genders": genders
        })


def detailed_listing(request, listing_id, message=None, comment_error=None):
    listing = Auction.objects.get(pk=listing_id)
    higher_bid = Bid.objects.filter(auction_id=listing_id).order_by("-amount")[0]
    comments = Comment.objects.filter(auction_id=listing_id).order_by("timestamp")

    return render(request, "auctions/detailed-listing.html", {
        "listing": listing,
        "is_author": listing.author.id == request.user.id,
        "on_watchlist": len(listing.watchlist.filter(id=request.user.id)) == 1,
        "higher_bid": higher_bid,
        "message": message,
        "comments": comments,
        "comment_error": comment_error
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

        listing = Auction.objects.get(pk=listing_id)
        bid_author = User.objects.get(pk=request.user.id)

        response = verify_bid(bid_amount, higher_bid.amount, listing, bid_author)
        if not response["success"]:
            return HttpResponseRedirect(reverse("see listing", args=[listing_id, response["message"]]))

        create_bid(listing, bid_author, bid_amount)
        return HttpResponseRedirect(reverse("see listing", args=[listing_id]))


@login_required
def add_watchlist(request, listing_id):
    listing = Auction.objects.get(pk=listing_id)
    listing.watchlist.add(User.objects.get(pk= request.user.id))

    return HttpResponseRedirect(reverse("see listing", args=[listing_id]))


@login_required
def remove_watchlist(request, listing_id):
    listing = Auction.objects.get(pk=listing_id)
    listing.watchlist.remove(User.objects.get(pk=request.user.id))

    return HttpResponseRedirect(reverse("see listing", args=[listing_id]))


@login_required
def close_auction(request, listing_id):
    listing = Auction.objects.get(pk=listing_id)
    higher_bid = Bid.objects.filter(auction_id=listing_id).order_by("-amount")[0]
    
    listing.status = 1
    listing.winner = higher_bid.author
    listing.save()

    return HttpResponseRedirect(reverse("see listing", args=[listing_id]))

@login_required
def comment(request, listing_id):
    body = request.POST["body"]
    image = request.FILES["image"] if "image" in request.FILES else None
    
    response = verify_comment(body, image)

    if not response["success"]:
        return HttpResponseRedirect(reverse("see listing", args=[listing_id, response["message"], 1]))
    
    auction = Auction.objects.get(pk=listing_id)
    author = User.objects.get(pk=request.user.id)

    create_comment(body, image, auction, author)
    return HttpResponseRedirect(reverse("see listing", args=[listing_id]))
    

@login_required
def like(request, listing_id):
    ...

@login_required
def watchlist(request):
    user = User.objects.get(pk=request.user.id)
    watched_listings = user.watched_listings.all()

    return render(request, "auctions/watchlist.html", {
        "listings": watched_listings,
        "options": options
    })