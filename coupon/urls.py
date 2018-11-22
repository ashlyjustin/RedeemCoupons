from django.urls import include, path

from django.conf.urls import url,include

from coupon import views

app_name='coupon'

urlpatterns = [
    
    path('', include('django.contrib.auth.urls')),
    # path('signup/', views.SignUpView.as_view(), name='signup'),
    
    path('signup/generator/', views.GeneratorSignupView.as_view(), name='generator_signup'),
    path('signup/validator/', views.ValidatorSignupView.as_view(), name='validator_signup'),
    url(r"^cafes/new/$", views.CreateCafe.as_view(), name="createCafe"),
    url(r"^coupons/by/(?P<username>[-\w]+)/$",views.CouponList.as_view(),name="couponList"),
    url(r"^cafes/of/(?P<cafeName>[a-zA-Z0-9_ ]+)/(?P<pk>\d+)/$",views.CafeDetail.as_view(),name="cafe_detail"),
    url(r"^cafes/$",views.CafeList.as_view(),name="cafe_list"),
    url(r"^cafes/send", views.CreateCoupon.as_view(), name="create_coupon"),
    url(r"^coupons/$",views.RedeemView.as_view(),name='redeem'),
    url(r'^coupons/validate',views.validation,name="validate"),
    url(r'^coupons/$',views.check_coupon,name='check_coupon')
]