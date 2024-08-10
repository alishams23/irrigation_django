from django.contrib import admin
from django.urls import reverse
from .models import *
from django.contrib.auth.admin import UserAdmin
from .models import User
# Register your models here.

UserAdmin.fieldsets += (
    ('فیلد های خاص من', {
        "fields": (
            'status',
            'phone_number',
            'special_user',
            'verify_phone',
            'verify_phone_code',
            'count_sms',
            'state',
            'city',
            'street',
            'zipCode',
     
        ),
    }),
)

UserAdmin.list_display += ('is_special_user',)
UserAdmin.list_filter += ('status',)

admin.site.register(User, UserAdmin)



# class NotificationAdmin(admin.ModelAdmin):
#     list_display = ("id","receiver", "createdAdd")
#     search_fields = ("title","id")
    
    


# admin.site.register(Notification, NotificationAdmin)


# class ZarinPalAdmin(admin.ModelAdmin):
#     search_fields = ("merchant_id","id" )
#     list_display = ("id","merchant_id",)




# admin.site.register(ZarinPal, ZarinPalAdmin)

# class QueueSignUpAdmin(admin.ModelAdmin):
#     list_display = ("id",
#                     "phone_number",
#                      "first_name",
#                      "last_name",
#                     )
#     search_fields = ("first_name", "last_name","id")
#     list_filter = ('verify_phone', )

    


# admin.site.register(QueueSignUp, QueueSignUpAdmin)


# class QueueVerifyShopAdmin(admin.ModelAdmin):
#     list_display = ("id",
#                      "author",
#                      "is_verified",
#                      "name",
#                     )
#     readonly_fields = ('confirmed', )
#     search_fields = ("name","id")
#     list_filter = ('is_verified', )


#     def confirmed(self, obj):
#         if obj.id != None :
#             url = reverse('account:confirm_shop_admin_panel', args=(obj.id,))
#             return format_html('<a class="button" href="{}">تایید ثبت نام</a>', url)

    
# admin.site.register(QueueVerifyShop, QueueVerifyShopAdmin)


# # class TermsAdmin(admin.ModelAdmin):
# #     list_display = ("id","title",)
# #     search_fields = ("title","body","id" )



# # admin.site.register(Terms, TermsAdmin)


