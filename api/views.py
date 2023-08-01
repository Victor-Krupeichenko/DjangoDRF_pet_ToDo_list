from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from api.serializers import TaskSerializer, RegisterUserSerializator, LoginUserSerializator, TaskCreateSerializer
from todo_list.models import Task
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from api.permissions import IsOvnerReadChange
from rest_framework.permissions import IsAuthenticated


class ListTaskApi(APIView):
    """Views Task"""
    permission_classes = [IsOvnerReadChange]

    def get(self, request):
        """View list tasks"""
        object_list = Task.objects.filter(user=request.user.pk, execute_status=False).select_related("user")
        serializer = TaskSerializer(object_list, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request, task_id):
        """Change execute status"""
        task = Task.objects.filter(pk=task_id).first()
        if task:
            task.execute_status = not task.execute_status
            task.save()
            return Response({"message": f"Task: {task.title} completed"}, status=status.HTTP_202_ACCEPTED)
        return Response({"message": "Task not found"}, status=status.HTTP_400_BAD_REQUEST)


class TaskCreate(APIView):
    """Task create"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TaskCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            response = {
                "message": f"Task: {serializer.validated_data.get('title')} added"
            }
            return Response(response, status=status.HTTP_201_CREATED)
        return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


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
