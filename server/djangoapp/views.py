from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

from .restapi import get_dealer_reviews_from_cf, get_dealers_from_cf, post_request
from .models import CarModel

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    return render(request, "djangoapp/about.html")

# Create a `contact` view to return a static contact page
def contact(request):
    return render(request, "djangoapp/contact.html")

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/index.html', context)
    else:
        return render(request, 'djangoapp/index.html', context)


# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                password=password
            )
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "https://01945f64.us-south.apigw.appdomain.cloud/api/dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # # Concat all dealer's short name
        # dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # context["dealer_names"] = dealer_names
        # # Return a list of dealer short name
        # return HttpResponse(dealer_names)
        context["dealership_list"] = dealerships
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        url_review = "https://01945f64.us-south.apigw.appdomain.cloud/api/review"
        url_dealer = "https://01945f64.us-south.apigw.appdomain.cloud/api/dealership"
        # Get reviews from the URL
        reviews = get_dealer_reviews_from_cf(url_review, dealer_id)
        dealerships = get_dealers_from_cf(url_dealer)
        dealer = [d for d in dealerships if d.id == dealer_id]
        # # Concat all review's name
        # review_names = ' '.join([review.name for review in reviews])
        # review_sentiments = ' '.join([review.sentiment for review in reviews])
        # context["review_names"] = review_names
        # context["review_sentiments"] = review_sentiments
        # # Return a list of dealer short name
        # return HttpResponse(review_sentiments)
        context["reviews"] = reviews
        context["dealer"] = dealer[0]
        return render(request, 'djangoapp/dealer_details.html', context)


# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    context = {}
    if request.method == "POST":
        if request.user.is_authenticated:
            review = {}
            review["time"] = datetime.utcnow().isoformat()
            review["name"] = request.user.username
            if "purchasecheck" in request.POST.keys() and request.POST["purchasecheck"] == "on":
                review["purchase"] = True
                if "purchasedate" in request.POST.keys() and request.POST["purchasedate"] != "":
                    review["purchase_date"] = request.POST["purchasedate"]
                if "car" in request.POST.keys() and request.POST["car"] != "" and request.POST["car"].isdigit():
                    car_uid = int(request.POST["car"])
                    car_model = CarModel.objects.get(uid=car_uid)
                    review["car_make"] = car_model.car_make.name
                    review["car_model"] = car_model.name
                    review["car_year"] = car_model.year.strftime("%Y")
            else:
                review["purchase"] = False
            
            if request.POST["content"] == "":
                messages.warning(request, "Please enter the review content.")
                return redirect("djangoapp:add_review", dealer_id=dealer_id)
            else:            
                review["review"] = request.POST["content"]

            review["dealership"] = dealer_id

            url = "https://01945f64.us-south.apigw.appdomain.cloud/api/review"
            response = post_request(url, review)
            if "ok" in response.keys() and response["ok"]:
                messages.success(request, "Thanks for your review")
                return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
            else:
                messages.error(request, "Something went wrong! Please try again.")
                return redirect("djangoapp:add_review", dealer_id=dealer_id)

        else:
            messages.warning(request, "Please login to submit review.")
            return redirect("djangoapp:add_review", dealer_id=dealer_id)
    
    else:
        url_dealer = "https://01945f64.us-south.apigw.appdomain.cloud/api/dealership"
        dealerships = get_dealers_from_cf(url_dealer)
        dealer = [d for d in dealerships if d.id == dealer_id]
        context["dealer"] = dealer[0]
        cars = CarModel.objects.filter(
            dealer_id=dealer_id
        )
        context["cars"] = cars
        return render(request, 'djangoapp/add_review.html', context)
