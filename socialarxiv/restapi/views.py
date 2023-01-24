from research.models import Paper
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import PaperSerializer
from .serializers import CommentSerializer, UserSerializer 
from taggit.models import Tag
from research.forms import SearchForm
from research.forms import CommentForm, LoginForm, UserRegistrationForm
from django.contrib.postgres.search import SearchVector
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.core import serializers
import json
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

@api_view(['GET'])
def list_papers(request, tag_slug=None):

    if request.method == 'GET':
        paper_list = Paper.objects.all()
        tag = None

        if tag_slug:
            tag = get_object_or_404(Tag, slug=tag_slug)
            paper_list = paper_list.filter(tags__in=[tag])

        paginator = Paginator(paper_list, 4)
        page_number = request.GET.get('page', 1)

        try:
            papers = paginator.page(page_number)

        except PageNotAnInteger:
            # if page_number is not an integer deliver the first page
            papers = paginator.page(1)

        except EmptyPage:
            papers = paginator.page(paginator.num_pages)
        
        serializer = PaperSerializer(papers, many=True)

        return Response(serializer.data)

@api_view(['GET'])
def paper_detail(request, id):

    if request.method == 'GET':
        paper = Paper.objects.get(id=id)
        comments = paper.comments.filter(active=True)
        comments_serializer = serializers.serialize('json', comments)
        clean_comments = comments_serializer[1:-1]
        to_json = json.loads(clean_comments)
        serializer = PaperSerializer(paper)
       # serializer2 = CommentSerializer(comments)

        return Response({'paper':serializer.data, 'comments': to_json})
    return Response({'error': 'was not a GET request'}, status=400)


@api_view(['GET'])
def post_search(request):

    form = SearchForm()
    results = []
    
    if 'search' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            results = Paper.objects.annotate(
                search=SearchVector('abstract', 'title')
                ).filter(search=form.cleaned_data['search'])
            serializer = PaperSerializer(results, many=True)
            return Response(serializer.data)
        return Response({'error': 'invalid search'}, status=400)
    return Response({'error': 'the term search was not in request'}, status=400)

@api_view(['POST'])
def paper_comment(request, paper_id):
    paper = get_object_or_404(Paper, id=paper_id)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment_data = form.cleaned_data
        comment = form.save(commit=False)
        comment.paper = paper
        comment.save()
        
        return Response(comment_data)
    return Response({'error': 'invalid form'})

@api_view(['POST'])
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return Response({'login': 'Succesful'})
                else:
                    return Response({'login': 'Disabled'})
            else:
                return Response({'Invalid': 'login'})
    else:
        form = LoginForm()

    return Response({'test': 'hello'})

@api_view(['POST']) 
def register(request):
    form = UserRegistrationForm(request.POST)   
    if form.is_valid():
        new_user = form.save(commit=False)
        cd = form.cleaned_data    
        new_user.set_password(cd['password'])

        new_user.save()

        return Response({'account': 'created'}) 

    return Response({'form': 'invalid'})

@api_view(['POST'])
@login_required(login_url='/api/login/')
@csrf_exempt
def user_list(request):
    users = User.objects.filter(is_active=True)
    data_users = serializers.serialize('json', users)

    return Response(data_users)
