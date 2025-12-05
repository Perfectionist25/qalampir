from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from qalampir.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),

    # Authentication endpoints
    re_path('login', Login),
    re_path('signup', Signup),
    re_path('logout', Logout),
    re_path('test-token', test_token),

    # API endpoints
    path('api/news/', NewsList.as_view(), name='news-list'),
    path('api/news/<slug:slug>/', NewsDetailView.as_view(), name='news-detail'),
    path('api/categories/', CategoryListCreateView.as_view(), name='category-list'),
    path('api/categories/<slug:slug>/', CategoryNewsView.as_view(), name='category-news'),
    path('api/latest-news/', LatestNewsByCategoryView.as_view(), name='latest-news-by-category'),
    path('api/news-search/', NewsSearchView.as_view(), name='news-search'),
    path('api/user-list/', UserList.as_view(), name='user-list'),
    path('api/my-news/', MyPosts.as_view(), name='my-news'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
