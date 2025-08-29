from django.shortcuts import redirect, render
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import JsonResponse
from .models import TblCreator
from rest_framework import status
from .serializer import TblCreatorSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework import viewsets
from .models import Video,tblcomment
from .serializer import VideoSerializer,tblcommentSerializer
from rest_framework.permissions import AllowAny
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import logging

logger = logging.getLogger(__name__)

@api_view(['POST'])
def addcreator(request):
    username = request.data['username']  
    password = request.data['pwd']   
    email = request.data['email']  
    fname = request.data['name'] 
    #fname = request.data['name']   
    serializer = TblCreatorSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        User.objects.create_user(first_name=fname,username=username, email=email, password=password)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def regcreator(request):
    return render(request, 'register.html')

def homepg(request):
    context = {
        'welcome_message': "Hi",  # Or however you generate it
        'trending_videos': [
            {
                'title': 'Sample Title',
                'thumbnail': '/media/path/to/thumb.jpg',
                'video_file': 1,
                'id': 'video-slug-or-id'
            },
            ...
        ]
    }
    return render(request, 'index.html', context)

@login_required
def welcome(request):
    return JsonResponse({'message': f"Welcome, {request.user.first_name}"})

def crlogin(request):
    return render(request, 'login.html')

def watchmv(request):
    return render(request, 'watch.html')


@api_view(['POST'])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    #print("Received data:", request.data)
    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)  # Sets session for future requests
        return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)

   
@api_view(['GET'])
def profile(request):
    if not request.user.is_authenticated:
        return redirect('crlogin')  # your login URL name
    return render(request, 'profile.html')


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def profile_api(request):
    try:
        creator = TblCreator.objects.get(username=request.user)
    except TblCreator.DoesNotExist:
        return Response({'error': 'Creator not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TblCreatorSerializer(creator)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = TblCreatorSerializer(creator, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            
            # Update auth.User fields manually
            user = request.user
            user_email = request.data.get('email')
            first_name = request.data.get('name')
             
            
            if user_email:
                user.email = user_email
            if first_name:
                user.first_name = first_name
            
            
            user.save()
            
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@csrf_exempt
@api_view(['GET'])
def myvideo(request):
    usr = request.user
    if not request.user.is_authenticated:
        return redirect('crlogin')  # your login URL name
    context = {
        'user': usr,  # pass user object to template
    }
    return render(request, 'video.html',context)

@method_decorator(csrf_exempt, name='dispatch')
class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

    def finalize_response(self, request, response, *args, **kwargs):
        # Add CORS headers to every response
        response = super().finalize_response(request, response, *args, **kwargs)
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, PATCH, DELETE, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response

    def options(self, request, *args, **kwargs):
        # Respond to preflight CORS requests
        response = Response(status=status.HTTP_200_OK)
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, PATCH, DELETE, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response
@csrf_exempt
@api_view(['GET'])
def trending_videos(request):
    # Example: Get top 4 videos ordered by id descending (latest first)
    videos = Video.objects.all().order_by('-id')[:8]
    serializer = VideoSerializer(videos, many=True)
    return Response(serializer.data)


@csrf_exempt
@api_view(['POST'])
def addusercomment(request):
    username = request.user.first_name # get from POST data
    comment_text = request.data.get('mesg')  # correct field name
    rating = request.data.get('rating')
    movieid = request.data.get('movieid') or '1'  # fallback

    # Validation
    if not username or not comment_text or not rating:
        return Response({'error': 'All fields are required.'}, status=status.HTTP_400_BAD_REQUEST)

    data = {
        'username': username,
        'mesg': comment_text,   # ✅ correct model field
        'rating': rating,
        'movieid': movieid
    }

    serializer = tblcommentSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['GET'])
def get_comments(request, movieid):
    comments = tblcomment.objects.filter(movieid=movieid)
    serializer = tblcommentSerializer(comments, many=True)
    return Response(serializer.data)
    
    
@api_view(['GET'])
def searchvideos(request):
    title_query = request.GET.get('title', '')
    videos = Video.objects.filter(title__icontains=title_query).order_by('-id')

    context = {
        'videos': videos,
        'query': title_query,
    }

    return render(request, 'search.html', context)


