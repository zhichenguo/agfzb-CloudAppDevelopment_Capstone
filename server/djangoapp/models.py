from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    uid = models.AutoField(
        primary_key=True,
        editable=False,
        unique=True,
        verbose_name="Car Unique ID",
    )
    name =  models.CharField(
        null=False,
        max_length=256,
    )
    description = models.CharField(
        null=False,
        max_length=1024,
    )

    def __str__(self):
        return self.name


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    uid = models.AutoField(
        primary_key=True,
        editable=False,
        unique=True,
        verbose_name="Car Unique ID",
    )
    car_make = models.ForeignKey(
        CarMake,
        on_delete=models.CASCADE,
    )
    name =  models.CharField(
        null=False,
        max_length=255,
    )
    dealer_id = models.IntegerField()
    type = models.CharField(
        null=False,
        max_length=20,
        choices=[
            ('sedan', 'Sedan'),
            ('suv', 'SUV'),
            ('wagon', 'WAGON'),
            ('pickup truck', 'Pickup Truck')
        ]
    )
    year = models.DateField(null=True)

    def __str__(self):
        return self.name


# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:

    def __init__(self, address, city, state, st, full_name, id, lat, long, short_name, zip):
        # Dealer id
        self.id = id
        # Dealer city
        self.city = city
        # Dealer state
        self.state = state
        # Dealer state short
        self.st = st
        # Dealer address
        self.address = address
        # Dealer zip
        self.zip = zip
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer Full Name
        self.full_name = full_name

    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:

    def __init__(self, dealership, name, purchase, review, purchase_date, car_make, car_model, car_year, sentiment, id):
        # Review dealership
        self.dealership = dealership
        # Review name
        self.name = name
        # Review purchase
        self.purchase = purchase
        # Review
        self.review = review
        # Review purchase_date
        self.purchase_date = purchase_date
        # Review car_make
        self.car_make = car_make
        # Review car_model
        self.car_model = car_model
        # Review car_year
        self.car_year = car_year
        # Review sentiment
        self.sentiment = sentiment
        # Review id
        self.id = id

    def __str__(self):
        return "Review name: " + self.name
