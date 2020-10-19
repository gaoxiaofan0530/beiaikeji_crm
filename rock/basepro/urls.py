from django.views import static
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, re_path,include
# from app import views
# from app import viewss
from django.urls import include, path
from rest_framework import routers
from user import views
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from user.views import MyTokenObtainPairView
from django.views.generic.base import TemplateView
router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
from django.views.static import serve
from .settings import MEDIA_ROOT

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('app/',include('app.urls')),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('user/login', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('user/info',views.get_user_info),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    url(r'^media/(?P<path>.*)$',serve,{"document_root":MEDIA_ROOT}),
]