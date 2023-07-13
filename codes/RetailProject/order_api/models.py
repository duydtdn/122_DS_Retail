# Create your models here.
from ckeditor.fields import RichTextField
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.safestring import mark_safe
from PIL import Image
from datetime import datetime
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import phonenumbers

# from SiiOn.controller.libs.file_folder_ast import delete_file


# Create your models here.
class Store(models.Model):
    name = models.CharField(max_length=512, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    description =  models.CharField(max_length=512, null=True, blank=True)
    location =  models.CharField(max_length=512, null=True, blank=True)
    created_date   = models.DateTimeField(auto_created=True)
    def thumbnail_directory_path(Client, filename):
        dirname = datetime.now().strftime('%Y.%m.%d.%H.%M.%S')
        return 'uploads/order-app/{0}/store/{1}'.format(dirname, filename)

    thumbnail = models.FileField(upload_to=thumbnail_directory_path, verbose_name="Hình ảnh",
                              default='', null=True)
    def __str__(self):
        return f'{self.name}'
    
    def save(self, force_insert=False, force_update=False):
        size = 300, 300
        super(Store, self).save(force_insert, force_update)
        if self.id is not None:
            if self.thumbnail:
                try:
                    image = Image.open(self.thumbnail.name)
                    # image = image.resize((100, 100), Image.ANTIALIAS)
                    image.thumbnail(size, Image.ANTIALIAS)
                    image.save(self.thumbnail.name)
                except IOError:
                    print("Co loi trong qua trinh resize")


class MyUserManager(BaseUserManager):
    def create_user(self, username,phone_number=None, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not username:
            raise ValueError("Users must have an username")

        user = self.model(
            username=username,
            phone_number=phone_number
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, username, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            username=username,
        )
        user.is_active=True
        user.is_admin=True
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, password=None):
        """
        creates a superuser with email and password
        """
        user = self.create_user(
            username=username,
        )
        user.is_active=True
        user.is_admin=True
        user.set_password(password)
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
    ROLES_CHOICES = [
        ('store_manager', 'Store Manager'),
        ('customer', 'Customer'),
        ('employee', 'Employee'),
    ]
    class Meta:
        verbose_name_plural = 'Custom User'

    username = models.CharField(max_length=20, unique=True,null=False, blank=False )
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    role = models.CharField(max_length=20, choices=ROLES_CHOICES, default='customer')
    store_operate = models.ForeignKey(Store, on_delete=models.CASCADE, null=True, blank=True)
    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS = ["phone_number"]

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        # "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        # "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        """Is the user a staff member"""
        return self.is_admin
    
    def save(self, *args, **kwargs):
        # Validate and normalize the phone number before saving
        # parsed_number = phonenumbers.parse(self.phone_number, None)
        # if not phonenumbers.is_valid_number(parsed_number):
        #     raise ValueError("Invalid phone number")
        # self.phone_number = phonenumbers.format_number(
        #     parsed_number, phonenumbers.PhoneNumberFormat.E164
        # )
        super().save(*args, **kwargs)


class ProductCategory(MPTTModel):
    name = models.CharField(verbose_name='Product category', max_length=150, db_index=True)
    slug = models.SlugField(max_length=150, unique=True ,db_index=True)
    # parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True,on_delete=models.CASCADE)
    store_operate = models.ForeignKey(Store, on_delete=models.CASCADE, null=True, blank=True)

    class MPTTMeta:
        # level_attr = 'mptt_level'
        order_insertion_by = ['parent']

    class Meta:
        unique_together = (('parent', 'slug',))
        verbose_name_plural = 'Product Category'

    def get_slug_list(self):
        try:
            ancestors = self.get_ancestors(include_self=True)
        except:
            ancestors = []
        else:
            ancestors = [i.slug for i in ancestors]
        slugs = []
        for i in range(len(ancestors)):
            slugs.append('/'.join(ancestors[:i + 1]))
        return slugs

    def __unicode__(self):
        return '%s' % self.name
    def __str__(self):
        return self.name
class Product(models.Model):
    title = models.CharField(max_length=512, null=False, blank=False)
    store_operate = models.ForeignKey(Store, on_delete=models.CASCADE, null=False, blank=False)
    price = models.FloatField(null=False, blank=False)
    discount = models.FloatField(null=True, blank=True)
    detail = models.CharField(max_length=512, null=True, blank=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, null=False, blank=False)
    is_active= models.BooleanField(default=True)
    is_show_main_media = models.BooleanField(default=False)
    is_show_list_media = models.BooleanField(default=False)
    def thumbnail_directory_path(Client, filename):
        dirname = datetime.now().strftime('%Y.%m.%d.%H.%M.%S')
        return 'uploads/order-app/{0}/product/{1}'.format(dirname, filename)

    thumbnail = models.FileField(upload_to=thumbnail_directory_path, verbose_name="Hình ảnh",
                              default='', null=True)
    def __str__(self):
        return f'{self.title}'
    
    def save(self, force_insert=False, force_update=False):
        size = 300, 300
        super(Product, self).save(force_insert, force_update)
        if self.id is not None:
            # previous = Destination.objects.get(id=self.id)
            # if self.avatar and self.avatar != previous.avatar:
            if self.thumbnail:
                try:
                    image = Image.open(self.thumbnail.name)
                    # image = image.resize((100, 100), Image.ANTIALIAS)
                    image.thumbnail(size, Image.ANTIALIAS)
                    image.save(self.thumbnail.name)
                except IOError:
                    print("Co loi trong qua trinh resize")


class ProductMedia(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    media_path = models.FileField(upload_to='uploads/%y/%m/%d')
    is_video = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'Media {self.id} : {self.product}'

    def file_list_view(self):
        content_width = 82
        if self.is_video:
            return mark_safe(f"""<video height="{content_width}" controls>
                                <source src="/media/{self.media_path}" type="video/mp4">
                            </video>""")
        else:
            return mark_safe(f'<img src="/media/{self.media_path}" height="{content_width}" />')

    def file_detail_view(self):
        content_width = 282
        if self.is_video:
            return mark_safe(f"""<video height="{content_width}" controls>
                                <source src="/media/{self.media_path}" type="video/mp4">
                            </video>""")
        else:
            return mark_safe(f'<img src="/media/{self.media_path}" height="{content_width}" />')


@receiver(pre_save, sender=ProductMedia)
def update_product_media(sender, instance, **kwargs):
    try:
        old_media_path = ProductMedia.objects.get(id=instance.id).media_path
        new_media_path = instance.media_path

        if old_media_path != new_media_path:
            content_path = f'media/{old_media_path}'
            # delete_file(file_path=content_path)
    except:
        pass


# @receiver(post_delete, sender=ProductMedia)
# def delete_product_media(sender, instance, **kwargs):
#     media_path = f'media/{instance.media_path}'
#     delete_file(file_path=media_path)


# class GiftCode(models.Model):
#     group = models.CharField(max_length=32, null=True, blank=True)
#     rule = models.TextField(null=True, blank=True)

class DiscountPackage(models.Model):
    title = models.CharField(max_length=512, null=True, blank=True)
    gift_code = models.CharField(max_length=10, null=True, blank=True, unique=True, default='')
    store_operate = models.ForeignKey(Store, on_delete=models.CASCADE, null=True, blank=True)
    discount = models.IntegerField(null=True, blank=True)
    detail = models.TextField(null=True, blank=True)
    amount = models.IntegerField(null=False, blank=False, default=0)
    available = models.IntegerField(null=False, blank=False, default=0)
    is_active = models.BooleanField(default=True)
    def thumbnail_directory_path(Client, filename):
        dirname = datetime.now().strftime('%Y.%m.%d.%H.%M.%S')
        return 'uploads/order-app/{0}/discount-package/{1}'.format(dirname, filename)

    thumbnail = models.FileField(upload_to=thumbnail_directory_path, verbose_name="Hình ảnh",
                              default='', null=True)
    def __str__(self):
        return f'{self.title}'
    
    def save(self, force_insert=False, force_update=False):
        size = 300, 300
        super(DiscountPackage, self).save(force_insert, force_update)
        if self.id is not None:
            # previous = Destination.objects.get(id=self.id)
            # if self.avatar and self.avatar != previous.avatar:
            if self.thumbnail:
                try:
                    image = Image.open(self.thumbnail.name)
                    # image = image.resize((100, 100), Image.ANTIALIAS)
                    image.thumbnail(size, Image.ANTIALIAS)
                    image.save(self.thumbnail.name)
                except IOError:
                    print("Co loi trong qua trinh resize")


class Table(models.Model):
    name = models.CharField(verbose_name='Table name', max_length=150, db_index=True)
    number_of_chair = models.IntegerField(null=False, blank=False)
    is_available = models.BooleanField(default=True)
    def __str__(self):
        return f'{self.name}'
class OrderType(models.Model):
    name = models.CharField(verbose_name='Table name', max_length=150, db_index=True)
    number_of_chair = models.IntegerField(null=False, blank=False)
    is_available = models.BooleanField(default=True)
    def __str__(self):
        return f'{self.name}'

class OrderPlace(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('serving', 'Serving'),
        ('finished', 'Finished'),
        ('cancelled', 'Cancelled'),
    ]
    ORDER_TYPE_CHOICES= [
        ('onsite', 'On-site Service'),
        ('delivery', 'Delivery'),
    ]
    PAY_TYPE_CHOICES= [
        ('online_pay', 'Online pay'),
        ('ship_cod', 'Ship COD'),
        ('onboard', 'Onboard'),
    ]
    store_operate = models.ForeignKey(Store, on_delete=models.CASCADE, null=True, blank=True)
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    discount = models.ForeignKey(DiscountPackage, on_delete=models.CASCADE, null=True, blank=True)
    # table = models.ForeignKey(Table, on_delete=models.CASCADE, null=True, blank=True, db_constraint=False)
    order_date = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    price = models.DecimalField(max_digits=8, decimal_places=2,null=True, blank=True)
    order_type = models.CharField(max_length=20, choices=ORDER_TYPE_CHOICES, default='onsite')
    pay_type = models.CharField(max_length=20, choices=PAY_TYPE_CHOICES, default='onboard')
    def __str__(self):
        return f'{self.id}'
    def save(self, *args, **kwargs):
        super(OrderPlace, self).save(*args, **kwargs) 
        return self
    
class OrderPlaceProduct(models.Model):
    order_place = models.ForeignKey(OrderPlace,  on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.IntegerField(null=False, blank=False, default=1)
    # price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    note = models.TextField(null=True, blank=True)


# class Cart(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.IntegerField(null=True, blank=True)


# class Pay(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.IntegerField(null=True, blank=True)
#     price = models.FloatField(null=True, blank=True)
#     date_begin = models.DateTimeField(auto_created=True)
#     date_finish = models.DateTimeField(null=True, blank=True)
#     status = models.CharField(max_length=32, null=True, blank=True)


# class Notification(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, db_constraint=False)
#     message = models.TextField(null=True, blank=True)
#     category = models.CharField(max_length=32, null=True, blank=True)
#     sender = models.CharField(max_length=32, null=True, blank=True)
