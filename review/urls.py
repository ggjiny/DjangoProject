from django.urls import path
from . import views

urlpatterns = [
    path('', views.ReviewList.as_view()),
    path('<int:pk>/', views.ReviewDetail.as_view()),
    path('category/<str:slug>/', views.show_category_reviews),
    path('tag/<str:slug>/', views.show_tag_reviews),
    path('create_review/', views.ReviewCreate.as_view()),
    path('update_review/<int:pk>/', views.ReviewUpate.as_view()),
    path('<int:pk>/addcomment/', views.add_comment),
]