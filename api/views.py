from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from api.serializers import TaskSerializer, RegisterUserSerializator, LoginUserSerializator
from todo_list.models import Task
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from api.permissions import IsOvnerOnlyRead


class ListTaskApi(APIView):
    """Views Task"""
    permission_classes = [IsOvnerOnlyRead]

    def get(self, request):
        object_list = Task.objects.filter(user=request.user.pk, execute_status=False).select_related("user")
        serializer = TaskSerializer(object_list, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class RegisterUserApi(APIView):
    """Register user"""

    def post(self, request):
        serializer = RegisterUserSerializator(data=request.data)
        if not serializer.is_valid():
            return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        username = serializer.validated_data.get("username")
        return Response({"message": f"User: {username} created"}, status=status.HTTP_201_CREATED)


class LoginUserApi(APIView):
    """Login User"""

    def post(self, request):
        serializer = LoginUserSerializator(data=request.data)
        if not serializer.is_valid():
            return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(
            username=serializer.data.get("username"),
            password=serializer.data.get("password")
        )
        if not user:
            return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        token, _ = Token.objects.get_or_create(user=user)
        print(token)
        return Response({"token": token.key})
