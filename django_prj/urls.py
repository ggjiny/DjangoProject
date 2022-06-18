from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from movie import views
from accounts import views as a_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('detail/<str:movie_id>', views.detail, name="detail"),
    path('review/', include('review.urls')),
    path('genre/<str:genre_id>/<str:genre>', views.detail_genre, name="detail_genre"),
    path('genre/', views.genre, name="genre"),
    path('about/', views.about, name="about"),

    path('login/', a_views.login, name="login"),
    path('logout/', a_views.logout, name="logout"),
    path('signup/', a_views.signup, name="signup"),

    path('markdownx/', include('markdownx.urls')),
    path('accounts/', include('allauth.urls')),
    path('', views.home, name="home"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)