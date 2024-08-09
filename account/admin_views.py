
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse

from .models import QueueVerifyShop,ZarinPal,User
import random
import string

def generate_random_username():
    # Generate a random username of length 8
    random_username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return random_username

    # Assuming you have a model named YourModel and you want to redirect to its change page
    # Replace 'YourModel' with the name of your model and 'change' with the appropriate admin URL name
    queue_verify_shop_instance = QueueVerifyShop.objects.get(id=id)
    admin_instance = queue_verify_shop_instance.author
    if  admin_instance.shop == None :
        zarinpal_instance = ZarinPal.objects.create(merchant_id =queue_verify_shop_instance.merchant_zarin )
        zarinpal_instance.save()
        shop_instance = Shop.objects.create(name = queue_verify_shop_instance.name,
                                            zarin_pal =zarinpal_instance,
                                             username = create_unique_username_shop() )
        tomanWalletInstance = TomanWallet()
        tomanWalletInstance.cash = int(0)
        tomanWalletInstance.save()
        shop_instance.toman_wallet = tomanWalletInstance
        shop_instance.admin.add(admin_instance)
        shop_instance.save()
        admin_instance.shop = shop_instance
        admin_instance.status = 's'
        admin_instance.save()
        queue_verify_shop_instance.is_verified = True
        queue_verify_shop_instance.save()

    else :
        return HttpResponse('کاربر از قبل دارای فروشگاه است')

    admin_url = reverse('admin:account_queueverifyshop_changelist')
    return redirect(admin_url)