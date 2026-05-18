from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import LogAcessoViewSet, RegisterView, MeView, LogoutView, ChangePasswordView

router = DefaultRouter()
router.register(r'log-acesso', LogAcessoViewSet, basename='log-acesso')

urlpatterns = router.urls + [
    path('register/', RegisterView.as_view()),
    path('me/', MeView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('change-password/', ChangePasswordView.as_view()),
]