from django.urls import path, include
from users import views as users_views

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup', users_views.SignUpView.as_view(), name='signup'),
    path('saved', users_views.saved, name='saved'),
    path('users/<str:username>/', users_views.profile, name='profile'),
    path('hosting/listings', users_views.listings, name='listings'),
]