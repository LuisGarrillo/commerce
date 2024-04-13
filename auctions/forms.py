from django import forms
from django.db import models
from django.forms import fields

from .models import Auction

class AuctionForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = ["title", "description", "cover", "initial_bid", "category", "author"]