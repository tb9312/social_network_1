from django.urls import path
from . import views

urlpatterns = [
    path('', views.signIn,name='signIn'),
    path('signup/',views.signUp,name='signUp'),
    path('homepage/',views.homePage,name='homePage'),
    path('logOut/',views.logOut,name='logOut'),
    path('likePost/',views.likePost,name='likePost'),
    path('likeComment/',views.likeComment,name='likeComment'),
    path('follow/',views.follow,name='follow'),
    path('profile/<str:pk>',views.profile,name='profile'),
    path('edit/',views.editProfile,name='edit'),
    path('search/',views.search,name='search'),
    path('notification/',views.notification,name='notification'),
    path('comment/<str:id>',views.comment,name='comment'),
]

