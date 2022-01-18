from django.urls import path

from .views import logout_user, delete_view, RegisterUser, LoginUser, UserUpdate

urlpatterns = [
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('update/<int:user_pk>', UserUpdate.as_view(), name='update'),
    path('delete/', delete_view, name='delete')
]
