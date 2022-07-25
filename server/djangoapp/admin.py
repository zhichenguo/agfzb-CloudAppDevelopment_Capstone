from django.contrib import admin
from .models import CarMake, CarModel


# Register your models here.

# CarModelInline class
class CarModelInlineInline(admin.TabularInline):
    model = CarModel
    fields = ["name", "dealer_id", "type", "year"]
    can_delete = True
    show_change_link = True


# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    list_display = [
        "uid",
        "car_make",
        "name",
        "dealer_id",
        "type",
        "year",
    ]
    list_filter = ["type"]
    raw_id_fields = ["car_make"]
    search_fields = [
        "uid",
        "car_make__uid",
        "car_make__name",
        "type",
        "name",
    ]

    def get_car_make_name(self, obj):
        return obj.car_make.name

    get_car_make_name.short_description = "car_make"
    get_car_make_name.admin_order_field = "car_make__name"


# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    list_display = [
        "uid",
        "name",
        "description",
    ]
    search_fields = [
        "uid",
        "name",
        "description",
    ]
    inlines = [CarModelInlineInline]


# Register models here
admin.site.register(CarModel, CarModelAdmin)
admin.site.register(CarMake, CarMakeAdmin)