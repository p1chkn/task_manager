from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import TaskViewSet, history_task, user_register


router = DefaultRouter()
router.register('v1/tasks', TaskViewSet)

urlpatterns = [
    path('v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('v1/token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
    path('v1/user/registration/', user_register),
    path('v1/history/<int:task_id>/', history_task),
    path('', include(router.urls)),
]
