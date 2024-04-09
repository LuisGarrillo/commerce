from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from .utils import options, valid_image_extensions

def check_title(title):
    return len(title) < 10 or len(title) > 64


def check_initial_bid(initial_bid):
    return initial_bid < 0 or initial_bid > 99999999999.99


def check_category(category):
    return not category in options


def check_cover(cover):
    for extension in valid_image_extensions:
        if cover.endswith(extension):
            return False
    
    return True


def check_body(body):
    return len(body) < 30 or len(body) > 500


def verify_listing(title, initial_bid, category, cover, body):
    if check_title(title):
        return {
            "success": False, 
            "message": "The title must have a minimum of 10 characters and a amximum of 64"
            }
    
    if check_initial_bid(initial_bid):
        return {
            "success": False, 
            "message": "The title field must have between 10 and 64 characters."
            }
    
    if check_category(category):
        return {
            "success": False, 
            "message": "Invalid category"
            }
    
    if check_cover(cover):
        return {
            "success": False, 
            "message": "Invalid image file. It must end with either '.png', '.jpg' or '.jpeg'."
        }
    
    if check_body(body):
        return {
            "success": False, 
            "message": "The body field must have between 30 and 500 characters."
        }
    
    return {
        "success": True, 
        "message": "The listing has been succesfully created."
    }
    
    