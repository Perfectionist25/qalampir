from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db.models import F
from .serializers import *
from .models import *

class UserList(APIView):
    def get(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

class UserDetail(APIView):
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

# Custom Pagination class
class CustomPagination(PageNumberPagination):
    page_size = 5  # default page size
    page_size_query_param = 'limit'  # frontend limit yuborishi uchun
    max_page_size = 30  # maksimal limit


# Yangiliklar ro'yxati - frontend nechta so'rasa, o'shancha qaytaradi. Aralash videolik va videosiz yangiliklar.
class NewsList(APIView):
    def get(self, request):
        is_video = request.GET.get('is_video', 'false').lower() == 'true'
        news = News.objects.filter(is_video=is_video).order_by('-created_at')

        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(news, request)
        serializer = NewsSerializer(result_page, many=True)

        return paginator.get_paginated_response(serializer.data)


# Yangilik detail slug orqali qidiriladi
class NewsDetailView(APIView):
    def get(self, request, slug):
        News.objects.filter(slug=slug).update(views=F('views') + 1)
        news = get_object_or_404(News, slug=slug)
        serializer = NewsSerializer(news)
        return Response(serializer.data)


# Kategoriyalar ro'yxati
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer



class CategoryNewsView(APIView):
    def get(self, request, slug):
        category = get_object_or_404(Category, slug=slug)

        # Frontenddan “load more” uchun limit parametri
        # Agar kelmasa default 33
        limit = int(request.GET.get('limit', 33))

        # Barcha yangiliklar (oxirgi birinchi)
        news = News.objects.filter(category=category).order_by('-created_at')[:limit]
        serializer = NewsSerializer(news, many=True)

        data = {
            'category': CategorySerializer(category).data,
            'news': serializer.data,
            'total_loaded': len(serializer.data)
        }

        return Response(data)




# Har bir kategoriya bo'yicha oxirgi videosiz yangiliklar
class LatestNewsByCategoryView(APIView):
    def get(self, request):
        limit = int(request.GET.get('limit', 5))  # Defolt limit 5
        categories = Category.objects.all()
        data = {}

        for category in categories:
            news = News.objects.filter(
                category=category,
                is_video=False
            ).order_by('-created_at')[:limit]
            serializer = NewsSerializer(news, many=True)
            data[category.name] = {
                'category_id': category.id,
                'news': serializer.data
            }

        return Response(data)


# Yangiliklar qidirish
class NewsSearchView(APIView):
    def get(self, request):
        query = request.GET.get('q', '')
        if not query:
            return Response({"error": "Query parameter 'q' is required"}, status=400)

        news = News.objects.filter(
            models.Q(title__icontains=query) |
            models.Q(content__icontains=query)
        ).order_by('-created_at')

        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(news, request)
        serializer = NewsSerializer(result_page, many=True)

        return paginator.get_paginated_response(serializer.data)