from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def does_user_exists(request):
    data = request.data
    username = data.get('username')
    password = data.get('password')
    user = User.objects.filter(username=username).exists()
    if user:
        auth = authenticate(request, username=username, password=password)
        if auth is not None:
            return Response({'data': True})
    return Response({'data': False})
