from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework import generics
from django.db.models import F

# Authentication tokens
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

# Local imports
from .serializers import *
from .models import *

from rest_framework.permissions import AllowAny
from django.db import models  # для Q запросов

# Create tokens for users
from rest_framework.authtoken.models import Token
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


# Any admins can see all users (admins) list
class UserList(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None):
        if not request.user.is_staff:
            return Response({"error": "Permission denied"}, status=403)
            
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)
    

# Main admin can see all news and admins can see their news
class MyPosts(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        if request.user.is_superuser:
            queryset = News.objects.all()
        elif request.user.is_staff:
            queryset = News.objects.filter(author=request.user)
        
        serializer = NewsSerializer(queryset, many=True)
        return Response(serializer.data)


# Custom Pagination class
class CustomPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'limit'
    max_page_size = 30  


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


# News list by choosen category
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






# ViewSet для новостей который использует вашу логику
class NewsViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    
    def list(self, request):
        # Используем вашу существующую логику из NewsList
        news_list_view = NewsList()
        return news_list_view.get(request)
    
    def retrieve(self, request, slug=None):
        # Используем вашу существующую логику из NewsDetailView
        news_detail_view = NewsDetailView()
        return news_detail_view.get(request, slug)
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        # Используем вашу существующую логику из NewsSearchView
        search_view = NewsSearchView()
        return search_view.get(request)
    
    @action(detail=False, methods=['get'])
    def my_posts(self, request):
        # Используем вашу существующую логику из MyPosts
        my_posts_view = MyPosts()
        return my_posts_view.get(request)

# ViewSet для категорий
class CategoryViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    
    def list(self, request):
        # Используем вашу существующую логику из CategoryListCreateView
        category_view = CategoryListCreateView()
        return category_view.get(request)
    
    def retrieve(self, request, slug=None):
        # Используем вашу существующую логику из CategoryNewsView
        category_news_view = CategoryNewsView()
        return category_news_view.get(request, slug)
    
    @action(detail=False, methods=['get'])
    def latest_news(self, request):
        # Используем вашу существующую логику из LatestNewsByCategoryView
        latest_news_view = LatestNewsByCategoryView()
        return latest_news_view.get(request)