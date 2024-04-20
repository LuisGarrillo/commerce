from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from .utils import options, valid_image_extensions, genders
from .models import Auction, Bid, User
from validator_collection import checkers

import re, datetime

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

def check_birthday(date):
    print(date)

def check_name(name):
    return len(name) < 1 or name.isspace() or not re.match("^[a-zA-Z0-9.,'& ]+$", name)

def check_username(username):
    return len(username) < 4 or username.isspace() or not re.match("^[a-zA-Z0-9.,'& ]+$", username)

def check_password(password):
    return len(password) < 8

def check_gender(gender):
    return not gender in genders 

def check_cellphone_number(number):
    return not re.match("^([\+\(]?[0-9]{1,3}\)?)?([ -.]?[0-9]{3}){1,2}([ -.]?[0-9]{4})$", number)

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
    check_birthday(birthday)
    if check_name(first_name):
        return {
            "success": False, 
            "message": "Enter a valid first name."
        }
    
    if check_name(last_name):
        return {
            "success": False, 
            "message": "Enter a valid last name."
        }
    
    if not checkers.is_date(birthday):
        return {
            "success": False, 
            "message": "Enter a valid birthday."
        }
    
    if check_gender(gender):
        return {
            "success": False, 
            "message": "Select a valid gender."
        }
    
    if check_cellphone_number(cellphone_number):
        return {
            "success": False, 
            "message": "Enter a valid cellphone number."
        }
    
    if not checkers.is_email(email):
        return {
            "success": False, 
            "message": "Enter a valid last name."
        }
    
    if check_username(username):
        return {
            "success": False, 
            "message": "The username must have at least 4 characters."
        }
    
    if check_password(password):
        return {
            "success": False, 
            "message": "The password must have at least 8 characters."
        }
    
    if not password == confirmation:
        return {
            "success": False, 
            "message": "The passwords must match."
        }
    
    return {
            "success": True, 
            "message": "The User has been succesfully created"
        } 