from django.urls import path
from .views import InvitadoListView, InvitadoDetailView

urlpatterns = [
     path('', InvitadoListView.as_view()),
     path('<pk>', InvitadoDetailView.as_view())
]
