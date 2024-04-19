from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from .utils import options, valid_image_extensions
from .models import Auction, Bid, User
from validator_collection import checkers

def check_title(title):
    return len(title) < 10 or len(title) > 64 or title.isspace()


def check_description(description):
    return len(description) < 30 or len(description) > 500 or description.isspace()


def check_initial_bid(initial_bid):
    return initial_bid < 0 or initial_bid > 99999999999.99


def check_category(category):
    return not category in options


def check_image(cover):
    for extension in valid_image_extensions:
        if cover.name.endswith(extension):
            return False
    
    return True


def check_amount(amount, higher_amount):
    return amount < higher_amount


def check_author(listing, bid_author):
    return listing.author.id == bid_author.id


def check_body(body):
    return len(body) < 1 or len(body) > 500 or body.isspace()


def verify_listing(title, description, initial_bid, category, cover):
    if check_title(title):
        return {
            "success": False, 
            "message": "The title must have a between 10 and 64 characters."
            }
    
    if check_initial_bid(initial_bid):
        return {
            "success": False, 
            "message": "The initial bid must be greater than $0 and less than $99999999999.99"
            }
    
    if check_category(category):
        return {
            "success": False, 
            "message": "Invalid category"
            }
    
    if check_image(cover):
        return {
            "success": False, 
            "message": "Invalid image file. It must end with either '.png', '.jpg' or '.jpeg'."
        }
    
    if check_description(description):
        return {
            "success": False, 
            "message": "The description field must have between 30 and 500 characters."
        }
    
    return {
        "success": True, 
        "message": "The listing has been succesfully created."
    }
    

def verify_bid(amount, higher_amount, listing, author):
    if check_amount(amount, higher_amount):
        return {
            "success": False, 
            "message": "The bid amount must be higher than the current highest bid."
        }

    if check_author:
        return {
            "success": False, 
            "message": "The author of the listing cannot bid."
        }
    
    return {
        "success": True, 
        "message": "The bid has been succesfully placed."
    }

def verify_comment(body, image):
    if check_body(body):
        return {
            "success": False,
            "message": "The comment body must have a between 1 and 500 characters."
        }
    
    if image:
        if check_image(image):
            return {
                "success": False,
                "message": "Invalid image file. It must end with either '.png', '.jpg' or '.jpeg'."
            }
    
    return {
        "success": True, 
        "message": "The comment has been succesfully posted."
    }

def verify_user(first_name, last_name, birthday, gender, cellphone_number, email, username, password, confirmation):
    ...