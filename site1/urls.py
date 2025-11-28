from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from qalampir import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/news/', views.NewsList.as_view(), name='news-list'),
    path('api/news/<slug:slug>/', views.NewsDetailView.as_view(), name='news-detail'),
    path('api/categories/', views.CategoryListCreateView.as_view(), name='category-list'),
    path('api/categories/<slug:slug>/', views.CategoryNewsView.as_view(), name='category-news'),
    path('api/latest-news/', views.LatestNewsByCategoryView.as_view(), name='latest-news-by-category'),
    path('api/news-search/', views.NewsSearchView.as_view(), name='news-search'),
    path('api/user-list/', views.UserList.as_view(), name='user-list'),
    path('api/my-news/', views.MyPosts.as_view(), name='my-news'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)