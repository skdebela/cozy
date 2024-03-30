from django.urls import path
from reviews import views as reviews_views
urlpatterns = [
    path('review-destination/<int:destination_id>/<slug:destination_name>', reviews_views.review, name='review'),
]
