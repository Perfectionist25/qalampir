from django.contrib import admin
from django.template.context_processors import static
from django.conf.urls.static import static
from django.urls import path, include
from qalampir.views import *
from site1 import settings

# http://127.0.0.1:8000/api/news/?is_video=true

urlpatterns = [
    path('admin/', admin.site.urls),

    # Universal url hamma yangiliklar uchun va poisk bilan
    path('api/news/', NewsList.as_view(), name='news-list'),

    # Detail yangilikniki
    path('api/news/<slug:slug>/', NewsDetailView.as_view(), name='news-detail'),

    # Categories
    path('api/categories/', CategoryListCreateView.as_view(), name='category-list-create'),

    # Categoriya bo'yicha yangiliklarni chiqarish
    path('api/categories/<slug:slug>/', CategoryNewsView.as_view(), name='category-news'),

    # Kategoriyalar bo`yicha yangiliklar defolt limit 5 tadan
    path('api/latest-news/', LatestNewsByCategoryView.as_view(), name='latest-news-by-category'),

    # Yangiliklar poiski (yangi url qo`shilgan) !Hali qo`shish jarayonida!
    path('api/news-search/', NewsSearchView.as_view(), name='news-search'),

    path('api/user-list/', UserList.as_view(), name='User-list'),

    # path('api/user-list/<int:pk>', UserDetail.as_view(), name='User-detail'),
]

# faqat DEBUG True bo'lganda media fayllarni development server orqali xizmat qilish
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

