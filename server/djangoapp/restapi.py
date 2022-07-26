import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions

def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(
            url,
            headers={'Content-Type': 'application/json'},
            params=kwargs
        )
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


def post_request(url, json_payload, **kwargs):
    print(kwargs)
    print("Post from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.post(
            url,
            headers={'Content-Type': 'application/json'},
            params=kwargs,
            json=json_payload
        )
    except:
        # If any error occurs
        print("Network exception occurred")
    
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["entries"]
        # For each dealer object
        for dealer_doc in dealers:
            # # Get its content in `doc` object
            # dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(
                id=dealer_doc.get("id", 0),
                city=dealer_doc.get("city", ""),
                state=dealer_doc.get("state", ""),
                st=dealer_doc.get("st", ""),
                address=dealer_doc.get("address", ""),
                zip=dealer_doc.get("zip", ""),
                lat=dealer_doc.get("lat", 0),
                long=dealer_doc.get("long", 0),
                short_name=dealer_doc.get("short_name", ""),
                full_name=dealer_doc.get("full_name", ""),
            )
            results.append(dealer_obj)

    return results


def get_dealer_reviews_from_cf(url, dealer_id):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as reviews
        reviews = json_result["entries"]
        # filter base on dealership id
        dealership_reviews = filter(lambda d: d['dealership'] == dealer_id, reviews)
        # For each review object
        for review in dealership_reviews:
            # # Get its content in `doc` object
            # dealer_doc = dealer["doc"]
            # Create a DealerReview object with values in `doc` object
            try:
                sentiment_result = analyze_review_sentiments(review["review"])
                if "sentiment" in sentiment_result.keys():
                    sentiment = sentiment_result["sentiment"]["document"]["label"]
                else:
                    sentiment = "neutral"
            except Exception as e:
                sentiment = "neutral"
            
            dealer_obj = DealerReview(
                dealership=review.get("dealership", 0),
                name=review.get("name", ""),
                purchase=review.get("purchase", False),
                review=review.get("review", ""),
                purchase_date=review.get("purchase_date", ""),
                car_make=review.get("car_make", ""),
                car_model=review.get("car_model", ""),
                car_year=review.get("car_year", ""),
                sentiment=sentiment,
                id=review.get("id", 0),
            )
            results.append(dealer_obj)

    return results


def analyze_review_sentiments(review):
    api_key = "0rU2GtDjCfl8HI7tX36v_GtEof0FQkVrGAquQsxCDprh"
    url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/a5e7e617-4e11-45a5-af40-477bcf6cad91"
    
    authenticator = IAMAuthenticator(api_key)
    service = NaturalLanguageUnderstandingV1(
        version='2022-04-07',
        authenticator=authenticator
    )

    service.set_service_url(url)
    response = service.analyze(
        text=review,
        features=Features(
            sentiment=SentimentOptions()
        )
    ).get_result()

    return response