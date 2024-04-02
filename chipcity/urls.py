from django.urls import path
from chipcity import views

app_name = "ChipCity"

urlpatterns = [
    path('', views.onLoad, name='onLoad'),
    path('splash', views.splash_action, name='splash'),
    path('join', views.join_action, name='join'),
    path('table', views.table_action, name='table'),
    # path('register', views.register_action, name='register'),
    # path('followers', views.followers_action, name='followers'),
    # path('logout', views.logout_action, name='logout'),
    # path('myprofile', views.myprofile_action, name='myprofile'),
    # path('otherprofile/<int:user_id>', views.otherprofile_action, name='otherprofile'),
    # path('photo/<int:id>', views.get_photo, name='photo'),
    # path('follow/<int:user_id>', views.follow, name='follow'),
    # path('unfollow/<int:user_id>', views.unfollow, name='unfollow'),
    # path('get-global', views.get_global, name = 'get-global'),
    # path('add-comment', views.add_comment, name = 'add-comment'),
    # path('get-follower', views.get_follower, name = 'get-follower')
]