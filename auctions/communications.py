from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect

def create_listing(title, initial_bid, category, cover, body):
    if len(title) < 10 or len(title) > 64:
        return {
            "success": False, 
            "message": "The title must have a minimum of 10 characters and a amximum of 64"
            }
    
    if initial_bid < 0 or initial_bid > 99999999999.99:
        return {
            "success": False, 
            "message": "The title must have a minimum of 10 characters and a amximum of 64"
            }
    