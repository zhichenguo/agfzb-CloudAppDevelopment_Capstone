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


# <HINT> Create a plain Python class `DealerReview` to hold review data
