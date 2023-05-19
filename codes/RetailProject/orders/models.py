# Create your models here.
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from django.utils.safestring import mark_safe
from PIL import Image
from datetime import datetime
from mptt.models import MPTTModel, TreeForeignKey


# from SiiOn.controller.libs.file_folder_ast import delete_file


# Create your models here.

class ProductCategory(MPTTModel):
    name = models.CharField(verbose_name='Thể loại', max_length=150, db_index=True)
    slug = models.SlugField(max_length=150, unique=True ,db_index=True)
    # parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True,on_delete=models.CASCADE)
    # thu_tu = models.IntegerField(default=0)
    class MPTTMeta:
        # level_attr = 'mptt_level'
        order_insertion_by = ['parent']

    class Meta:
        unique_together = (('parent', 'slug',))
        verbose_name_plural = 'Quản lý Category'

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
    title = models.CharField(max_length=512, null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    discount = models.FloatField(null=True, blank=True)
    detail = RichTextField(null=True, blank=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
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


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True, blank=True)


class Pay(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    date_begin = models.DateTimeField(auto_created=True)
    date_finish = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=32, null=True, blank=True)


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(null=True, blank=True)
    category = models.CharField(max_length=32, null=True, blank=True)
    sender = models.CharField(max_length=32, null=True, blank=True)


class GiftCode(models.Model):
    group = models.CharField(max_length=32, null=True, blank=True)
    rule = models.TextField(null=True, blank=True)

class DiscountPackage(models.Model):
    title = models.CharField(max_length=512, null=True, blank=True)
    discount = models.IntegerField(null=True, blank=True)
    detail = models.TextField(null=True, blank=True)
    amount = models.IntegerField(null=True, blank=True)
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
