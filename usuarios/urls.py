from django.urls import path
from usuarios.views import login_ssr
from usuarios.views import logout_ssr

urlpatterns = [
    path('', login_ssr, name='login_ssr'),
    path('logout/', logout_ssr, name='logout_ssr'),

]
