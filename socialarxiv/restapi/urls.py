from django.urls import path
from restapi import views
from django.urls import path

app_name = 'restapi'

urlpatterns = [
    path('', views.list_papers, name='list_papers'),
    path('tag/<slug:tag_slug>/', views.list_papers, name='list_papers_by_tag'),
    path('<int:id>/', views.paper_detail, name='paper_detail'),
    path('search/', views.post_search, name='post_search'),
    path('<int:paper_id>/comment/', views.paper_comment, name='post_comment'),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('users/', views.user_list, name='user_list'),
]
