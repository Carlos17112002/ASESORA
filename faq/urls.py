from django.urls import path
from .views import  crear_faq_view, faq_view

urlpatterns = [
    path('', faq_view, name='faq_listado'),
    path('crear/', crear_faq_view, name='crear_faq'),
]
