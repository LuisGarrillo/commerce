from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Auction, Bid, Comment

def create_bid(auction, author, amount):
    bid = Bid(
        amount=amount,
        author=author,
        auction=auction
    )

    bid.save()

def save_auction(title, description, initial_bid, category, cover, author):
    
    auction = Auction(
            title=title, 
            description=description,
            cover=cover,  
            initial_bid=initial_bid, 
            category=category,
            status=0, 
            author= author, 
            winner = None
        )
    
    auction.save()
    create_bid(auction, author, initial_bid)
    
def create_comment(body, image, auction, author):
    comment = Comment(
        body=body,
        image=image,
        auction=auction,
        author=author
    )

    comment.save()