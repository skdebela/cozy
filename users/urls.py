from django.urls import path, include
from users import views as users_views

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup', users_views.SignUpView.as_view(), name='signup'),
]