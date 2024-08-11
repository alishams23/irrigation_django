from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from PIL import Image as ImagePIL
from django.utils.html import format_html

# Create your models here.

class User(AbstractUser):
    STATUS_CHOICES = (("admin", "مدیر چاه"), ("farmer", "کشاورز"))
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="b", verbose_name="وضعیت کاربر")
    special_user = models.DateTimeField(default=timezone.now, verbose_name="کاربر ویژه")
    image = models.ImageField(upload_to='profile/%Y/%m/%d/', verbose_name="عکس پروفایل", blank=True, null=True)
    verify_phone = models.BooleanField(verbose_name="تایید شماره تلفن", blank=True, null=True)
    verify_phone_code = models.BigIntegerField(verbose_name="کد تایید", blank=True, null=True)
    phone_number = models.TextField(verbose_name="شماره تلفن", blank=True, null=True)
    count_sms=models.IntegerField(verbose_name="تعداد پیامک",default=0)
    state = models.TextField(blank=True,null=True,verbose_name="استان")
    city = models.TextField(blank=True,null=True,verbose_name="شهر")
    street = models.TextField(blank=True,null=True,verbose_name="خیابان")
    zipCode = models.TextField(blank=True,null=True,verbose_name="کد پستی")
    last_login_time = models.DateTimeField(auto_now_add=True,verbose_name="زمان اخرین لاگین ")
    sms_schedules = models.IntegerField(default="1440",verbose_name="زمان یاد آوری")

    def is_special_user(self):
            if self.special_user > timezone.now():
                return True
            else:
                return False

    is_special_user.boolean = True
    is_special_user.short_description = 'کاربر ویژه'


    def save(self, *args, **kwargs):
        try:
            super().save(*args, **kwargs)
            img = ImagePIL.open(self.image.path)
            if img.height > 500:
                img.thumbnail((500, 500))
                img.save(self.image.path)
        except:
            pass
    def picture_show(self):
        try:
            data = format_html("<img src='{}' width=100 style='border-radius : 10px;' >".format(self.image.url))
        except:
            data="null"
        return data
    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"
    
        
    
class QueueSignUp(models.Model):
    phone_number = models.TextField(verbose_name="شماره تلفن")
    verify_phone = models.BooleanField(verbose_name="تایید شماره تلفن", blank=True, null=True)
    verify_phone_code = models.BigIntegerField(verbose_name="کد تایید", blank=True, null=True)
    count_sms=models.IntegerField(verbose_name="تعداد پیامک",default=0)
    first_name = models.TextField(verbose_name="نام")
    last_name = models.TextField(verbose_name="نام خانوادگی")
    email = email = models.EmailField(verbose_name="ایمیل", blank=True,null=True)
    last_sign_up_time = models.DateTimeField(auto_now_add=True,verbose_name="زمات اخرین تلاش برای ثبت نام")

    class Meta:
        verbose_name = "صف تایید ثبت نام "
        verbose_name_plural = "صف های تایید ثبت نام "


        
    
    
class QueueVerifyShop(models.Model):
    name = models.TextField(verbose_name="نام فروشگاه")
    image_national_card = models.ImageField(upload_to='imageNationalCard/%Y/%m/%d/', verbose_name="عکس کارت ملی",)
    selfie_with_national_card = models.FileField(upload_to='ًSelfieWithNationalCard/%Y/%m/%d/', verbose_name="عکس کارت ملی با سلفی",)
    shop_card = models.FileField(upload_to='shop_card/%Y/%m/%d/', verbose_name="عکس کارت مغاره",blank=True)
    merchant_zarin = models.TextField(verbose_name="مرچنت ایدی زرین پال")
    author  = models.ForeignKey(User,blank = True,null=True,on_delete=models.CASCADE,verbose_name="نویسنده")
    is_verified = models.BooleanField(default = False,verbose_name="تایید شده")

    def __str__(self):
        return f"{self.name} -- {self.id} "
    class Meta:
        verbose_name = "صف تایید ثبت نام فروشگاه"
        verbose_name_plural = "صف های تایید ثبت نام فروشگاه"


        
    
class Terms(models.Model):
    created_at = models.DateField(auto_now_add=True,verbose_name="زمان ساخته شده")
    position = models.IntegerField(
        verbose_name="پوزیشن", blank=True, null=True,)
    title = models.CharField(max_length=200, verbose_name="موضوع")
    body = models.TextField(verbose_name="متن")

    class Meta:
        verbose_name = "قانون"
        verbose_name_plural = "قوانین"
        ordering = ["position"]

    def __str__(self):
        return self.title


class ZarinPal(models.Model):
    merchant_id = models.TextField()

    class Meta:
        verbose_name = "زرین پال "
        verbose_name_plural = "زرین پال "




class Notification(models.Model):
    createdAdd = models.DateField(auto_now_add=True,verbose_name="زمان ساخته شده")
    receiver = models.ForeignKey(User, verbose_name="گیرنده", on_delete=models.SET_NULL, null=True,
                               related_name="authorNotification")
    title = models.TextField(verbose_name="تیتر", blank=True, null=True)
    body = models.TextField(verbose_name="متن", blank=True, null=True)
    user = models.ForeignKey(User, verbose_name="یوزر", on_delete=models.SET_NULL, null=True,
                             related_name="userNotification")
    readingStatus = models.BooleanField(default=False, verbose_name="وضعیت خواندن")
    url = models.TextField(verbose_name="آدرس", blank=True, null=True)

    class Meta:
        verbose_name = "نوتیفیکیشن"
        verbose_name_plural = "نوتیفیکیشن ها"
        ordering = ["-createdAdd"]

    def __str__(self):
        return self.title



