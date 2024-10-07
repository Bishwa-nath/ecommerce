from django.urls import path
from django.contrib import admin
from . import views
from django.contrib.auth import views as auth_view
from .forms import LoginForm, MyPasswordResetForm, MyPasswordChangeForm, MySetPasswordForm


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('category/<slug:val>', views.CategoryView.as_view(), name='category'),
    path('category-title/<val>', views.CategoryTitleView.as_view(), name='category-title'),
    path('product-detail/<str:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('update-address/<int:pk>', views.UpdateAddress.as_view(), name='update-address'),
    path('logout/', views.logout_user, name='logout'),

    path("add-to-cart/", views.add_to_cart, name="add-to-cart"),
    path("showcart/", views.show_cart, name="showcart"),
    path("checkout/", views.CheckoutView.as_view(), name="checkout"),
    path("paymentdone/", views.payment_done, name="paymentdone"),
    path("orders/", views.orders, name="orders"),
    path("wishlist/", views.wishlist, name="wish-list"),
    path("search/", views.search, name="search"),

    path('pluscart/', views.plus_cart),
    path('minuscart/', views.minus_cart),
    path('removecart/', views.remove_cart),
    path('pluswishlist/', views.plus_wishlist),
    path('minuswishlist/', views.minus_wishlist),
    
    # Login authentication
    path('customer-registration/', views.CustomerRegistrationView.as_view(), name='customer-registration'),
    path('accounts/login/', auth_view.LoginView.as_view(template_name="app/login.html", authentication_form=LoginForm), name='login'),
    path('passwordchange/', auth_view.PasswordChangeView.as_view(template_name="app/passwordchange.html", form_class=MyPasswordChangeForm, success_url="/passwordchangedone"), name="passwordchange"),
    path('passwordchangedone/', auth_view.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html'),  name='passwordchangedone'),

    # Password Reset
    path('password-reset/', auth_view.PasswordResetView.as_view(template_name='app/password_reset.html', form_class=MyPasswordResetForm), name='password_reset'),
    path('password-reset/done/', auth_view.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'), name='password_reset_done'),
    path('password-reset/confirm/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html',form_class=MySetPasswordForm), name='password_reset_confirm'),
    path('password-reset/complete/', auth_view.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'), name='password_reset_complete'),
]


admin.site.site_header = "Dairy Product Crop"
admin.site.site_title = "Dairy Product Crop"
admin.site.site_index_title = "Welcome to Dairy Product Crop"