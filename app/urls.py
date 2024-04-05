from django.conf.urls.static import static
from django.urls import path
from app.views import *
from GamASSstore import settings

urlpatterns = [
    path('', AppMain.as_view(), name='main_page'),
    path('profile', profile_view, name='profile'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('game/<game_name>/', GamePage.as_view(), name='game'),
    path('sell/', SellGame.as_view(), name='sell'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)