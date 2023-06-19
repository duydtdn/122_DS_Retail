from django.contrib import admin

from orders.models import Cart, Pay, Notification, GiftCode, Product, ProductMedia, ProductCategory, DiscountPackage,Table,OrderPlace,OrderPlaceProduct,CustomUser

# Register your models here.

admin.site.register(
    Product,
    list_display=['id', 'title', 'price', 'discount', 'is_show_main_media', 'is_show_list_media'],
    list_display_links=['id', 'title'],
)

admin.site.register(
    ProductCategory,
    list_display=['id', 'name', 'slug', 'parent'],
    list_display_links=['id', 'name'],
)

admin.site.register(
    ProductMedia,
    list_display=['id', 'product', 'file_list_view', 'is_video', 'is_active'],
    list_display_links=['id', 'product'],
    fields=['product', 'file_detail_view', 'media_path', 'is_video', 'is_active'],
    readonly_fields=['file_list_view', 'file_detail_view'],
    list_filter=['product', ],
)

admin.site.register(
    Cart,
    list_display=['id', 'user', 'product', 'quantity'],
    list_display_links=['id', 'user', 'product'],
)

admin.site.register(
    Pay,
    list_display=['id', 'user', 'product', 'quantity', 'date_begin', 'date_finish', 'status', 'price'],
    list_display_links=['id', 'user', 'product'],
)


admin.site.register(
    Notification,
    list_display=['id', 'user', 'category', 'sender', 'message'],
    list_display_links=['id', 'user', 'category'],
)


admin.site.register(
    GiftCode,
    list_display=['id', 'group', 'rule'],
    list_display_links=['id', 'group'],
)
admin.site.register(
    DiscountPackage,
    list_display=['id', 'title', 'discount', 'amount', 'is_active',],
    list_display_links=['id', 'title'],
)
admin.site.register(
    Table,
    list_display=['id', 'name', 'number_of_chair' , 'is_available'],
    list_display_links=['id', 'name'],
)
admin.site.register(
    OrderPlace,
    list_display=['id', 'discount', 'table', 'is_pay', 'time'],
    list_display_links=['id', 'table'],
)
admin.site.register(
    OrderPlaceProduct,
    list_display=['id', 'order_place_id', 'product', 'amount'],
    list_display_links=['id', 'order_place_id'],
)

admin.site.register(CustomUser,
  list_display=['id', 'phone_number'])