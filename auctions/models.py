from django.contrib.auth.models import AbstractUser
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.utils import timezone
import os

class User(AbstractUser):
    cellphone_number = models.CharField(max_length=20)
    gender = models.CharField(max_length=20)
    birthday = models.DateField(default=timezone.now)

class Auction(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=500)
    cover = models.ImageField(upload_to="covers/")
    initial_bid = models.DecimalField(decimal_places=2, max_digits=11)
    category = models.CharField(max_length=64)
    status = models.IntegerField(default=0)
    timestamp = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="won_auctions", null=True, blank=True)
    watchlist = models.ManyToManyField(User, related_name="watched_listings", null=True, blank=True)

    @property
    def cover_filename(self):
        return os.path.basename(self.cover.filename)


class Bid(models.Model):
    amount = models.DecimalField(decimal_places=2, max_digits=11)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="bid_list")


class Comment(models.Model):
    body = models.CharField(max_length=500)
    image = models.ImageField(upload_to="comments/", null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    timestamp = models.DateTimeField(default=timezone.now)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="comment_list")
    likes = models.ManyToManyField(User, related_name="liked_posts", null=True, blank=True)


