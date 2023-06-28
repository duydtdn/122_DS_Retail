from django.contrib import admin

from orders.models import Product, ProductCategory, DiscountPackage,OrderPlace,OrderPlaceProduct,CustomUser, Store
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from orders.form import  UserChangeForm, UserCreationForm
# Register your models here.

admin.site.register(
    Store,
    list_display=['id', 'name','description', 'location', 'is_active', "created_date"],
    list_display_links=['id', 'name'],
)
admin.site.register(
    Product,
    list_display=['id', 'title', 'price', 'discount', 'is_show_main_media', 'is_show_list_media'],
    list_display_links=['id', 'title'],
)

admin.site.register(
    ProductCategory,
    list_display=['id', 'name', 'slug', 'parent', 'store_operate'],
    list_display_links=['id', 'name'],
)

# admin.site.register(
#     ProductMedia,
#     list_display=['id', 'product', 'file_list_view', 'is_video', 'is_active'],
#     list_display_links=['id', 'product'],
#     fields=['product', 'file_detail_view', 'media_path', 'is_video', 'is_active'],
#     readonly_fields=['file_list_view', 'file_detail_view'],
#     list_filter=['product', ],
# )

# admin.site.register(
#     Pay,
#     list_display=['id', 'user', 'product', 'quantity', 'date_begin', 'date_finish', 'status', 'price'],
#     list_display_links=['id', 'user', 'product'],
# )

admin.site.register(
    DiscountPackage,
    list_display=['id', 'title', 'discount', 'amount', 'is_active', 'store_operate'],
    list_display_links=['id', 'title'],
)

# admin.site.register(
#     Table,
#     list_display=['id', 'name', 'number_of_chair' , 'is_available'],
#     list_display_links=['id', 'name'],
# )

admin.site.register(
    OrderPlace,
    list_display=['id', 'discount', 'order_date','status','price', 'store_operate', 'customer'],
    list_display_links=['id'],
)

admin.site.register(
    OrderPlaceProduct,
    list_display=['id', 'order_place', 'product', 'amount'],
    list_display_links=['id', 'order_place'],
)

# admin.site.register(CustomUser,
#   list_display=['id','username', 'phone_number', 'password'])

class CustomUserAdmin(UserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.

    list_display = ["username", "is_active", "is_admin","phone_number", "role", "store_operate"]
    list_filter = ["is_admin", "is_active", "role"]
    fieldsets = [
        (None, {"fields": ["username"]}),
        ("Personal info", {"fields": ["phone_number"]}),
        ("Permissions", {"fields": ["store_operate", "is_active", "is_admin"]}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["username", "phone_number", "password1", "password2", "store_operate", "role","is_admin", ],
            },
        ),
    ]
    search_fields = ["username", "phone_number"]
    ordering = ["username"]
    filter_horizontal = []

admin.site.register(CustomUser, CustomUserAdmin )
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
# admin.site.unregister(UserAdmin)