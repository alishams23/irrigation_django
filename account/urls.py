from django.contrib import admin
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import *
from . import seller_views
from . import admin_views

app_name = "account"
AUTH_USER_MODEL = "account.User"

urlpatterns = [
        path('login/',obtain_auth_token,name="login"),
        path('notification-list/', NotificationList.as_view(), ),
        path('login-sms/', LoginSms.as_view(), ),
        path('code_check/', CodeCheck.as_view(), ),
        path('user-settings-retrieve/<str:username>/', UserSettingsRetrieve.as_view(), ),
        path('user-settings-update/<str:username>/', UserSettingsUpdate.as_view(), ),
        path('sign-up-sms/', SignUpSms.as_view(), ),
        path('code-check-sign-up/', CodeCheckSignUp.as_view(), ),
        path('user-profile/<str:username>/', user_profile, ),
    
]

seller_panel_urls = [
        path('seller-panel/change-username-shop/', seller_views.ChangeUsernameShopView.as_view(), ),
        path('seller-panel/code-check/', seller_views.CodeCheckAdmin.as_view(), ),
        path('seller-panel/verify-shop-retrieve-update/<int:pk>/',seller_views.VerifyShopRetrieveUpdateApi.as_view(), ),
        path('seller-panel/verify-shop-create/',seller_views.VerifyShopCreateAdminApi.as_view(), ),
        path('seller-panel/verify-shop-list/',seller_views.VerifyShopListAdminApi.as_view(), ),
        path('seller-panel/terms-list-api/', seller_views.TermsListApi.as_view(),name="TermsListApi"),
        path('seller-panel/zarinpal-merchant-list/', seller_views.ZarinPalMerchantListApi.as_view()),
        path('seller-panel/zarinpal-merchant-update/<int:pk>/', seller_views.ZarinPalMerchantUpdateApi.as_view()),
]





urlpatterns += seller_panel_urls
