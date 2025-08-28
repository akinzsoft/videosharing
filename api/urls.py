from django.urls import path,include
from .views import addcreator,regcreator,homepg,crlogin,login_user,welcome,profile,profile_api,myvideo,addusercomment,get_comments,searchvideos
from rest_framework.routers import DefaultRouter
from .views import VideoViewSet,watchmv,trending_videos

router = DefaultRouter()
router.register(r'videos', VideoViewSet, basename='video')
urlpatterns = [
    path("apiaddcreator",addcreator,name="addcreator"),
    path("regcreator",regcreator,name="regcreator"),
    path("",homepg,name="homepg"),
    path("crlogin",crlogin,name="crlogin"),
    path("login_creator",login_user,name="login_user"),
    path('welcome', welcome, name='welcome'),
    path('profile', profile, name='profile'),
    path('profile_api', profile_api, name='profile_api'),
    path('myvideo', myvideo, name='myvideo'),
    path('v/', include(router.urls)),
    path('watchmv', watchmv, name='watchmv'),
    path('trending/', trending_videos, name='trending'),
    path('addusercomment/', addusercomment, name='addusercomment'),
    path('get_comments/<str:movieid>/', get_comments, name='get_comments'),
    path('searchvideos', searchvideos, name='searchvideos'),
    
    
    
    
]

