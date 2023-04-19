from django.urls import path
from . import views

urlpatterns = [
    # path('', views.index),
    path('', views.PostList.as_view()),
    # path('<int:post_num>/', views.single_post_page)
    path('<int:pk>/', views.PostDetail.as_view()),
    path('category/<str:slug>', views.categories_page),
    path('tag/<str:slug>', views.tag_page),
    path('create_post/', views.PostCreate.as_view()),
    path('update_post/<int:pk>/', views.PostUpdate.as_view()),
    path('<int:pk>/add_comment/', views.add_comment),
]
