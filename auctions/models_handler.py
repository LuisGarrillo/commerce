from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Auction

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