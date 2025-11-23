from django.urls import path
from .views import PredictIntentView

urlpatterns = [
    path('predict/', PredictIntentView.as_view(), name='predict_intent'),
]