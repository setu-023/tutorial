from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.http import HttpResponseRedirect


from rest_framework.routers import DefaultRouter
from rest_framework import generics, permissions, renderers # new
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .models import Snippet
from .permissions import IsOwnerOrReadOnly
from .serializers import SnippetSerializer, UserSerializer

class SnippetHighlight(generics.GenericAPIView): # new
    queryset = Snippet.objects.all()
    renderer_classes = (renderers.StaticHTMLRenderer,)

    def get(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)


'''
class sqr_number(generics.ListAPIView): # new
    def cal(request,pk):
        val = pk * pk
    serializer_class = UserSerializer
'''


@api_view(['GET']) # new
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })


class SnippetList(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,) # new

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


def sqr_number(request,pk):
    num = pk
    #for i in range (num,10):
        #if num < 10:
    val = num * num
    return JsonResponse(val,safe=False)


def test_route(request,pk):
    #html = "homepage.html"
    val = pk
    if val > 5 :
        return HttpResponseRedirect(redirect_to='http://127.0.0.1:8000/snippets')

    return HttpResponseRedirect(redirect_to='http://127.0.0.1:8000/homepage')


def homepage(request):
    html =  "homepage.html"
    return render (request,html)


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,) # new

class UserList(generics.ListAPIView): # new
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView): # new
    queryset = User.objects.all()
    serializer_class = UserSerializer
